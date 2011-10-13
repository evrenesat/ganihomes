__author__ = 'Evren Esat Ozkan'
from django.utils.translation import ugettext_lazy as _

n_tuple = lambda n: tuple([(i,i) for i in range(1, n)])

PLACE_TYPES = (
    (1, _('Apartment')),
    (2, _('House')),
    (3, _('Garden House')),
    (4, _('Bed and Breakfast')),
    (5, _('Villa')),
    (6, _('Caravan')),
)
SPACE_TYPES = (
    (1, _('Entire Place')),
    (2, _('Private Room')),
    (3, _('Shared Room')),
)



NO_OF_ROOMS = n_tuple(10)
MIN_STAY = n_tuple(7)
MAX_STAY = n_tuple(7)
NO_OF_BEDS = n_tuple(20)

BED_TYPES = (
    (1, _('Real bed')),
    (2, _('Bunk beds')),
    (3, _('Waterbed')),
    (4, _('Hammock')),
    (5, _('Couch')),
)

BATHROOM_TYPES = (
    (1, _('Private')),
    (2, _('Shared')),
)

CANCELATION_RULES = (
    (1, _('Flexible')),
    (2, _('Semi-flexible')),
    (3, _('Strict')),
)
PAYMENT_TYPES = (
    (1, _('Credit Card')),
    (2, _('PayPal')),
    (3, _('Bank Transfer')),
)


BOOKING_STATUS = (
    (1, _('Requested')),
    (2, _('Confirmed')),
    (3, _('Payed')),
    (41, _('Canceled (by host)')),
    (42, _('Canceled (by guest)')),
    (43, _('Canceled (by staff)')),
)
