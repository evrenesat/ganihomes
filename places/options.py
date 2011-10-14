__author__ = 'Evren Esat Ozkan'
from django.utils.translation import ugettext_lazy as _

def n_tuple (n, first=[], last=[]):
    return tuple(first + [(i,i) for i in range(1, n)] + last)

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
MAX_STAY = n_tuple(7, first=[(0,'Unlimited')])
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

LOCALES = (
('ar_SA', 'Arabic'),
('bg_BG', 'Bulgarian'),
('cs_CZ', 'Czech'),
('da_DK', 'Danish'),
('de_DE', 'German'),
('el_GR', 'Greek'),
('en_GB', 'English (United Kingdom)'),
('en_US', 'English (United States)'),
('es_ES', 'Spanish'),
('fi_FI', 'Finnish'),
('fr_FR', 'French'),
('hr_HR', 'Croatian'),
('hu_HU', 'Hungarian'),
('it_IT', 'Italian'),
('iw_IL', 'Hebrew'),
('ja_JP', 'Japanese'),
('ko_KR', 'Korean'),
('nl_NL', 'Dutch'),
('nn_NO', 'Norwegian'),
('pl_PL', 'Polish'),
('pt_BR', 'Portuguese (Brazil)'),
('pt_PT', 'Portuguese'),
('ro_RO', 'Romanian'),
('ru_RU', 'Russian'),
('sk_SK', 'Slovak'),
('sv_SE', 'Swedish'),
('tr_TR', 'Turkish'),
('zh_CN', 'Chinese (China)'),
('zh_TW', 'Chinese (Taiwan)'),
)
