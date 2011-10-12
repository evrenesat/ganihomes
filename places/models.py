from django.db import models
from django.utils.translation import ugettext_lazy as _
from options import *


class Places(models.Model):
    '''Places'''

    title = models.CharField(_('Place title'))
    type = models.SmallIntegerField(_('Place type'), choices=PLACE_TYPES)
    space = models.SmallIntegerField(_('Space offered'), choices=SPACE_TYPES)
    bedroom = models.SmallIntegerField(_('Number of bedrooms'), choices=NO_OF_ROOMS)
    bed_type = models.SmallIntegerField(_('Bed type'), choices=BATHROOM_TYPES)
    bathroms = models.SmallIntegerField(_('Number of bathrooms'), choices=NO_OF_ROOMS)
    size = models.IntegerField(_('Size'))
    pets = models.BooleanField(_('Pets'))

    cancelation = models.SmallIntegerField(_('Cancellation rules'), choices=CANCELATION_RULES)
    min_stay = models.SmallIntegerField(_('Minimum number of nights'), choices=MAX_STAY)
    max_stay = models.SmallIntegerField(_('Maximum number of nights'), choices=MIN_STAY)
    manual = models.TextField(_('House manual'))
    rules = models.TextField(_('House rules'))

    price = models.DecimalField(_('Price per night'), help_text=_('Price for guest'))


    # = models.ForeignKey(, verbose_name=_(''))
    # = models.CharField(_(''))
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
    timestamp = models.DateTimeField(_('timestamp'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.title,)
