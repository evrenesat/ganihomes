from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from options import *


class Place(models.Model):
    '''Places'''

    title = models.CharField(_('Place title'), max_length=100)
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES)
    bathrooms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS)
    size = models.IntegerField(_('Size'))
    pets = models.BooleanField(_('Pets'))

    cancellation = models.SmallIntegerField(_('Cancellation rules'), choices=CANCELATION_RULES)
    min_stay = models.SmallIntegerField(_('Minimum number of nights'), choices=MAX_STAY)
    max_stay = models.SmallIntegerField(_('Maximum number of nights'), choices=MIN_STAY)
    manual = models.TextField(_('House manual'))
    rules = models.TextField(_('House rules'))

    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'), decimal_places=2, max_digits=6)

    beds = models.SmallIntegerField(_('Accommodates'), choices=NO_OF_BEDS)
    extra_limit = models.SmallIntegerField(_('Extra charge for more guests than'), choices=NO_OF_BEDS)
    extra_price = models.DecimalField(_('Extra charge per person'), decimal_places=2, max_digits=6,
                                      help_text=_('Each extra person exceeding the number you specified, must pay this extra charge.'))

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
        return '%s' % (self.title,)

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

    host = models.ForeignKey(User,verbose_name=_('Host'), related_name='host')
    guest = models.ForeignKey(User,verbose_name=_('Host'), related_name='guest')
    place = models.ForeignKey(Place,verbose_name=_('Place'))
    reservation = models.ForeignKey(ReservedDates,verbose_name=_('Reservation Dates'))


    start = models.DateField(_('Booking start'))
    end = models.DateField(_('Booking end'))
    summary = models.CharField(_('Summary'), max_length=100 , null=True, blank=True)
    valid = models.BooleanField(_('Valid'))
    status = models.SmallIntegerField(_('Status'), choices=BOOKING_STATUS)
    payment_type = models.SmallIntegerField(_('Payment type'), choices=PAYMENT_TYPES)

    guest_payment = models.DecimalField(_('Total payment for guest'), decimal_places=2, max_digits=6)
    host_earning = models.DecimalField(_('Host\'s earning'), decimal_places=2, max_digits=6)

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
