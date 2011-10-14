from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from options import *
from countries import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Transaction(models.Model):
    '''money transactions'''

    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=8)
    type = models.SmallIntegerField(_('Type'), choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    details = models.TextField(_('Transection details (json serialized dict)'), null=True, blank=True)#readonly

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.amount,)


class TagCategory(models.Model):
    '''Tag category'''

    name = models.CharField(_('Name'), max_length=30)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.name,)


class Tag(models.Model):
    '''Place tags'''

    category = models.ForeignKey(TagCategory)
    name = models.CharField(_('Name'), max_length=30)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.name,)


class Place(models.Model):
    '''Places'''


    owner = models.ForeignKey(User, verbose_name=_('Host'))
    tags = models.ManyToManyField(Tag,verbose_name=_('Tags'))
    title = models.CharField(_('Place title'), max_length=100)
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    street = models.CharField(_('Street'), max_length=60)
    postcode = models.CharField(_('Postcode'), max_length=15)
    city = models.CharField(_('City'), max_length=40)
    district = models.CharField(_('District'), max_length=40)
    state = models.CharField(_('State/Region'), max_length=40)
    emergency_phone = models.CharField(_('Emergency phone'), max_length=20)
    phone = models.CharField(_('Phone'), max_length=20)


    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS)
    size = models.IntegerField(_('Size'))
    pets = models.BooleanField(_('Pets'))

    cancellation = models.SmallIntegerField(_('Cancellation rules'), choices=CANCELATION_RULES)
    min_stay = models.SmallIntegerField(_('Minimum number of nights'), choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(_('Maximum number of nights'), choices=MAX_STAY, default=0)
    manual = models.TextField(_('House manual'), null=True, blank=True)
    rules = models.TextField(_('House rules'), null=True, blank=True)

    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)
    weekly_discount = models.SmallIntegerField(_('Weekly discount (%)'), null=True, blank=True)
    monthly_discount = models.SmallIntegerField(_('Monthly discount (%)'), null=True, blank=True)
    capacity = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS)
    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS, null=True, blank=True)
    extra_price = models.DecimalField(_('Extra charge per person'), null=True, blank=True, decimal_places=2, max_digits=6,
                                      help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))
    cleaning_fee = models.DecimalField(_('Cleaning fee'), decimal_places=2, max_digits=8, null=True, blank=True)
    street_view = models.BooleanField(_('Street view'), default=False)


    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.title,)

class Profile(models.Model):
    '''User profile'''

    usr = models.OneToOneField(User, verbose_name=_('User'))
    favorites = models.ManyToManyField(Place, verbose_name=_('Favorite places'))
    friends = models.ManyToManyField(User, through='Friendship', related_name='friend_profiles')
    city = models.CharField(_('City'), max_length=30)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    cell = models.CharField(_('Cellular Phone'), max_length=20, null=True, blank=True)
    occupation = models.CharField(_('Occupation'), max_length=30, null=True, blank=True)
    twitter = models.CharField(_('Twitter'), max_length=60, null=True, blank=True)
    facebook = models.CharField(_('Facebook'), max_length=60, null=True, blank=True)
    brithdate = models.DateField(_('Brithdate'), null=True, blank=True)
    lastlogin = models.DateTimeField(_('Last login time'), auto_created=True)
    lang = models.CharField(_('Default Language'), max_length=5, choices=LOCALES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return 'User #%s' % (self.user_id,)

class Friendship(models.Model):
    '''Friendship'''

    profile = models.ForeignKey(Profile)
    user = models.ForeignKey(User)
    confirmed = models.BooleanField(_('Confirmed'), default=False)


class Photo(models.Model):
    '''Photos'''
    place = models.ForeignKey(Place,verbose_name=_('Place'))
    name = models.CharField(_('Image name'), max_length=60, null=True, blank=True)
    image = models.ImageField(_('Image File'), upload_to='place_photos')
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.name,)


class ReservedDates(models.Model):
    '''unavailable dates'''

    start = models.DateField(_('Reservation Start'))
    end = models.DateField(_('Reservation End'))
    # = models.ForeignKey(, verbose_name=_(''))
    # = models.CharField(_(''))
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s - %s' % (self.start,self.end)



class Booking(models.Model):
    '''Booking'''

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
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.summary,)


class SessionalPrice(models.Model):
    '''Sessional pricing'''

    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    weekend_price = models.DecimalField(_('Weekly price'), decimal_places=2, max_digits=8, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
    start = models.DateField(_('Session start'))
    end = models.DateField(_('Session end'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.name,)



class Description(models.Model):
    '''Place description'''

    place = models.ForeignKey(Place,verbose_name=_('Place'))
    lang = models.CharField(_('Language'), max_length=5, choices=LOCALES)
    text = models.TextField(_('Description'))
    auto = models.BooleanField(_('Auto translation'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.place_id, self.lang)



class Message(models.Model):
    '''user messaging system'''

    sender = models.ForeignKey(User,verbose_name=_('Sender'), related_name='sender')
    receiver = models.ForeignKey(User,verbose_name=_('Receiver'), related_name='receiver')
    text = models.TextField(_('Message'))
    read = models.BooleanField(_('Message was read'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=MESSAGE_STATUS, default=1)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return 'Message from user #%s' % (self.sender_id,)


class UserReview(models.Model):
    '''user reviews'''

    writer = models.ForeignKey(User,verbose_name=_('Reviewer'), related_name='writer')
    person = models.ForeignKey(User,verbose_name=_('Person'), related_name='person')
    text = models.TextField(_('Review'))
    active = models.BooleanField(_('Review visible on the site'), default=False)
    status = models.SmallIntegerField(_('Status'), choices=REVIEW_STATUS, default=1)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return 'Message from user #%s' % (self.sender_id,)


class PlaceReview(models.Model):
    '''user reviews'''

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
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return 'Message from user #%s' % (self.sender_id,)
