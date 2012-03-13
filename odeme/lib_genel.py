# -*-  coding: utf-8 -*-
from string import Template
import urllib2
import re
sonuc_re=re.compile("<ProcReturnCode>(.*?)</ProcReturnCode>")
import logging
log = logging.getLogger('genel')
try:
    from django.conf import settings
    CHECKOUT_SSL = settings.CHECKOUT_SSL
except:
    CHECKOUT_SSL = False
from utils.xml2dict import fromstring
import base64
from hashlib import sha1

import urllib, urllib2
from random import random

class GenelBanka:
    def __init__(self, *args, **kwargs):
        self.kull, self.parola, self.posid  = kwargs.get('bank_data',['','',''])
        self.kull = kwargs.get('kull',self.kull)
        self.parola = kwargs.get('parola',self.parola)
        self.posid = kwargs.get('posid',self.posid)
        self.taksitleri_alabilir=False
        self.altbanka_varmi=False
        self.store_type=''
        self.SSL=CHECKOUT_SSL
        self.islem_tipi = 'PreAuth'
        self.url='https://testsanalpos.est.com.tr/servlet/cc5ApiServer'
        self.secure3d_url='https://testsanalpos.est.com.tr/servlet/est3Dgate'
        #self.url='https://cc5test.est.com.tr/servlet/cc5ApiServer'
        self.url='https://testvpos.est.com.tr/servlet/cc5ApiServer'
        self.uyelik_bilgileri=(
            'API Kullanıcı Adı',
            'API Şifresi',
            'Firma SanalPOS IDsi',
            )
        self.domain=kwargs.get('domain','')
        ssl='s' if self.SSL else ''
        self.okUrl = 'http%s://%s%s' % (ssl, self.domain, kwargs.get('ok_url',''))
        self.failUrl = 'http%s://%s%s' % (ssl, self.domain, kwargs.get('fail_url',''))
        self.rnd=repr(random()).split('.')[1]
        self.taksitSayisi = ''
        #self.banka_bilgileri=(u'kull',u'parola',u'posid')
        self.sablon = {'start':'''DATA=<?xml version=\"1.0\" encoding=\"ISO-8859-9\"?>
        <CC5Request>
        <Name>$kull</Name>
        <Password>$parola</Password>
        <ClientId>$posid</ClientId>
        <IPAddress>$ip</IPAddress>
        <Type>$type</Type>
        <OrderId>$oid</OrderId>''',

        'payment' : '''
        <Number>$cardno</Number>
        <Expires>$skt</Expires>
        <Cvv2Val>$cvc</Cvv2Val>
        <Total>$tutar</Total>
        <Currency>949</Currency>
        <Taksit>$taksit</Taksit>
        ''',


        'secure_3d_payment': '''
            <PayerTxnId>$xid</PayerTxnId>
            <PayerSecurityLevel>$eci</PayerSecurityLevel>
            <PayerAuthenticationCode>$cavv</PayerAuthenticationCode>
            <CardholderPresentCode>13</CardholderPresentCode>''',

        'end':'</CC5Request>',}

    def secure3d(self, ccdata_dict):
        pan=ccdata_dict['pan']
        cv2=ccdata_dict['cv2']
        Ecom_Payment_Card_ExpDate_Year=ccdata_dict['exp_y'][:2]
        Ecom_Payment_Card_ExpDate_Month=ccdata_dict['exp_m']
        cardType='1' if self.cc_type(ccdata_dict['pan']) == 'Visa' else '2'
        oid=str(ccdata_dict['oid'])
        amount=str(ccdata_dict['amount'])



        log.info('OFFF : %s  %s  %s  %s  %s  %s  %s  %s  %s ' % (self.posid, oid, amount, self.okUrl, self.failUrl, self.islemTipi, self.taksitSayisi, self.rnd, self.storekey))
        hashable_data=self.posid+oid+amount+self.okUrl+self.failUrl+self.islemTipi+self.taksitSayisi+self.rnd+self.storekey
        hashed_data=base64.b64encode(sha1(hashable_data).digest())

        data={'storetype':self.store_type, 'storekey':self.store_key,'rnd':self.rnd,'okUrl':self.okUrl,
              'failUrl':self.failUrl,'pan':pan,'cv2':cv2,
              'Ecom_Payment_Card_ExpDate_Year':Ecom_Payment_Card_ExpDate_Year,
              'Ecom_Payment_Card_ExpDate_Month':Ecom_Payment_Card_ExpDate_Month,
              'cardType':cardType,'clientid':self.posid,'oid':oid,'amount':amount,'hash':hashed_data,
              'islemtipi':self.islem_tipi, 'taksit':self.taksitSayisi
        }


        enc_data=urllib.urlencode(data)
        req=urllib2.Request(self.secure3d_url, enc_data)
        resp=urllib2.urlopen(req)
        sonuc=resp.read()

        return sonuc


    def sablon(self, bilgiler):
        sablon = self.sablon['start']
        type = bilgiler['type']
        if type in ['Auth','PreAuth']:
            sablon += self.sablon['payment']
#        elif type == 'PostAuth':
#            pass
        if '3d' in self.store_type and type in ['Auth','PreAuth']:
            sablon += self.sablon['secure_3d_payment']

        sablon += self.sablon['end']
        veri=Template(sablon).substitute(bilgiler)

    def cc_type(self, cc_number):
        """
        Function determines type of CC by the given number.
        """
        AMEX_CC_RE = re.compile(r"^3[47][0-9]{13}$")
        VISA_CC_RE = re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$")
        MASTERCARD_CC_RE = re.compile(r"^5[1-5][0-9]{14}$")
        DISCOVER_CC_RE = re.compile(r"^6(?:011|5[0-9]{2})[0-9]{12}$")

        CC_MAP = {"American Express": AMEX_CC_RE, "Visa": VISA_CC_RE,
                  "Mastercard": MASTERCARD_CC_RE, "Discover": DISCOVER_CC_RE}

        for type, regexp in CC_MAP.items():
            if regexp.match(str(cc_number)):
                return type
        return None


    def bankalari_al(self):
        return [{'name': self.adi,  'bankid':self.id}]

    def cc(self,    bilgiler):
        bilgiler['skt']="%02d/%s" % (int(bilgiler['sktay']), bilgiler['sktyil'][2:]) if bilgiler.get('sktay') else bilgiler.get('skt','')
        if bilgiler.get('taksit',1) in [0, '0', 1, '1']: bilgiler['taksit']=''
        bilgiler.update({'kull':self.kull, 'parola':self.parola, 'posid':self.posid, })
        veri = self.sablon(bilgiler)
        if settings.DEBUG:
            log.info(veri)
        req = urllib2.Request(self.url, veri)
        response = urllib2.urlopen(req)
        sonuc = response.read()
        log.info(sonuc)
        if sonuc:
            sd=fromstring(sonuc)['CC5Response']
            sonuc={
            'authorization_code':sd['AuthCode']and unicode(sd['AuthCode']['value']),
            'reference_code':sd['HostRefNum'] and unicode(sd['HostRefNum']['value']),
            'transaction_id':sd['TransId'] and unicode(sd['TransId']['value']),
            'error_text':sd['ErrMsg'] and unicode(sd['ErrMsg']['value'])
            }
            return sd['Response']['value']=='Approved', sonuc
