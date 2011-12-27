# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from options import *
from countries import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import simplejson as json
from django.db.models.signals import post_save
from utils.cache import kes
from random import randint
from easy_thumbnails.files import get_thumbnailer
import codecs
import logging
log = logging.getLogger('genel')
from django.utils.translation import activate, force_unicode
import codecs
import options

for code,name in settings.LANGUAGES:
    activate(code)
    fp = codecs.open('%s/js/gh_%s.js' % (settings.STATIC_ROOT,code), 'w', encoding='utf8')
    for o in ['COUNTRIES','SPACE_TYPES','PLACE_TYPES']:
        items = {}
        for c in getattr(options,o):
            items[c[0]]=force_unicode(c[1])
        fp.write(u'%s=%s;'% (o, json.dumps(items,ensure_ascii=False)))
    fp.close()

activate(settings.LANGUAGES[0][0])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        currency = Currency.objects.filter(main=True)
        if currency:
            currency = currency[0]
        else:
            currency = Currency.objects.create(main=True, code='TL', name='TL', factor=1)
        po = Profile.objects.create(user=instance, currency=currency)
        po.photo = po.photo.field.attr_class(po, po.photo.field, 'user_photos/user-256.jpg')
        po.save()

post_save.connect(create_user_profile, sender=User)

#from paypal.standard.ipn.signals import payment_was_successful
from paypal.pro.signals import payment_was_successful

def show_me_the_money(sender, **kwargs):
    log.info('para aktarimi %s'%sender)
payment_was_successful.connect(show_me_the_money)

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


