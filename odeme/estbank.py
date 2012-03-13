# -*-  coding: utf-8 -*-
from string import Template
import urllib2
import re
sonuc_re=re.compile("<ProcReturnCode>(.*?)</ProcReturnCode>")
import logging
log = logging.getLogger('genel')
#try:
#    from django.conf import settings
#    CHECKOUT_SSL = settings.CHECKOUT_SSL
#except:
#    CHECKOUT_SSL = False
from utils.xml2dict import fromstring
import base64
from hashlib import sha1

import urllib, urllib2
from random import random

class ESTBank:
    def __init__(self, *args, **kwargs):
        self.store_key, self.kull, self.parola, self.posid  = kwargs.get('bank_data',['123456','','',''])
        self.kull = kwargs.get('kull',self.kull)
        self.parola = kwargs.get('parola',self.parola)
        self.posid = kwargs.get('posid',self.posid)
        self.store_key = kwargs.get('store_key',self.store_key)

        self.store_type= kwargs.get('store_type','3d')
        self.islem_tipi = kwargs.get('islem_tipi','PreAuth')

        self.SSL=kwargs.get('ssl')
        self.url=kwargs.get('url','https://testsanalpos.est.com.tr/servlet/cc5ApiServer')
        self.secure3d_url=kwargs.get('secure3d_url','https://testsanalpos.est.com.tr/servlet/est3Dgate')
        self.domain=kwargs.get('domain','')
        self.taksit_sayisi=kwargs.get('taksit_sayisi','')

        ssl='s' if self.SSL else ''
        self.okUrl = 'http%s://%s%s' % (ssl, self.domain, kwargs.get('ok_url',''))
        self.failUrl = 'http%s://%s%s' % (ssl, self.domain, kwargs.get('fail_url',''))

        self.rnd=repr(random()).split('.')[1]


        self.sablon = {'start':'''DATA=<?xml version=\"1.0\" encoding=\"ISO-8859-9\"?>
        <CC5Request>
        <Name>$kull</Name>
        <Password>$parola</Password>
        <ClientId>$posid</ClientId>
        <Type>$type</Type>
        <OrderId>$oid</OrderId>''',

        'payment' : '''
        <IPAddress>$ip</IPAddress>
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

    def secure3d_request(self, ccdata_dict):
        cardType='1' if self.cc_type(ccdata_dict['pan']) == 'Visa' else '2'
        oid=str(ccdata_dict['oid'])
        amount=str(ccdata_dict['amount'])

        log.info('secure3d rq : %s  %s  %s  %s  %s  %s  %s  %s  %s ' % (
            self.posid, oid, amount, self.okUrl, self.failUrl, self.islem_tipi,
            self.taksit_sayisi, self.rnd, self.store_key))

        hashable_data=self.posid+oid+amount+self.okUrl+self.failUrl+self.islem_tipi+self.taksit_sayisi+self.rnd+self.store_key
        hashed_data=base64.b64encode(sha1(hashable_data).digest())

        data={'storetype':self.store_type, 'storekey':self.store_key,'rnd':self.rnd,'okUrl':self.okUrl,
              'failUrl':self.failUrl,'pan':ccdata_dict['pan'],'cv2':ccdata_dict['cv2'],
              'Ecom_Payment_Card_ExpDate_Year':ccdata_dict['exp_y'][:2],
              'Ecom_Payment_Card_ExpDate_Month':ccdata_dict['exp_m'],
              'cardType':cardType,'clientid':self.posid,'oid':oid,'amount':amount,'hash':hashed_data,
              'islemtipi':self.islem_tipi, 'taksit':self.taksit_sayisi
        }
        enc_data=urllib.urlencode(data)
        req=urllib2.Request(self.secure3d_url, enc_data)
        resp=urllib2.urlopen(req)
        sonuc=resp.read()
        log.info('s3d sonuc: %s' % sonuc)
        return sonuc


    def sablon_yap(self, bilgiler):
        sablon = self.sablon['start']
        type = bilgiler['type']
        if type in ['Auth','PreAuth']:
            sablon += self.sablon['payment']
#        elif type == 'PostAuth':
#            pass
        if '3d' in self.store_type and type in ['Auth','PreAuth']:
            sablon += self.sablon['secure_3d_payment']

        sablon += self.sablon['end']
        return Template(sablon).substitute(bilgiler)

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


    def bilgi_duzenle(self, bilgiler):

        if bilgiler.get('sktay'):
            bilgiler['skt'] = "%02d/%s" % (int(bilgiler['sktay']), bilgiler['sktyil'][2:])
        else:
            bilgiler['skt'] = bilgiler.get('skt','')

        if bilgiler.get('taksit',1) in [0, '0', 1, '1']:
            bilgiler['taksit']=''

        bilgiler.update({'kull':self.kull, 'parola':self.parola, 'posid':self.posid, })
        return bilgiler

    def request(self,    bilgiler):
        bilgiler = self.bilgi_duzenle(bilgiler)
        veri = self.sablon_yap(bilgiler)
        log.info(veri)
        req = urllib2.Request(self.url, veri)
        response = urllib2.urlopen(req)
        xml_sonuc = response.read()
        log.info(xml_sonuc)
        if xml_sonuc:
            sd=fromstring(xml_sonuc)['CC5Response']
            sonuc={
            'authorization_code':sd['AuthCode']and unicode(sd['AuthCode']['value']),
            'reference_code':sd['HostRefNum'] and unicode(sd['HostRefNum']['value']),
            'transaction_id':sd['TransId'] and unicode(sd['TransId']['value']),
            'error_text':sd['ErrMsg'] and unicode(sd['ErrMsg']['value'])
            }
            return sd['Response']['value']=='Approved', sonuc, xml_sonuc
