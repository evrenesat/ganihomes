# -*- coding: utf-8 -*-
import os
from posix import unlink
import random
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import ugettext
from odeme.estbank import ESTBank
from options import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import simplejson as json
from django.db.models.signals import post_save
from paypal.pro.models import PayPalNVP
from paypal.pro.helpers import PayPalWPP
from utils.cache import kes
from random import randint
from utils.htmlmail import send_html_mail
from utils.thumbnailer import customThumbnailer
import logging
from configuration import configuration
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger('genel')
from django.utils.translation import activate, force_unicode
import codecs
import options
from utils.mail2perm import mail2perm
#LANG_DROPDOWN = []

def send_message(rq, msg, receiver=None, place=None, sender=None, replyto=None, typ=10):
    """
    at least receiver or place should be given
    """
    status = 10
    if place and not hasattr(place, 'id'):
        place = Place.objects.get(pk=place)
    else:
        place = place
    if receiver is None:receiver = place.owner
    if sender is None:
        if typ==40:
            sender = User.objects.filter(is_staff=True, username='GaniHomes')[0]
        else:
            sender = rq.user
            if sender.is_staff:
                typ=40
                status = 20
    msg = sender.sent_messages.create(receiver=receiver, text=msg, status=status, place=place, replyto=replyto, type=typ, lang=rq.LANGUAGE_CODE)
    mail2perm(msg, url=reverse('admin:places_message_change', args=(msg.id, )))
    return msg



for code,name in settings.LANGUAGES:
    activate(code)
#    LANG_DROPDOWN.append((code, force_unicode(_(name))))
    fp = codecs.open('%s/js/gh_%s.js' % (settings.STATIC_ROOT,code), 'w', encoding='utf8')
    for o in ['COUNTRIES','SPACE_TYPES','PLACE_TYPES','JSTRANS']:
        items = {}
        for c in getattr(options,o):
            items[c[0]]=force_unicode(c[1])
        fp.write(u'%s=%s;'% (o, json.dumps(items,ensure_ascii=False)))
    fp.close()

activate(settings.LANGUAGES[0][0])

def clear_place_cache(sender, instance, created, **kwargs):
    pass

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        po, new = Profile.objects.get_or_create(user=instance)
        if new:
            currency = Currency.objects.filter(main=True)
            if currency:
                currency = currency[0]
            else:
                currency = Currency.objects.create(main=True, code='EUR', name='EUR', factor=1)
            po.currency=currency
            po.photo = po.photo.field.attr_class(po, po.photo.field, 'user_photos/user-256.jpg')
            po.save()

post_save.connect(create_user_profile, sender=User)

#from paypal.standard.ipn.signals import payment_was_successful
#from paypal.pro.signals import payment_was_successful
#
#def show_me_the_money(sender, **kwargs):
#    log.info('para aktarimi %s'%sender)
#payment_was_successful.connect(show_me_the_money)

ugettext('Support')
ugettext('Website')
ugettext('Auth')
import re
from urllib2 import urlopen

ecb_forex_xml_regex = re.compile("<Cube currency='(\w*?)' rate='(\d*?.\d*?)'/>")
ecb_forex_xml_url = 'http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml'

class TagCategory(models.Model):
    """Tag category"""

    name = models.CharField(_('Name'), max_length=30)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag Category')
        verbose_name_plural = _('Tag Categories')

    def __unicode__(self):
        return '%s' % (self.name,)

CURR_CACHE = kes('crv')
CURR_CACHE.s(randint(10, 100000), 999999)

MAINCURRID = kes('maincurrid')

class Currency(models.Model):
    """Currencies """

    name = models.CharField(_('Currency name'), max_length=20, unique=True)
    code = models.CharField(_('Currency code'), max_length=3)
    code_position = models.SmallIntegerField(_('Currency placement'), default=1,
        choices=((1, _('Prefix')), (2, _('Suffix'))))
    factor = models.DecimalField(_('Conversation factor'), decimal_places=4, max_digits=12, default='0')
    modify_factor = models.DecimalField(_('Modify updated factor'), decimal_places=4, max_digits=12, default='0',
    help_text=_('Enter a positive or negative decimal value to modify auto-updated conversation ratio.'))
    main = models.BooleanField(_('Main site currency?'), default=False,
        help_text=_('Main currency is the conversation bridge between other currencies.'))
    auto_update = models.BooleanField(_('Auto update'), default=True)
    active = models.BooleanField(_('Active'), default=False)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    def get_factor(self, target_currency_id=None):
        c =  Currency.objects.filter(pk=target_currency_id) if target_currency_id else Currency.objects.filter(main=True)
        return c.values_list('factor')[0][0] / self.factor

    def convert_to(self, amount, target):
        return amount * self.get_factor(target)

    @classmethod
    def get_main_id(cls, get_obj=False):
        return MAINCURRID.g() or MAINCURRID.s(cls.objects.filter(main=True).values_list('id', flat=True)[0])

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def save(self, *args, **kwargs):
        super(Currency, self).save(*args, **kwargs)
        self.generateJSON()

    @classmethod
    def updateRates(cls):
        rates = urlopen(ecb_forex_xml_url).read()
        for r in ecb_forex_xml_regex.findall(rates):
            try:
                c, new = Currency.objects.get_or_create(name=r[0])
                if c.auto_update:
                    c.factor = Decimal(str(r[1])) + c.modify_factor
                    c.save()
            except:
                log.exception('currency update rate : %s'% repr(r))

    @classmethod
    def generateJSON(cls):
        CURR_CACHE.incr()
        di = {}
        for c in Currency.objects.filter(active=True):
            if c.factor:
                di[c.id] = [str(round(float(c.factor), 4)), c.name, c.code, c.code_position]
        f = codecs.open(os.path.join(settings.STATIC_ROOT, "js", u'curr.js'), 'w', 'utf-8')
        f.write((u"gh_crc=%s" % json.dumps(di, ensure_ascii=False)).replace(" ", ''))
        f.close()


    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code,)


