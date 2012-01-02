# -*- coding: utf-8 -*-
__author__ = 'Evren Esat Ozkan'

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.utils import simplejson as json
from django.forms.models import ModelForm, ModelChoiceField
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django import http
#from personel.models import Personel, Ileti
#from urun.models import Urun
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from places.countries import OFFICIAL_COUNTRIES_DICT, COUNTRIES_DICT
from places.models import Place, Tag, Photo, Currency
from django.db import DatabaseError
from places.options import n_tuple, PLACE_TYPES
from utils.cache import kes
from website.models.icerik import Sayfa, Haber, Vitrin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from website.models.medya import Medya
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from  django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from django.contrib import auth
from django.contrib import messages
import logging
log = logging.getLogger('genel')



def list_places(request, type=None):
    pls = request.user.place_set.all()
    result = u'[%s]' % u','.join([p for p in pls.values_list('summary', flat=True)])
    return HttpResponse(result, mimetype='application/json')
