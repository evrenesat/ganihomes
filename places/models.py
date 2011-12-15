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
import codecs
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        currency = Currency.objects.filter(main=True)
        if currency:
            currency = currency[0]
        else:
            currency = Currency.objects.create(main=True, code='TL', name='TL', factor=1)
        Profile.objects.create(usr=instance, currency=currency)

post_save.connect(create_user_profile, sender=User)

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
CURR_CACHE.s(randint(10,100000),999999)
class Currency(models.Model):
    """Currencies """

    name = models.CharField(_('Currency name'), max_length=20)
    code = models.CharField(_('Currency code'), max_length=3)
    code_position = models.SmallIntegerField(_('Currency placement'), default=1, choices=((1,_('Prefix')), (2,_('Suffix'))))
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
                c,new = Currency.objects.get_or_create(name=r[0])
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
                di[c.id] = [str(round(float(c.factor),4)),c.name, c.code, c.code_position]
        f=codecs.open(os.path.join(settings.STATIC_ROOT, "js", u'curr.js'),'w','utf-8')
        f.write(("gh_crc=%s"%json.dumps(di, ensure_ascii=False)).replace(" ",''))
        f.close()


    def __unicode__(self):
        return '%s' % (self.code,)

class PromotionCode(models.Model):
    """Promotion codes """

    code = models.CharField(_('Promotion code'), max_length=10, unique=True)
    type = models.SmallIntegerField(_('Type'), choices=PROMOTION_TYPES)
    puser= models.ForeignKey(User, verbose_name=_('Who used this code'), related_name='used_promotions')
    sender = models.ForeignKey(User, verbose_name=_('Sender/Inviter'), related_name='related_promotions')
    percentage = models.DecimalField(_('Percentage'), decimal_places=2, max_digits=8)
    price = models.DecimalField(_('Promotion Amount'), help_text=_('Discount amount'), decimal_places=2, max_digits=6)
    used = models.BooleanField(_('Used'), default=False)
    active = models.BooleanField(_('Active/Valid'), default=True)
    expiry_date = models.DateField(_('Expiry date'),  null=True, blank=True)
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

    user = models.ForeignKey(User,verbose_name=_('Sender'))
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
    help = models.TextField(_('Help Text'),default='',blank=True)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return '%s' % (self.name,)

class TagTranslation(models.Model):
    """Place description"""

    tag = models.ForeignKey(Tag,verbose_name=_('Tag'), related_name='tags')
    lang = models.CharField(_('Language'), max_length=5, choices=LOCALES)
    translation = models.CharField(_('Translation'),max_length=30)
    help = models.TextField(_('Help Text'),default='',blank=True)
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
     r = (end+datetime.timedelta(days=1)-start).days
     return [start+datetime.timedelta(days=i) for i in range(r)]