class Currency(models.Model):
    """Currencies """

    name = models.CharField(_('Currency name'), max_length=20)
    code = models.CharField(_('Currency code'), max_length=3)
    code_position = models.SmallIntegerField(_('Currency placement'), default=1,
        choices=((1, _('Prefix')), (2, _('Suffix'))))
    factor = models.DecimalField(_('Conversation factor'), decimal_places=4, max_digits=12, default='0')
    main = models.BooleanField(_('Main site currency?'), default=False, help_text=_('Main currency is the \
    conversation bridge between other currencies.'))
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    def get_factor(self, target_currency_id):
        return Currency.objects.filter(pk=target_currency_id).values_list('factor')[0][0] / self.factor

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
                c.factor = str(r[1])
                if new:
                    c.active = False
                c.save()
            except:
                print r
                raise

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
        return '%s' % (self.code,)


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
    reciver_type = models.SmallIntegerField(_('Receiver type'), choices=MONEY_NODES)
    sender_type = models.SmallIntegerField(_('Sender type'), choices=MONEY_NODES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    active = models.BooleanField(_('Active'), default=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    details = models.TextField(_('Transection details (json serialized dict)'), null=True, blank=True)#readonly

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __unicode__(self):
        return '%s' % (self.amount,)


class Tag(models.Model):
    """Place tags"""

    category = models.ForeignKey(TagCategory)
    name = models.CharField(_('Name'), max_length=30)
    help = models.TextField(_('Help Text'), default='', blank=True)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return '%s' % (self.name,)
    @classmethod
    def _updateCache(cls):

        for code,name in settings.LANGUAGES:
            tags = []
            TAGS_CACHE = kes(code,'tags')
            if code == 'en': #assuming en as the default language
                for d in cls.objects.filter(active=True).values('id','name','help'):
                    tags.append(d)
            else:
                for d in TagTranslation.objects.filter(tag__active=True,lang=code).values('tag_id','translation','help'):
                    tags.append({'id':d['tag_id'],'help':d['help'],'name':d['translation']})
            TAGS_CACHE.s(tags,999999)

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
    primary_photo = models.ImageField(_('Primay photo'), upload_to='place_photos', null=True, blank=True)
    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)
    capacity = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS, default=2)
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES, default=1)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES, default=1)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS, default=1)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES, default=1)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS, default=1)
    size = models.IntegerField(_('Size'), null=True, blank=True)
    size_type = models.IntegerField(_('Measurement type'), choices=MTYPES, default=2)
    cancellation = models.SmallIntegerField(_('Cancellation rules'), choices=CANCELATION_RULES, default=1)
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
    lang = models.CharField(_('Language'), max_length=5, choices=LOCALES)
    #    geocode = models.CharField(_('Geographical Location'), max_length=40, null=True, blank=True)
    lat = models.FloatField(_('Latitude'), default=0.0)
    lon = models.FloatField(_('Longitude'), default=0.0)

    weekly_discount = models.SmallIntegerField(_('Weekly discount (%)'), null=True, blank=True, default=0)
    monthly_discount = models.SmallIntegerField(_('Monthly discount (%)'), null=True, blank=True, default=0)
    weekend_price = models.DecimalField(_('Weekend price'), help_text=_('Price for guest'), decimal_places=2,
        max_digits=6, default='0.0')
    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS, null=True,
        blank=True)
    extra_price = models.DecimalField(_('Extra charge per person'), null=True, blank=True, decimal_places=2,
        max_digits=6,
        help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))
    cleaning_fee = models.DecimalField(_('Cleaning fee'), decimal_places=2, max_digits=8, null=True, blank=True)
    street_view = models.BooleanField(_('Street view'), default=False)

    active = models.BooleanField(_('Place is online'), default=True)
    timestamp = models.DateTimeField(_('Creatation'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    #####JSON CACHES######
    reserved_dates = models.TextField(editable=False, default='')
    prices = models.TextField(editable=False, default='')
    summary = models.TextField(editable=False, default='')
    #    details = models.TextField(editable=False, default='')
    SHORTS = {'id': 'id', 'title': 'tt', 'city': 'ci', 'district': 'di',
              'country': 'co', 'postcode': 'pc','currency_id': 'cid',
              'owner_id': 'oid', 'lat': 'lt', 'lon': 'ln', 'state': 'st',
              'favorite_counter': 'fc', 'overall_rating': 'or',
              'type':'typ', 'space':'spc','price':'prc'
    }

    def _updateSummary(self):
        di = {}
        for k, v in self.SHORTS.items():
            val = getattr(self, k)
            if isinstance(val, Decimal): val = float(val)
            di[v] = val
        self.summary = json.dumps(di, ensure_ascii=False)

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
        tag_ids = self.tags.values_list('id',flat=True)
        tags = []
        for t in kes(lang,'tags').g([]):
            if t['id'] in tag_ids:
                t['class']='hit'
            tags.append(t)
        if not tags and tag_ids:
            Tag._updateCache()
        return tags


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

    def calculateTotalPrice(self, currency_id, start, end, guests):
        factor = self.currency.get_factor(currency_id)
        r = (end + datetime.timedelta(days=1) - start).days
        #FIXME: sezonlu fiyatlar, indirimler ve haftasonlarini yoksaydik
        days = [start + datetime.timedelta(days=i) for i in range(r)]
        total= len(days) * self.price * factor
        paypal_price = round(total,2)
        return {'total': total, 'paypal':paypal_price}

    def createThumbnails(self):
        customThumbnailer(self.primary_photo, self.id, [(120, 100, 's')])

    def save(self, *args, **kwargs):
        self._updatePrices()
        self._updateSummary()
        self.createThumbnails()
        super(Place, self).save(*args, **kwargs)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _(u'Place')
        verbose_name_plural = _(u'Places')

    def __unicode__(self):
        return '%s' % (self.title,)


def customThumbnailer(img, id, opts):
    results = []
    if not img:
        return
    for opt in opts:
        size, name = opt[:2], '%s_%s' % (id, opt[2])
        thumbnail_options = dict(size=size, upscale=True, crop='smart', custom_name=name)
        results.append(get_thumbnailer(img).get_thumbnail(thumbnail_options))
    return results


class Profile(models.Model):
    """User profile"""


    #    usr = models.OneToOneField(User, verbose_name=_('User'), related_name='uusr')
    user = models.OneToOneField(User, verbose_name=_('User'), null=True, blank=True)
    photo = models.ImageField(_('Photo'), upload_to='user_photos', null=True, blank=True)
    favorites = models.ManyToManyField(Place, verbose_name=_('Favorite places'), null=True, blank=True)
    friends = models.ManyToManyField(User, through='Friendship', related_name='friend_profiles')
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'))
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

    def save(self, *args, **kwargs):
        self.update_names()
        super(Profile, self).save(*args, **kwargs)
        self.createThumbnails()

    def update_names(self):
        self.private_name = u"%s %s." % (self.user.first_name, self.user.last_name[0])
        self.full_name = self.user.get_full_name()

    def createThumbnails(self):
        customThumbnailer(self.photo, self.user.id, [(200, 0, 'l'), (0, 30, 's')])

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return 'User #%s' % (self.user_id,)


class Friendship(models.Model):
    """Friendship"""

    profile = models.ForeignKey(Profile)
    user = models.ForeignKey(User)
    confirmed = models.BooleanField(_('Confirmed'), default=False)


class ReservedDates(models.Model):
    """unavailable dates"""

    start = models.DateField(_('Reservation Start'))
    end = models.DateField(_('Reservation End'))
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    # = models.CharField(_(''))
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
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


class Photo(models.Model):
    """Photos"""

    #FIXME : delete actual file on delete

    place = models.ForeignKey(Place, verbose_name=_('Place'), null=True, blank=True)
    name = models.CharField(_('Image name'), max_length=60, null=True, blank=True)
    image = models.ImageField(_('Image File'), upload_to='place_photos')
    type = models.SmallIntegerField(_('Photo type'), choices=PHOTO_TYPES, null=True, blank=True)
    order = models.SmallIntegerField(_('Display order'), default=60)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        #FIXME: order on save
        if self.order == 1 or (self.place and not self.place.primary_photo):
            self.place.primary_photo = self.image
            self.place.save()


class Booking(models.Model):
    """Booking"""

    host = models.ForeignKey(User, verbose_name=_('Host'), related_name='host')
    guest = models.ForeignKey(User, verbose_name=_('Guest'), related_name='guest')
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    reservation = models.ForeignKey(ReservedDates, verbose_name=_('Reservation Dates'))

    start = models.DateField(_('Booking start'))
    end = models.DateField(_('Booking end'))
    summary = models.CharField(_('Summary'), max_length=100, null=True, blank=True)
    valid = models.BooleanField(_('Valid'))
    status = models.SmallIntegerField(_('Status'), choices=BOOKING_STATUS, default=1)
    payment_type = models.SmallIntegerField(_('Payment type'), choices=PAYMENT_TYPES, null=True, blank=True)

    guest_payment = models.DecimalField(_('Total payment for guest'), decimal_places=2, max_digits=8)
    host_earning = models.DecimalField(_('Host\'s earning'), decimal_places=2, max_digits=8)

    # = models.ForeignKey(, verbose_name=_(''))
    # = models.CharField(_(''))
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __unicode__(self):
        return '%s' % (self.summary,)


class SessionalPrice(models.Model):
    """Sessional pricing"""
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    weekend_price = models.DecimalField(_('Weekend price'), decimal_places=2, max_digits=8, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
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
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
        super(SessionalPrice, self).save(*args, **kwargs)
        #        self.place.update_prices()
        self.place.save()


class Description(models.Model):
    """Place description"""

    place = models.ForeignKey(Place, verbose_name=_('Place'), related_name='descriptions')
    lang = models.CharField(_('Language'), max_length=5, choices=LOCALES)
    text = models.TextField(_('Description'))
    auto = models.BooleanField(_('Auto translation'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Description')
        verbose_name_plural = _('Descriptions')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.place_id, self.lang)


class Message(models.Model):
    """user messaging system"""

    sender = models.ForeignKey(User, verbose_name=_('Sender'), related_name='sender')
    receiver = models.ForeignKey(User, verbose_name=_('Receiver'), related_name='receiver')
    text = models.TextField(_('Message'))
    read = models.BooleanField(_('Message was read'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=MESSAGE_STATUS, default=1)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __unicode__(self):
        return 'Message from user #%s' % (self.sender_id,)


class UserReview(models.Model):
    """user reviews"""

    writer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='writer')
    person = models.ForeignKey(User, verbose_name=_('Person'), related_name='person')
    text = models.TextField(_('Review'))
    active = models.BooleanField(_('Review visible on the site'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=REVIEW_STATUS, default=1)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('User Review')
        verbose_name_plural = _('User Reviews')

    def __unicode__(self):
        return 'Message from user #%s' % (self.writer,)


class PlaceReview(models.Model):
    """user reviews"""

    writer = models.ForeignKey(User, verbose_name=_('Reviewer'))
    place = models.ForeignKey(Place, verbose_name=_('Place'))
    text = models.TextField(_('Review'))
    overall_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    clean_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    comfort_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    location_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    value_money_rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
    active = models.BooleanField(_('Review visible on the site'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=REVIEW_STATUS, default=1)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Place Review')
        verbose_name_plural = _('Place Reviews')

    def __unicode__(self):
        return 'Message from user #%s' % (self.writer,)