class PromotionCode(models.Model):
    """Promotion codes """

    code = models.CharField(_('Promotion code'), max_length=10, unique=True)
    type = models.SmallIntegerField(_('Type'), choices=PROMOTION_TYPES)
    puser = models.ForeignKey(User, verbose_name=_('Who used this code'), related_name='used_promotions')
    sender = models.ForeignKey(User, verbose_name=_('Sender/Inviter'), related_name='related_promotions')
    percentage = models.DecimalField(_('Percentage'), decimal_places=2, max_digits=8)
    price = models.DecimalField(_('Promotion Amount'), help_text=_('Discount amount'), decimal_places=2, max_digits=6)
    used = models.BooleanField(_('Used'), default=False)
    active = models.BooleanField(_('Active/Valid'), default=True)
    expiry_date = models.DateField(_('Expiry date'), null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Promotion Code')
        verbose_name_plural = _('Promotion Codes')


    def __unicode__(self):
        return '%s' % (self.code,)


class Transaction(models.Model):
    """money transactions"""

    user = models.ForeignKey(User, verbose_name=_('Sender'))
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=8)
    type = models.SmallIntegerField(_('Type'), choices=TRANSACTION_TYPES)
    status = models.SmallIntegerField(_('Transaction status'), choices=TRANSACTION_STATUS)
    receiver_type = models.SmallIntegerField(_('Receiver type'), choices=MONEY_NODES)
    sender_type = models.SmallIntegerField(_('Sender type'), choices=MONEY_NODES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    active = models.BooleanField(_('Active'), default=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    details = models.TextField(_('Transection details'), null=True, blank=True)#readonly

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __unicode__(self):
        return '%s' % (self.amount,)

    @classmethod
    def get_bank(cls, r):
        return ESTBank(name=settings.POS_NAME,
                    ssl=settings.CHECKOUT_SSL,
                    bank_data=settings.POS_DENIZBANK,
                    domain=settings.SITE_NAME,
                    ok_url = '/%s/cc_success/' % r.LANGUAGE_CODE,
                    fail_url='/%s/cc_fail/' % r.LANGUAGE_CODE)


class Tag(models.Model):
    """Place tags"""

    category = models.ForeignKey(TagCategory)
#    lang = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    name = models.CharField(_('Name'), max_length=30)
    help = models.TextField(_('Help Text'), default='', blank=True)
    active = models.BooleanField(_('Active'), default=True)
    order = models.SmallIntegerField(_('Order'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['order']
        get_latest_by = "timestamp"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return '%s' % (self.name,)


    @classmethod
    def getTags(cls, lang=None):
        return kes(lang,'tags').g() or cls._updateCache(lang)


    @classmethod
    def _updateCache(cls, lang=None):
        for code,name in settings.LANGUAGES:
            tags = []
#            if code == 'en': #assuming en as the default language
#                for d in cls.objects.filter(active=True).values('id','name','help'):
#                    tags.append(d)
#            else:
            for d in TagTranslation.objects.filter(tag__active=True,lang=code).values('tag_id','translation','help'):
                tags.append({'id':d['tag_id'],'help':d['help'],'name':d['translation']})
            kes(code,'tags').s(tags,999999)
            if lang:
                lang = tags
        return lang

    def save(self, *args, **kwargs):
        self._updateCache()
        super(Tag, self).save(*args, **kwargs)

class TagTranslation(models.Model):
    """Place description"""

    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), related_name='tags')
    lang = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES)
    translation = models.CharField(_('Translation'), max_length=30)
    help = models.TextField(_('Help Text'), default='', blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag Translation')
        verbose_name_plural = _('Tag Translations')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.tag_id, self.lang)


import datetime
from django.utils.safestring import mark_safe

def date_range(start, end):
    r = (end + datetime.timedelta(days=1) - start).days
    return [start + datetime.timedelta(days=i) for i in range(r)]


class GeoLocation(models.Model):
    id = models.IntegerField('WOEID', primary_key=True)
    iso = models.CharField(_('Country'), max_length=2, db_index=True)
    name = models.CharField(_('Name'), max_length=100, db_index=True)
    type = models.SmallIntegerField(_('Type'), choices=LOCATION_TYPES)
    #    parent_id = models.IntegerField('WOEID')
    parent = models.ForeignKey('self')
    #    alias = models.CharField(_('Alias'), max_length=100,default='')
    #    popularity = models.IntegerField('Popularity',default=0)
    #    priority = models.IntegerField('Priority',default=0)
    #

    def findLocation(self, location_name):
        print 'locationame', location_name
        if location_name:
            for gl in self.g.filter(name__contains=location_name):
                print 'gl', gl
                if gl.parent in self.loclist:
                    return gl


    def getSublocs(self, loc_name_list):
        """
        loc_name_list = [state, city, district, neighborhood]
        """
        print 'loc_name_list', loc_name_list
        self.loclist = [self]
        self.g = GeoLocation.objects.filter(iso=self.iso)
        for l in loc_name_list:
            l = self.findLocation(l)
            if l:
                self.loclist.append(l)
        return self.loclist


    class Meta:
    #        ordering = ['priority','popularity']
        verbose_name = _('GeoLocation Data')
        verbose_name_plural = _('GeoLocation Datas')

    def __unicode__(self):
        return '%s %s' % (self.iso, self.name)


#
#class GeoLocationAliases(models.Model):
#    gl = models.ForeignKey(GeoLocation,verbose_name=_('Geolocation'))
#    alias = models.CharField(_('Alias name'), max_length=100, db_index=True)
#
#    class Meta:
##        ordering = ['priority','popularity']
#        verbose_name = _('GeoLocation Alias')
#        verbose_name_plural = _('GeoLocation Aliases')
#
#    def __unicode__(self):
#        return '%s %s' % (self.alias, self.gl_id)
from decimal import Decimal
class Place(models.Model):
    """Places"""

    owner = models.ForeignKey(User, verbose_name=_('Host'))
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'), null=True, blank=True)
    title = models.CharField(_('Place title'), max_length=100)
    slug = models.SlugField(_('URL Name'), null=True, blank=True)
    address = models.CharField(_('Address Line'), max_length=100, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    street = models.CharField(_('Street'), max_length=60)
    i18_tags = models.CharField(_('Multi-ling location info'), max_length=255,  null=True, blank=True, editable=False)
    postcode = models.CharField(_('Postcode'), max_length=15, null=True, blank=True)
    city = models.CharField(_('City'), max_length=40)
    district = models.CharField(_('District'), max_length=40, null=True, blank=True)
    #    woeid = models.IntegerField('WOEID')
    placement = models.ManyToManyField(GeoLocation, verbose_name=_('Geographic Location'), null=True, blank=True)
    neighborhood = models.CharField(_('Neighborhood'), max_length=40, null=True, blank=True)
    state = models.CharField(_('State/Region'), max_length=40, null=True, blank=True)
    emergency_phone = models.CharField(_('Emergency phone'), max_length=20, null=True, blank=True)
    #    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'))
    primary_photo = models.ImageField(_('Primary photo'), upload_to='place_photos', null=True, blank=True)
    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)
    gprice = models.DecimalField(_('Converted Price'), help_text=_('Price in main site currency (eg:euro)'), null=True, blank=True, decimal_places=2, max_digits=6)
    capacity = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS, default=6)
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES, default=1)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES, default=1)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS, default=1)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES, default=1)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS, default=1)
    size = models.IntegerField(_('Size'), null=True, blank=True)
    size_type = models.IntegerField(_('Measurement type'), choices=MTYPES, default=2)
    cancellation = models.SmallIntegerField(_('Cancellation policy'), choices=CANCELATION_RULES, default=1)
    min_stay = models.SmallIntegerField(_('Minimum number of nights'), choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(_('Maximum number of nights'), choices=MAX_STAY, default=0)
    manual = models.TextField(_('House manual'), null=True, blank=True)
    rules = models.TextField(_('House rules'), null=True, blank=True)
    #    pets = models.BooleanField(_('Pets'), default=False, help_text=_('Pets exists'))
    favorite_counter = models.IntegerField(_('Favorite counter'), default=0)
    overall_rating = models.SmallIntegerField(_('Overall rating'), choices=PLACE_RATING, default=0)
    clean_rating = models.SmallIntegerField(_('Cleaness'), choices=PLACE_RATING, default=0)
    comfort_rating = models.SmallIntegerField(_('Comfort'), choices=PLACE_RATING, default=0)
    location_rating = models.SmallIntegerField(_('Location'), choices=PLACE_RATING, default=0)
    value_money_rating = models.SmallIntegerField(_('Value/Money Rating'), choices=PLACE_RATING, default=0)
    description = models.TextField(_('Description'), null=True, blank=True)
#    version = models.IntegerField(_('Version'), default=1)
    lang = models.CharField(_('Language'), max_length=5, choices=LANGUAGES)
    #    geocode = models.CharField(_('Geographical Location'), max_length=40, null=True, blank=True)
    lat = models.FloatField(_('Latitude'), default=0.0)
    lon = models.FloatField(_('Longitude'), default=0.0)

    weekly_discount = models.SmallIntegerField(_('Weekly discount (%)'), null=True, blank=True, default=0)
    monthly_discount = models.SmallIntegerField(_('Monthly discount (%)'), null=True, blank=True, default=0)
    weekend_price = models.DecimalField(_('Weekend price'), help_text=_('Weekend price for guest'), decimal_places=2,
        max_digits=6, default='0.0')
    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS, null=True,
        blank=True, default=0, help_text=_('Weekend price for guest'))
    extra_price = models.DecimalField(_('Extra charge per person'), null=True, blank=True, decimal_places=2,
        max_digits=6,
        help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))
    cleaning_fee = models.DecimalField(_('Cleaning fee'), decimal_places=2, max_digits=8, null=True, blank=True)
    street_view = models.BooleanField(_('Street view'), default=False)
    translated = models.BooleanField(_('Translated'), default=False)

    active = models.BooleanField(_('Etkin'), default=True, help_text=u'Etkin olmayan mekanlar kendi sahibine bile gösterilmez. Ev sahibi için "silinmiş" gibi görünür. ')
    has_photo = models.BooleanField(_('Place has a photo'), default=False, editable=False)
    published = models.BooleanField(_('Published'), default=False)
    timestamp = models.DateTimeField(_('Creatation'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
#    translation_status = models.SmallIntegerField(_('Translation status'), choices=TRANSLATION_STATUS, default=10)

    #####JSON CACHES######
    reserved_dates = models.TextField(editable=False, default='')
    prices = models.TextField(editable=False, default='')
    summary = models.TextField(editable=False, default='')
    #    details = models.TextField(editable=False, default='')
    SHORTS = {'id': 'id', 'title': 'tt', 'city': 'ci', 'district': 'di',
              'country': 'co', 'postcode': 'pc','currency_id': 'cid',
              'owner_id': 'oid', 'lat': 'lt', 'lon': 'ln', 'state': 'st',
              'favorite_counter': 'fc', 'overall_rating': 'or',
              'type':'typ', 'space':'spc','price':'prc','has_photo':'pht'
    }

    def admin_image(self):
        return '<a href="%s"><img src="%s/place_photos/%s_plkks.jpg"/></a>'%(self.get_absolute_url(), settings.MEDIA_URL, self.id)
    admin_image.allow_tags = True

    def get_absolute_url(self):
        return '/%s%s' % (self.lang[:2] or 'en', reverse('show_place', args=(self.id, )) )

    def _updateSummary(self):
        di = {}
        for k, v in self.SHORTS.items():
            val = getattr(self, k)
#            if k in ['has_photo',]:
#                val = val()
            if isinstance(val, Decimal): val = float(val)
            di[v] = val
        self.summary = json.dumps(di, ensure_ascii=False)

    def siblings(self):
        return Place.objects.filter(active=True, published=True, owner=self.owner).exclude(pk=self.id)

    def translation_check(self):
        """marks  if place title or description has updated"""
        if self.id:
            title,desc = Place.objects.filter(pk=self.id).values_list('title','description')[0]
            if title != self.title or desc != self.description:
                self.translated = False


    def get_size(self):
        return mark_safe('%s  %s<sup style="line-height:0;">2</sup>' % (
        self.size, self.get_size_type_display()) if self.size else '-')

    # [ 0|sessional_prices_list[[startdate, enddate, price, weekendprice]],
    # 1|default_price, 2|weekend_price, 3|currency_id, 4|weekly_discount, 5|monthly_discount,
    #  6|extra_limit, 7|extra_price, 8|cleaning_fee]
    def _updatePrices(self):
        di = [float(str(self.price)), float(str(self.weekend_price)), self.currency_id, self.weekly_discount or 0,
              self.monthly_discount or 0, self.extra_limit or 0, float(str(self.extra_price or 0)),
              float(str(self.cleaning_fee or 0))]
        sessions = []
        for sp in self.sessionalprice_set.filter(active=True, end__gte=datetime.datetime.today()):
            sessions.append([sp.start.timetuple()[:3], sp.end.timetuple()[:3], float(str(sp.price or 0)),
                             float(str(sp.weekend_price or 0))])
        di.insert(0, sessions)
        self.prices = json.dumps(di)

    def getTags(self, lang):
        k=kes('tgs',self.id,lang)
        tags = k.g([])
        if not tags:
            tag_ids = self.tags.values_list('id',flat=True)
            for t in Tag.getTags(lang):
                if t['id'] in tag_ids:
                    t['class']='hit'
                tags.append(t)
            k.s(tags)
        return tags

    def invalide_caches(self):
        desc_trans_list = kes('ptranslist',self.id)
        for l in desc_trans_list:
            kes('ptrans',self.id,l).d()
        desc_trans_list.d()

    def get_translation_list(self, reset=None):
        k=kes('ptranslist',self.id)
        sonuc = k.g() if reset is None else False
        return sonuc or k.s(self.descriptions.filter(text__isnull=False).values_list('lang', flat=True) or [''],500)

    @classmethod
    def c_get_translation(cls,place_id, lang):
        k=kes('ptrans',place_id,lang)
        try:
            return k.g() or k.s(Description.objects.filter(place_id=place_id, lang=lang).values_list('text','title')[0])
        except:
            return '',''

    def get_translation(self,lang):
        return self.c_get_translation(self.id, lang)


    def setGeoLocation(self):
        cset = [[l.geolocation_set.count(), l] for l in  GeoLocation.objects.filter(parent_id=1, iso=self.country)]
        country = sorted(cset, key=lambda x: x[0])[-1][1]
        locset = country.getSublocs([self.state, self.city, self.district, self.neighborhood])
        return locset
        self.placement.add(locset)
        self.save()


    def updateReservedDates(self):
        ard = []
        for rd in self.reserveddates_set.filter(end__gte=datetime.datetime.today()):
            r = (rd.end + datetime.timedelta(days=1) - rd.start).days
            ard.extend([int((rd.start + datetime.timedelta(days=i)).strftime('%y%m%d')) for i in range(r)])
        self.reserved_dates = json.dumps(ard)
        self.save()

    def getReservedDates(self):
        ard = []
        for rd in self.reserveddates_set.filter(end__gte=datetime.datetime.today()):
            ard.append([int(rd.start.strftime('%y%m%d')),int(rd.end.strftime('%y%m%d')), rd.type] )
        return json.dumps(ard)

    def setUnavailDates(self, jsdata, type=1):
        self.reserveddates_set.filter(end__gte=datetime.datetime.today(), type=type).delete()
        for dt in json.loads(jsdata):
            st=str(dt[0])
            en=str(dt[1])
            st = '%s-%s-%s' %(st[:4], st[4:6], st[6:8])
            en = '%s-%s-%s' %(en[:4], en[4:6], en[6:8])
            self.reserveddates_set.create(type=1, start=st, end=en)
        return True

    def reorderPhotos(self, jsdata):
        order = 0
        ids = json.loads(jsdata)
#        self.primary_photo = self.photo_set.get(pk=ids[0]).image
#        self.save()
        for id in ids:
            if not id: continue
            order +=1
            self.photo_set.filter(pk=id).update(order=order)
        self.pick_primary_photo()
        return True

    def calculatePrice(self, start, end ):
        pd = self.getSessionalPriceDict()
        price = Decimal('0.0')
        nights = (end - start).days
#        log.info('pd %s ' % (pd))
        log.info('nights %s ' % (nights))
        mdiscount=0
        wdiscount=0
        guest_fee=0
        for d in range(nights):
            day = start + datetime.timedelta(days=d)
            price+=pd.get(int(day.strftime('%y%m%d'))) or (self.weekend_price if (day.weekday() in [6,7] and self.weekend_price) else self.price)
#            log.info(day.strftime('%y-%m-%d'))
#        log.info('after days %s ' % (price))
        if self.monthly_discount and nights>=30:
            mdiscount = price * self.monthly_discount / Decimal('100')
            price = price - mdiscount
#        log.info('after mont %s ' % (price))
        if self.weekly_discount and nights>=7:
            wdiscount = price * self.weekly_discount / Decimal('100')
            price = price - wdiscount
#        log.info('after week %s ' % (price))
        guest_fee = configuration('guest_fee') or 0
        if guest_fee:
            guest_fee = price * guest_fee/Decimal('100')
            price = price + guest_fee
        if self.cleaning_fee:
            price+=self.cleaning_fee
#        log.info('after clean %s ' % (price))
        return price, guest_fee, wdiscount, mdiscount




    def getSessionalPriceDict(self):
        price_dict = {}
        for sp in self.sessionalprice_set.filter(end__gte=datetime.datetime.today()):
            r = (sp.end + datetime.timedelta(days=1) - sp.start).days
            for i in range(r):
                day = sp.start + datetime.timedelta(days=i)
                price_dict[int(day.strftime('%y%m%d'))]= sp.weekend_price if day.weekday() in [6,7] else sp.price
        return price_dict

    def calculateTotalPrice(self, currency_id, start, end, guests):
        factor = self.currency.get_factor(currency_id)
        nights = (end + datetime.timedelta(days=1) - start).days
        total, guest_fee, wdiscount, mdiscount = [p * factor for p in  self.calculatePrice(start, end)]
#        log.info('total %s ' % (total))
        if self.extra_price and self.extra_limit < guests:
            total = total + ((self.extra_price * Decimal(str(guests - self.extra_limit) ) * factor ) * nights)
#        log.info('after extra %s ' % (total))
        return {'total': total,'guest_fee':guest_fee,
                'wdiscount':wdiscount, 'mdiscount':mdiscount,
                'cleaning_fee':self.cleaning_fee,
        }

    def createThumbnails(self):
        if self.primary_photo:
            customThumbnailer(self.primary_photo, self.id, PLACE_THUMB_SIZES)
            self.has_photo = bool(self.primary_photo)

    def pick_primary_photo(self):
        photos = self.photo_set.all()
        if photos:
            self.has_photo = True
            self.primary_photo = photos[0].image
            self.cleanup_place_thumbs()
            self.save()

    def cleanup_place_thumbs(self):
        for s in PLACE_THUMB_SIZES:
            try:
                unlink('%s/place_photos/%s_%s.jpg' % (settings.MEDIA_ROOT,self.id, s[2] ) )
            except OSError:
                log.exception('gorsel silinirken hata')

    def save(self, *args, **kwargs):
        self._updatePrices()
        self._updateSummary()
        self.createThumbnails()
        self.calculateGPrice()
        super(Place, self).save(*args, **kwargs)

    def calculateGPrice(self):
        factor = self.currency.get_factor()
        self.gprice = self.price * factor

    class Meta:
        ordering = ['-has_photo','-overall_rating','timestamp']
        get_latest_by = "timestamp"
        verbose_name = _(u'Place')
        verbose_name_plural = _(u'Places')

    def __unicode__(self):
        return '%s' % (self.title,)



class Friendship(models.Model):
    """Friendship"""

    fr1 = models.ForeignKey('Profile', related_name='fr1')
    fr2 = models.ForeignKey('Profile', related_name='fr2')
    confirmed = models.BooleanField(_('Confirmed'), default=False)


from django_facebook.models import FacebookProfileModel
class Profile(FacebookProfileModel):
    """User profile"""


    #    usr = models.OneToOneField(User, verbose_name=_('User'), related_name='uusr')
    user = models.OneToOneField(User, verbose_name=_('User'), null=True, blank=True)
    photo = models.ImageField(_('Photo'), upload_to='user_photos', null=True, blank=True)
    favorites = models.ManyToManyField(Place, verbose_name=_('Favorite places'), null=True, blank=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    cell = models.CharField(_('Cellular Phone'), max_length=20, null=True, blank=True)
    occupation = models.CharField(_('Occupation'), max_length=30, null=True, blank=True)
    twitter = models.CharField(_('Twitter'), max_length=60, null=True, blank=True)
    facebook = models.CharField(_('Facebook'), max_length=60, null=True, blank=True)
    brithdate = models.DateField(_('Brithdate'), null=True, blank=True)
    lastlogin = models.DateTimeField(_('Last login time'), auto_now=True)
    lang = models.CharField(_('Default Language'), max_length=5, choices=LOCALES, default='tr_TR')
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    private_name = models.CharField(_('Private Name'), max_length=60, null=True, blank=True)
    full_name = models.CharField(_('Full Name'), max_length=60, null=True, blank=True)
    bio = models.TextField(_('About you'), null=True, blank=True)

    #FIXME: rename profile photo

    def get_friends(self, confirmed=False):
        friendship = Friendship.objects.filter(Q(fr1=self)|Q(fr2=self))
        if confirmed:
            friendship = friendship.exclude(confirmed=False)
        return [f.fr1 if f.fr2==self else f.fr2 for f in friendship]

    def is_friend(self, profile):
        return profile in self.get_friends()

    def save(self, *args, **kwargs):
        self.update_names()
        super(Profile, self).save(*args, **kwargs)
        self.createThumbnails()

    def update_names(self):
        if self.user.last_name:
            self.private_name = (u"%s %s." % (self.user.first_name, self.user.last_name[0])).title()
        self.full_name = self.user.get_full_name()

    def createThumbnails(self):
        customThumbnailer(self.photo, self.user.id,
            [   (200, 300, 'xl'),
                (200, 0, 'l'),
                (100, 0, 'm'),
                (0, 30, 's')],
            mark=False, crop='scale')

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return '%s #%s' % (self.full_name, self.user_id,)

class PaymentSelection(models.Model):
    '''Payment Selections'''

    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    user = models.OneToOneField(User, verbose_name=_('User'), null=True, blank=True)
    payment_type = models.SmallIntegerField(_('Payment type'), choices=PAYMENT_TYPES, default=2, blank=True)
    email = models.EmailField(_('PayPal email'), null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    active = models.BooleanField(_('Active'), default=True)
    acc_owner = models.CharField(_('Account Owner'), max_length=40, null=True, blank=True)
    iban = models.CharField(_('IBAN/Account No'), max_length=40, null=True, blank=True)
    bic = models.CharField(_('SWIFT/BIC Code'), max_length=40, null=True, blank=True)
    street = models.CharField(_('Street'), max_length=40, null=True, blank=True)
    postcode = models.CharField(_('Postcode'), max_length=40, null=True, blank=True)
    city = models.CharField(_('City'), max_length=40, null=True, blank=True)
    bank_name = models.CharField(_('Bank name'), max_length=40, null=True, blank=True)
    bank_street = models.CharField(_('Bank street'), max_length=40, null=True, blank=True)
    bank_postcode = models.CharField(_('Bank postcode'), max_length=40, null=True, blank=True)
    bank_city = models.CharField(_('Bank city'), max_length=40, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Payment Selection')
        verbose_name_plural = _('Payment Selections')

    def __unicode__(self):
        return '%s %s' % (self.user.username,self.get_payment_type_display())



class ReservedDates(models.Model):
    """unavailable dates"""

    start = models.DateField(_('Reservation Start'))
    end = models.DateField(_('Reservation End'))
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    type = models.SmallIntegerField(_('Reason'), choices=UNAVAIL_REASON)
    # = models.CharField(_(''))
    # = models.IntegerField(_(''))

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Reserved Date')
        verbose_name_plural = _('Reserved Dates')

    def __unicode__(self):
        return '%s - %s' % (self.start, self.end)

    def save(self, *args, **kwargs):
        super(ReservedDates, self).save(*args, **kwargs)
        self.place.updateReservedDates()

    def delete(self, *args, **kwargs):
        super(ReservedDates, self).delete(*args, **kwargs)
        self.place.updateReservedDates()


def update_filename(instance, filename):
    format = '%s_%s%s' % (instance.place_id, random.randrange(99999), os.path.splitext(filename)[1])
    return os.path.join('place_photos', format)

class Photo(models.Model):
    """Photos"""

    #FIXME : delete actual file on delete

    place = models.ForeignKey(Place, verbose_name=_('Place'), null=True, blank=True)
    name = models.CharField(_('Image name'), max_length=60, null=True, blank=True)
    image = models.ImageField(_('Image File'), upload_to=update_filename)
    type = models.SmallIntegerField(_('Photo type'), choices=PHOTO_TYPES, null=True, blank=True)
    order = models.SmallIntegerField(_('Display order'), default=60)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['order']
        get_latest_by = "timestamp"
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return '%s' % (self.name,)


    def admin_image(self):
        return '<a href="%s"><img src="%s/place_photos/%s_xs.jpg"/></a>'%(self.image.url, settings.MEDIA_URL, self.id)
    admin_image.allow_tags = True

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
#        customThumbnailer(self.image, self.id, [(50, 50, 's')])
        customThumbnailer(self.image, self.id, PHOTO_THUMB_SIZES)
        #FIXME: order on save
        if self.place and (self.order == 1 or not self.place.primary_photo):
            self.place.pick_primary_photo()

    def delete(self, *args, **kwargs):
        id = self.id
        order = self.order
        place = self.place
        try:
            unlink(self.image.path)
        except:
            log.exception('ana img silinirken hata')
        super(Photo, self).delete(*args, **kwargs)

        for s in PHOTO_THUMB_SIZES:
            try:
                unlink('%s/place_photos/%s_%s.jpg' % (settings.MEDIA_ROOT,id, s[2] ) )
            except:
                log.exception('thumb %s silinirken hata' % repr(s))
        if order == 1 and place:
            place.pick_primary_photo()




class Booking(models.Model):
    """Booking"""

    host = models.ForeignKey(User, verbose_name=_('Host'), related_name='hostings')
    guest = models.ForeignKey(User, verbose_name=_('Guest'), related_name='guestings')
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    reservation = models.ForeignKey(ReservedDates, verbose_name=_('Reservation Dates'), null=True, blank=True)
    nguests = models.SmallIntegerField(_('Number of guests'))
    nights = models.SmallIntegerField(_('Nights'),default=0)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'))
    start = models.DateField(_('Booking start'))
    end = models.DateField(_('Booking end'))
    summary = models.CharField(_('Summary'), max_length=100, null=True, blank=True)
    valid = models.BooleanField(_('Valid'), default=True)
    status = models.SmallIntegerField(_('Status'), choices=BOOKING_STATUS, default=5)
    payment_type = models.SmallIntegerField(_('Payment type'), choices=PAYMENT_TYPES, null=True, blank=True)
    guest_payment = models.DecimalField(_('Total payment for guest'), decimal_places=2, max_digits=8)
    host_earning = models.DecimalField(_('Host\'s earning'), decimal_places=2, max_digits=8)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    rejection_date = models.DateTimeField(null=True, blank=True)
    guest_ok_date = models.DateTimeField(null=True, blank=True)
    payment_notification_date = models.DateTimeField(null=True, blank=True)
    payment_confirmation_date = models.DateTimeField(null=True, blank=True)
    payment_transfer_date = models.DateTimeField(null=True, blank=True)

    def getPaypalAuthTransaction(self):
        return PayPalNVP.objects.filter(custom=self.id,method='DoExpressCheckoutPayment')[0]

    def capturePayment(self,request):
        if self.payment_type==2: #paypal
            auth_transaction = self.getPaypalAuthTransaction()
            wpp = PayPalWPP(request)
            if auth_transaction.transactionid == 'testest':
                return True
            capture_transaction = wpp.doCapture({
                'AUTHORIZATIONID':auth_transaction.transactionid,
                'CURRENCYCODE':auth_transaction.currencycode,
                'AMT':auth_transaction.amt,
            })
            return auth_transaction.transactionid == capture_transaction.transactionid
        elif self.payment_type == 1:#cc
            bnk = Transaction.get_bank(request)
            basarilimi, sonuc, xml_sonuc = bnk.request({'type':'PostAuth', 'oid':self.id})
            return basarilimi

    def send_booking_request(self, rq):
        msg = _("""%(guest)s would like to stay at your place %(title)s on %(start)s through %(end)s. Please <a href='?showBookingRequest=%(bid)s'>accept or decline</a> this  reservation in 24 hours .
        Phone, email, and address information will be exchanged between guest/host after you accept the guest.
        """)
        msg = force_unicode(msg) % {
            'guest':self.guest.get_profile().private_name,
            'title':self.place.title,
            'start':self.start,
            'end':self.end,
            'bid':self.id,
        }
        send_message(rq, msg, place=self.place, typ=30, sender=self.guest)

    def voidPayment(self, request):
        if self.payment_type==2: #paypal
            wpp = PayPalWPP(request)
            auth_transaction = self.getPaypalAuthTransaction()
            void_transaction = wpp.doVoid({'AUTHORIZATIONID':auth_transaction.transactionid,})
            return auth_transaction.transactionid == void_transaction.transactionid
        elif self.payment_type == 1:#cc
            bnk = Transaction.get_bank(request)
            basarilimi, sonuc, xml_sonuc = bnk.request({'type':'Void', 'oid':self.id})
            return basarilimi

    def refundPayment(self):
        #TODO: implement paypal refund
        pass

    def payoutHost(self):
        #TODO: implement payout host
        pass

    def del_reservation(self):
        r = self.reservation
        if r:
            self.reservation = None
            self.save()
            r.delete()

    def set_reservation(self):
        self.reservation = ReservedDates.objects.create(place = self.place, start= self.start, end=self.end, type=2)

    def save(self, *args, **kwargs):
        if not self.host_earning:
            self.host_earning =  self.place.price * ((100-configuration('host_fee'))/100)
        super(Booking, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __unicode__(self):
        return '%s %s' % (self.summary,self.id)


class SessionalPrice(models.Model):
    """Sessional pricing"""
    place = models.ForeignKey(Place, verbose_name=_('Place'))
#    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    weekend_price = models.DecimalField(_('Weekend price'), decimal_places=2, max_digits=8, null=True, blank=True)
    active = models.BooleanField(_('Active'), default=True)
    start = models.DateField(_('Session start'))
    end = models.DateField(_('Session end'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Sessional Price')
        verbose_name_plural = _('Sessional Prices')

    def __unicode__(self):
        return '%s' % (self.id,)

    def save(self, *args, **kwargs):
        super(SessionalPrice, self).save(*args, **kwargs)
        #        self.place.update_prices()
        self.place.save()


class Description(models.Model):
    """Place description"""

    place = models.ForeignKey(Place, verbose_name=_('Place'), related_name='descriptions')
    lang = models.CharField(_('Language'), max_length=2)
    text = models.TextField(_('Description'))
    title = models.CharField(_('Place title'), max_length=100)
#    version = models.IntegerField(_('Version'), default=1)
    auto = models.BooleanField(_('Auto translation'),default=False)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Description')
        verbose_name_plural = _('Descriptions')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.place_id, self.lang)



    def save(self, *args, **kwargs):
        super(Description, self).save(*args, **kwargs)
        kes('ptranslist',self.place_id).d()



class Message(models.Model):
    """user messaging system"""

    replyto = models.ForeignKey('self', verbose_name=_('First message'),  null=True, blank=True)
    sender = models.ForeignKey(User, verbose_name=_('Sender'), related_name='sent_messages')
    receiver = models.ForeignKey(User, verbose_name=_('Receiver'), related_name='received_messages')
    place = models.ForeignKey(Place, verbose_name=_('Place'),  null=True, blank=True)
    text = models.TextField(_('Message'))
    read = models.BooleanField(_('Was read'), default=False)
    sent = models.BooleanField(_('Sent'), default=False, help_text=u"Alıcıya uyarı epostası gönderilmiş mi?")
    replied = models.BooleanField(_('Replied'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=MESSAGE_STATUS, default=10)
    type = models.SmallIntegerField(_('Type'), choices=MESSAGE_TYPES, default=0)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    last_message_time = models.DateTimeField(_('Last message time'), default=datetime.datetime.now())
    lang = models.CharField(_('Language'), max_length=2, choices=LANGUAGES)
#
#    def __init__(self, *args, **kwargs):
#       super(Message, self).__init__(*args, **kwargs)
#       self.old_status = self.status

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        if not self.sent and self.status == 20:
            if self.send_message():
                self.sent = True

        kes('mcount',self.receiver_id).d()

    def send_message(self):
        """
        send a notification email to the receiver
        """
        mail_context = {
            'link': u'/dashboard/?showMessage=%s'% self.id,
            'surname':self.receiver.last_name,
            'LANGUAGE_CODE':self.lang
        }
        subject = self.get_type_display()
        obj = None
        if self.type in [10,20]:  obj = self.sender.get_profile().private_name
        elif self.type == 30:     obj = self.place.title
        elif self.type in [50]:   obj = self.sender.get_full_name()

        if obj:
            subject = subject % obj
        return send_html_mail(subject, self.receiver.email, mail_context, template='mail/new_message.html', recipient_name=self.receiver.get_full_name())


    @classmethod
    def message_count(cls, request, reset=False):
        try:
            mcount = kes('UMC',request.session.session_key)
#            log.info('%s %s'% ('USRMSGCOUNT',request.session.session_key))
            cnt = mcount.g()
            return cnt if isinstance(cnt,int) else mcount.s(cls.objects.filter(read=False, receiver=request.user, status__gte=20).count(),600)
        except:
            return 0

    def get_sender_name(self):
        return self.sender.get_profile().private_name

    def get_receiver_name(self):
        return self.receiver.get_profile().private_name

    def isnew(self):
        return (not self.read or self.hasnewrepy)

    class Meta:
        ordering = ['-last_message_time']
        get_latest_by = "timestamp"
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __unicode__(self):
        return 'Message from user #%s' % (self.sender,)


class UserReview(models.Model):
    """user reviews"""

    writer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='personal_reviews_by_you')
    person = models.ForeignKey(User, verbose_name=_('Person'), related_name='personal_reviews_about_you')
    text = models.TextField(_('Review'))
    active = models.BooleanField(_('Review visible on the site'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=REVIEW_STATUS, default=1)
    lang = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('User Review')
        verbose_name_plural = _('User Reviews')

    def __unicode__(self):
        return 'Review from user #%s' % (self.writer,)


class PlaceReview(models.Model):
    """user reviews"""

    writer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='place_reviews_by_you')
    person = models.ForeignKey(User, verbose_name=_('Person'), related_name='place_reviews_about_you')
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    text = models.TextField(_('Review'))
    overall_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    clean_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    comfort_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    location_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    value_money_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    active = models.BooleanField(_('Review visible on the site'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=REVIEW_STATUS, default=1)
    lang = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Place Review')
        verbose_name_plural = _('Place Reviews')

    def __unicode__(self):
        return 'Review from user #%s' % (self.writer,)