class Place(models.Model):
    """Places"""


    owner = models.ForeignKey(User, verbose_name=_('Host'))
    tags = models.ManyToManyField(Tag,verbose_name=_('Tags'), null=True, blank=True)
    title = models.CharField(_('Place title'), max_length=100)
    slug = models.SlugField(_('URL Name'), null=True, blank=True)
    address = models.CharField(_('Address Line'), max_length=100, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    street = models.CharField(_('Street'), max_length=60)
    postcode = models.CharField(_('Postcode'), max_length=15)
    city = models.CharField(_('City'), max_length=40)
    district = models.CharField(_('District'), max_length=40)
    state = models.CharField(_('State/Region'), max_length=40, null=True, blank=True)
    emergency_phone = models.CharField(_('Emergency phone'), max_length=20, null=True, blank=True)
#    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    currency = models.ForeignKey(Currency,verbose_name=_('Currency'))
    primary_photo = models.ImageField(_('Primay photo'), upload_to='place_photos', null=True, blank=True)
    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)
    capacity = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS, default=2)
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES, default=1)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES, default=1)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS, default=1)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES, default=1)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS, default=1)
    size = models.IntegerField(_('Size'), null=True, blank=True)
    size_type = models.IntegerField(_('Measurement type'), choices=MTYPES, default=1)
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
    geocode = models.CharField(_('Geographical Location'), max_length=40, null=True, blank=True)


    weekly_discount = models.SmallIntegerField(_('Weekly discount (%)'), null=True, blank=True, default=0)
    monthly_discount = models.SmallIntegerField(_('Monthly discount (%)'), null=True, blank=True, default=0)
    weekend_price = models.DecimalField(_('Weekend price'), help_text=_('Price for guest'), decimal_places=2, max_digits=6, default=0.0)
    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS, null=True, blank=True)
    extra_price = models.DecimalField(_('Extra charge per person'), null=True, blank=True, decimal_places=2, max_digits=6,
                                      help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))
    cleaning_fee = models.DecimalField(_('Cleaning fee'), decimal_places=2, max_digits=8, null=True, blank=True)
    street_view = models.BooleanField(_('Street view'), default=False)

    active = models.BooleanField(_('Place is online'), default=True)
    timestamp = models.DateTimeField(_('Creatation'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    reserved_dates = models.TextField(editable=False, default='')
    prices = models.TextField(editable=False, default='')

    def get_size(self):
        return mark_safe('%s  %s<sup style="line-height:0;">2</sup>' % (self.size, self.get_size_type_display()) if self.size else '-')

    # [ 0|sessional_prices_list[[startdate, enddate, price, weekendprice]],
    # 1|default_price, 2|weekend_price, 3|currency_id, 4|weekly_discount, 5|monthly_discount,
    #  6|extra_limit, 7|extra_price, 8|cleaning_fee]
    def _update_prices(self):

        di =[float(str(self.price)), float(str(self.weekend_price)), self.currency_id,  self.weekly_discount or 0, self.monthly_discount or 0, self.extra_limit or 0, float(str(self.extra_price or 0)), float(str(self.cleaning_fee or 0))]
        sessions = []
        for sp in self.sessionalprice_set.filter(active=True,end__gte=datetime.datetime.today()):
            sessions.append([sp.start.timetuple()[:3],sp.end.timetuple()[:3],float(str(sp.price or 0)),float(str(sp.weekend_price or 0))])
        di.insert(0,sessions)
        self.prices = json.dumps(di)


    def update_reserved_dates(self):
        ard=[]
        for rd in self.reserveddates_set.filter(end__gte=datetime.datetime.today()):
            r = (rd.end+datetime.timedelta(days=1)-rd.start).days
            ard.extend([int((rd.start+datetime.timedelta(days=i)).strftime('%y%m%d')) for i in range(r)])
        self.reserved_dates =  json.dumps(ard)
        self.save()

    def calculateTotalPrice(self, currency_id, start, end, guests):
        factor = self.currency.get_factor(currency_id)
        r = (end+datetime.timedelta(days=1)-start).days
        #FIXME: sezonlu fiyatlar, indirimler ve haftasonlarini yoksaydik
        days = [start+datetime.timedelta(days=i) for i in range(r)]
        return {'total':len(days) * self.price * factor}


    def save(self, *args, **kwargs):
        self._update_prices()
        super(Place, self).save(*args, **kwargs)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _(u'Place')
        verbose_name_plural = _(u'Places')

    def __unicode__(self):
        return '%s' % (self.title,)

class Profile(models.Model):
    """User profile"""


    usr = models.OneToOneField(User, verbose_name=_('User'))
    photo = models.ImageField(_('Photo'), upload_to='user_photos', null=True, blank=True)
    favorites = models.ManyToManyField(Place, verbose_name=_('Favorite places'))
    friends = models.ManyToManyField(User, through='Friendship', related_name='friend_profiles')
    currency = models.ForeignKey(Currency,verbose_name=_('Currency'))
    city = models.CharField(_('City'), max_length=30)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    cell = models.CharField(_('Cellular Phone'), max_length=20, null=True, blank=True)
    occupation = models.CharField(_('Occupation'), max_length=30, null=True, blank=True)
    twitter = models.CharField(_('Twitter'), max_length=60, null=True, blank=True)
    facebook = models.CharField(_('Facebook'), max_length=60, null=True, blank=True)
    brithdate = models.DateField(_('Brithdate'), null=True, blank=True)
    lastlogin = models.DateTimeField(_('Last login time'), auto_now=True)
    lang = models.CharField(_('Default Language'), max_length=5, choices=LOCALES, default='tr_TR')
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return 'User #%s' % (self.usr_id,)

class Friendship(models.Model):
    """Friendship"""

    profile = models.ForeignKey(Profile)
    user = models.ForeignKey(User)
    confirmed = models.BooleanField(_('Confirmed'), default=False)


class ReservedDates(models.Model):
    """unavailable dates"""

    start = models.DateField(_('Reservation Start'))
    end = models.DateField(_('Reservation End'))
    place = models.ForeignKey(Place,verbose_name=_('Place'))
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
        return '%s - %s' % (self.start,self.end)

    def save(self, *args, **kwargs):
        super(ReservedDates, self).save(*args, **kwargs)
        self.place.update_reserved_dates()


class Photo(models.Model):
    """Photos"""

    #FIXME : delete actual file on delete

    place = models.ForeignKey(Place,verbose_name=_('Place'), null=True, blank=True)
    name = models.CharField(_('Image name'), max_length=60, null=True, blank=True)
    image = models.ImageField(_('Image File'), upload_to='place_photos')
    type = models.SmallIntegerField(_('Photo type'), choices=PHOTO_TYPES, null=True, blank=True)
    order = models.SmallIntegerField(_('Display order'),  default=60)
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
        if self.order==1 or (self.place and not self.place.primary_photo):
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
    summary = models.CharField(_('Summary'), max_length=100 , null=True, blank=True)
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
    place = models.ForeignKey(Place,verbose_name=_('Place'))
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    weekend_price = models.DecimalField(_('Weekend price'), decimal_places=2, max_digits=8,  null=True, blank=True)
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

    place = models.ForeignKey(Place,verbose_name=_('Place'), related_name='descriptions')
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

    sender = models.ForeignKey(User,verbose_name=_('Sender'), related_name='sender')
    receiver = models.ForeignKey(User,verbose_name=_('Receiver'), related_name='receiver')
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

    writer = models.ForeignKey(User,verbose_name=_('Reviewer'), related_name='writer')
    person = models.ForeignKey(User,verbose_name=_('Person'), related_name='person')
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

    writer = models.ForeignKey(User,verbose_name=_('Reviewer'))
    place = models.ForeignKey(Place,verbose_name=_('Place'))
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
