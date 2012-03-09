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


class GenelBanka:
    def __init__(self, veriler=None):
        if veriler: self.kull, self.parola, self.posid=veriler
        self.taksitleri_alabilir=False
        self.altbanka_varmi=False
        self.SSL=CHECKOUT_SSL
        self.odeme3d=False
        self.odemeNormal=True
        #self.url='https://cc5test.est.com.tr/servlet/cc5ApiServer'
        self.url='https://testvpos.est.com.tr/servlet/cc5ApiServer'
        self.uyelik_bilgileri=(
            'API Kullanıcı Adı',
            'API Şifresi',
            'Firma SanalPOS IDsi',
            )
        #self.aciklama='Bu modül %s adlı bankaya ait kredi kartları için  taksitli satış imkanı sağlamaktadır.' % self.adi
        self.aciklama=''

        #self.banka_bilgileri=(u'kull',u'parola',u'posid')

        self.sablon='''DATA=<?xml version=\"1.0\" encoding=\"ISO-8859-9\"?>
        <CC5Request>
        <Name>$kull</Name>
        <Password>$parola</Password>
        <ClientId>$posid</ClientId>
        <IPAddress>$ip</IPAddress>
        <Email></Email>
        <Mode>P</Mode>
        <OrderId>$oid</OrderId>
        <GroupId></GroupId>
        <TransId></TransId>
        <UserId>$uid</UserId>
        <Type>Auth</Type>
        <Number>$cardno</Number>
        <Expires>$skt</Expires>
        <Cvv2Val>$cvc</Cvv2Val>
        <Total>$tutar</Total>
        <Currency>949</Currency>
        <Taksit>$taksit</Taksit>
        <BillTo>
        <Name></Name>
        <Street1></Street1>
        <Street2></Street2>
        <Street3></Street3>
        <City></City>
        <StateProv></StateProv>
        <PostalCode></PostalCode>
        <Country></Country>
        <Company></Company>
        <TelVoice></TelVoice>
        </BillTo>
        <ShipTo>
        <Name></Name>
        <Street1></Street1>
        <Street2></Street2>
        <Street3></Street3>
        <City></City>
        <StateProv></StateProv>
        <PostalCode></PostalCode>
        <Country></Country>
        </ShipTo>
        <Extra></Extra>
        </CC5Request>'''

    def bankalari_al(self):
        return [{'name': self.adi,  'bankid':self.id}]

    def cc(self, banka_verisi, bilgiler):
        skt=bilgiler['skt']="%02d/%s" % (int(bilgiler['sktay']), bilgiler['sktyil'][2:])
        if bilgiler['taksit'] in [0, '0', 1, '1']: bilgiler['taksit']='' #paynet 0 olmasini bekliyordu, est 1 istiyor.
        bilgiler.update({'kull':self.kull, 'parola':self.parola, 'posid':self.posid, })
        veri=Template(self.sablon).substitute(bilgiler)
        if settings.DEBUG: log.info(veri)
        req = urllib2.Request(self.url, veri)
        response = urllib2.urlopen(req)
        sonuc = response.read()
        log.info(sonuc)
        if sonuc:
            sd=fromstring(sonuc)['CC5Response']
            sonuc={
            'authorizationcode':sd['AuthCode']and unicode(sd['AuthCode']['value']),
            'referencecode':sd['HostRefNum'] and unicode(sd['HostRefNum']['value']),
            'xactID':sd['TransId'] and unicode(sd['TransId']['value']),
            'error_text':sd['ErrMsg'] and unicode(sd['ErrMsg']['value'])
            }
            return sd['Response']['value']=='Approved', sonuc
'''
{'AuthCode': {'value': '123456'},
                 'ErrMsg': {},
                 'Extra': {'NUMCODE': {'value': '00000099999999'},
                           'SETTLEID': {'value': '224'},
                           'TRXDATE': {'value': '20081118 00:06:05'},
                           'value': '\n    '},
                 'GroupId': {'value': '42'},
                 'HostRefNum': {'value': '123456789012'},
                 'OrderId': {'value': '42'},
                 'ProcReturnCode': {'value': '00'},
                 'Response': {'value': 'Approved'},
                 'TransId': {'value': '48b292ba-c3ac-3000-002d-0003ba16ddc0'},
                 'value': '\n  '}}
'''
