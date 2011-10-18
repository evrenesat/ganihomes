from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from options import *
from countries import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        currency = Currency.objects.filter(main=True)[0]
        Profile.objects.create(usr=instance, currency=currency)

post_save.connect(create_user_profile, sender=User)

ugettext('Support')
ugettext('Website')
ugettext('Auth')

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

class Currency(models.Model):
    """Currencies """

    name = models.CharField(_('Currency name'), max_length=20)
    code = models.CharField(_('Currency code'), max_length=3)
    factor = models.DecimalField(_('Conversation factor'), decimal_places=2, max_digits=8)
    main = models.BooleanField(_('Main site currency?'), default=False, help_text=_('Main currency is the \
    conversation bridge between other currencies.'))
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


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
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return '%s' % (self.name,)


class Place(models.Model):
    """Places"""


    owner = models.ForeignKey(User, verbose_name=_('Host'))
    tags = models.ManyToManyField(Tag,verbose_name=_('Tags'), null=True, blank=True)
    title = models.CharField(_('Place title'), max_length=100)
    slug = models.SlugField(_('URL Name'))
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    street = models.CharField(_('Street'), max_length=60)
    postcode = models.CharField(_('Postcode'), max_length=15)
    city = models.CharField(_('City'), max_length=40)
    district = models.CharField(_('District'), max_length=40)
    state = models.CharField(_('State/Region'), max_length=40)
    emergency_phone = models.CharField(_('Emergency phone'), max_length=20)
    phone = models.CharField(_('Phone'), max_length=20)
    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)
    capacity = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS)
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES)
    size = models.PositiveIntegerField(_('Size'))
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS)
    size = models.IntegerField(_('Size'))
    cancellation = models.SmallIntegerField(_('Cancellation rules'), choices=CANCELATION_RULES)
    min_stay = models.SmallIntegerField(_('Minimum number of nights'), choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(_('Maximum number of nights'), choices=MAX_STAY, default=0)
    manual = models.TextField(_('House manual'), null=True, blank=True)
    rules = models.TextField(_('House rules'), null=True, blank=True)
    pets = models.BooleanField(_('Pets'), default=False, help_text=_('Pets allowed'))


    weekly_discount = models.SmallIntegerField(_('Weekly discount (%)'), null=True, blank=True)
    monthly_discount = models.SmallIntegerField(_('Monthly discount (%)'), null=True, blank=True)

    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS, null=True, blank=True)
    extra_price = models.DecimalField(_('Extra charge per person'), null=True, blank=True, decimal_places=2, max_digits=6,
                                      help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))
    cleaning_fee = models.DecimalField(_('Cleaning fee'), decimal_places=2, max_digits=8, null=True, blank=True)
    street_view = models.BooleanField(_('Street view'), default=False)

    active = models.BooleanField(_('Place is online'), default=True)
    timestamp = models.DateTimeField(_('Creatation'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

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


class Photo(models.Model):
    """Photos"""
    place = models.ForeignKey(Place,verbose_name=_('Place'))
    name = models.CharField(_('Image name'), max_length=60, null=True, blank=True)
    image = models.ImageField(_('Image File'), upload_to='place_photos')
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return '%s' % (self.name,)


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
        verbose_name = _('ReservedDate')
        verbose_name_plural = _('Reserved Dates')

    def __unicode__(self):
        return '%s - %s' % (self.start,self.end)



class Booking(models.Model):
    """Booking"""

    host = models.ForeignKey(User, verbose_name=_('Host'), related_name='host')
    guest = models.ForeignKey(User, verbose_name=_('Host'), related_name='guest')
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

    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    weekend_price = models.DecimalField(_('Weekly price'), decimal_places=2, max_digits=8, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
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



class Description(models.Model):
    """Place description"""

    place = models.ForeignKey(Place,verbose_name=_('Place'))
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
    rating = models.SmallIntegerField(_('Rating'), choices=PLACE_RATING, default=0)
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
