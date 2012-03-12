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
    def __init__(self, *args, **kwargs):
        self.kull, self.parola, self.posid  = kwargs.get('bank_data',['','',''])
        self.kull = kwargs.get('kull',self.kull)
        self.parola = kwargs.get('parola',self.parola)
        self.posid = kwargs.get('posid',self.posid)
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
        <UserId></UserId>
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
        <StateProv></StateProv>s
        <PostalCode></PostalCode>
        <Country></Country>
        </ShipTo>
        <Extra></Extra>%s
        </CC5Request>
        '''  % '''
            <PayerTxnId>$xid</PayerTxnId>
            	    <PayerSecurityLevel>$eci</PayerSecurityLevel>
            	    <PayerAuthenticationCode>$cavv</PayerAuthenticationCode>
            	    <CardholderPresentCode>13</CardholderPresentCode>
            	    '''\
        if self.storetype =='3d' else ''


    def cc_type(self, cc_number):
        """
        Function determines type of CC by the given number.

        WARNING:
        Creditcard numbers used in tests are NOT valid credit card numbers.
        You can't buy anything with these. They are random numbers that happen to
        conform to the MOD 10 algorithm!

        >>> # Unable to determine CC type
        >>> print cc_type(1234567812345670)
        None

        >>> # Test 16-Digit Visa
        >>> print cc_type(4716182333661786), cc_type(4916979026116921), cc_type(4532673384076298)
        Visa Visa Visa

        >>> # Test 13-Digit Visa
        >>> print cc_type(4024007141696), cc_type(4539490414748), cc_type(4024007163179)
        Visa Visa Visa

        >>> # Test Mastercard
        >>> print cc_type(5570735810881011), cc_type(5354591576660665), cc_type(5263178835431086)
        Mastercard Mastercard Mastercard

        >>> # Test American Express
        >>> print cc_type(371576372960229), cc_type(344986134771067), cc_type(379061348437448)
        American Express American Express American Express

        >>> # Test Discover
        >>> print cc_type(6011350169121566), cc_type(6011006449605014), cc_type(6011388903339458)
        Discover Discover Discover
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
