__author__ = 'Evren Esat Ozkan'
from django.utils.translation import ugettext_lazy as _

def n_tuple (n, first=[], last=[]):
    return tuple(first + [(i,i) for i in range(1, n)] + last)

PLACE_TYPES = [
    (1, _('Apartment')),
    (2, _('House')),
    (3, _('Garden House')),
    (4, _('Bed and Breakfast')),
    (5, _('Villa')),
    (6, _('Caravan')),
    (50, _('Office')),
]
LOCATION_TYPES = (
 (25, 'Continent'),
 (19, 'Sport'),
 (8, 'Timezone'),
 (23, 'Sea'),
 (9, 'Island'),
 (3, 'County'),
 (13, 'Colloquial'),
 (21, 'Estate'),
 (7, 'LandFeature'),
 (18, 'HistoricalCounty'),
 (14, 'Drainage'),
 (5, 'Airport'),
 (26, 'Ocean'),
 (17, 'HistoricalTown'),
 (6, 'Country'),
 (16, 'LocalAdmin'),
 (4, 'Town'),
 (12, 'HistoricalState'),
 (15, 'POI'),
 (11, 'Suburb'),
 (22, 'Miscellaneous'),
 (10, 'Zip'),
 (24, 'Supername'),
 (2, 'State'),
 (1, 'PlaceType'),
 (20, 'Zone'))

PROMOTION_TYPES = (
    (1, _('Amount (positive balance)')),
    (2, _('Percentage of bookings which cheaper then ....')),

    )

PHOTO_TYPES = (
    (1, _('Inside of the place')),
    (2, _('View of the place')),
    (3, _('External appearance of the place')),
    (4, _('Around the place')),
    (4, _('Other')),

)
SPACE_TYPES = (
    (1, _('Entire Place')),
    (2, _('Private Room')),
    (3, _('Shared Room')),
)
MTYPES = (
    (1, _('ft')),
    (2, _('mt')),
)



NO_OF_ROOMS = n_tuple(10)
MIN_STAY = n_tuple(7)
MAX_STAY = n_tuple(7, first=[(0,'Unlimited')])
NO_OF_BEDS = n_tuple(20)
PLACE_RATING = n_tuple(6, first=[(0, 'Not rated')])
ORDER = n_tuple(20)



TRANSACTION_TYPES = (
    (1, _('PayPal > System')),
    (2, _('Credit Card > System')),
    (3, _('Bank Transfer > System')),
    (20, _('Guest Account > Host Account')),
    (30, _('System > PayPal')),
    (40, _('System > Credit Card')),
    (50, _('System > Bank Account')),
)

MONEY_NODES = (
    (1, _('PayPal')),
    (2, _('Credit Card')),
    (3, _('Bank')),
    (20, _('Guest')),
    (30, _('Host')),
    (40, _('System Account')),
)

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
    (3, _('Bank Transfer (IBAN)')),
)


BOOKING_STATUS = (
    (1, _('Requested')),
    (2, _('Confirmed')),
    (3, _('Payed')),
    (4, _('Canceled by host')),
    (5, _('Canceled by guest')),
    (6, _('Canceled by staff')),
)


REVIEW_STATUS = (
    (1, _('Waiting for confirmation')),
    (2, _('Confirmed, active')),
    (3, _('Deactived by staff')),
    (4, _('Deleted by reviewer')),
    (5, _('Archived')),
)

INFORM_TYPES = (
    (1, _('Wrong house details')),
    (2, _('Wrong price')),
    (3, _('Malicous activity')),
)

MESSAGE_STATUS = (
    (1, _('Waiting for confirmation')),
    (2, _('Confirmed')),
    (3, _('Deactived by staff')),
    (4, _('Deleted')),
    (5, _('Archived')),
)

LOCALES = (
#('ar_SA', _('Arabic')),
#('bg_BG', _('Bulgarian')),
#('cs_CZ', _('Czech')),
#('da_DK', _('Danish')),
#('de_DE', _('German')),
#('el_GR', _('Greek')),
('en_GB', _('English')),
#('en_US', _('English (United States)')),
#('es_ES', _('Spanish')),
#('fi_FI', _('Finnish')),
#('fr_FR', _('French')),
#('hr_HR', _('Croatian')),
#('hu_HU', _('Hungarian')),
#('it_IT', _('Italian')),
#('iw_IL', _('Hebrew')),
#('ja_JP', _('Japanese')),
#('ko_KR', _('Korean')),
#('nl_NL', _('Dutch')),
#('nn_NO', _('Norwegian')),
#('pl_PL', _('Polish')),
#('pt_BR', _('Portuguese (Brazil)')),
#('pt_PT', _('Portuguese')),
#('ro_RO', _('Romanian')),
#('ru_RU', _('Russian')),
#('sk_SK', _('Slovak')),
#('sv_SE', _('Swedish')),
('tr_TR', _('Turkish')),
#('zh_CN', _('Chinese (China)')),
#('zh_TW', _('Chinese (Taiwan)')),
)

JSTRANS = (
    ('edit_prices',_('Edit Prices')),
    ('edit_place_details',_('Edit Place Details')),
    ('set_availability',_('Set Availability')),
    ('manage_photos',_('Manage Photos')),
    ('successfully_complete',_('Operation succesfully completed.')),
    ('profile_saved',_('Your profile successfully updated.')),
#    ('',_('')),
#    ('',_('')),
#    ('',_('')),
)

from countries import *
