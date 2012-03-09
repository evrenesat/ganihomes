# -*-  coding: utf-8 -*-

import urllib, urllib2
import base64

from lib_genel import *
from random import random
from hashlib import sha1



class Banka(GenelBanka): #
    def __init__(self, *args, **kwargs):
        self.adi='Halk Bank'
        self.id='Halk Bank POS'
        GenelBanka.__init__(self, *args, **kwargs)
        self.odemeNormal=False
        self.odeme3d=True
        self.url='https://testsanalpos.est.com.tr/servlet/cc5ApiServer'
        self.secure3d_url='https://testsanalpos.est.com.tr/servlet/est3Dgate'
        self.aciklama='Bu modül %s bankasına ait  kredi kartları ile taksitli alış imkanı sağlamaktadır.'%self.adi
        self.storetype='3d'
        self.storekey='123456'
        self.domain=''
        self.rnd=repr(random()).split('.')[1]

#        self.url='https://www.sanalakpos.com/servlet/cc5ApiServer'
    #cc fonksiyonunu burada tanimlayarak
    #GECICI OLARAK AKBANK MODULUNU ISLEVSIZ HALE GETIRDIK
    #ISLEM YAPMADAN TRUE DONDURUYOR
#    def cc(self,*args,**kwds):
#        return True,{            'authorizationcode':'1','referencecode':'1',            'xactID':'', 'error_text':''     }


    def secure3d(self, ccdata_dict):
        ssl='s' if self.SSL else ''
        okUrl='http%s://%s/odeme/3d_ok/'%(ssl,self.domain)
        failUrl='http%s://%s/odeme/3d_fail/'%(ssl,self.domain)
        pan=ccdata_dict['pan']
        cv2=ccdata_dict['cv2']
        Ecom_Payment_Card_ExpDate_Year=ccdata_dict['exp_y'][:2]
        Ecom_Payment_Card_ExpDate_Month=ccdata_dict['exp_m']
        cardType=ccdata_dict['cardType']
        clientid=self.posid
        oid=str(ccdata_dict['oid'])
        amount=ccdata_dict['amount']




        hashable_data=clientid+oid+amount+okUrl+failUrl+self.rnd+self.storekey
        hashed_data=base64.b64encode(sha1(hashable_data).digest())

        data={'storetype':self.storetype, 'storekey':self.storekey,'rnd':self.rnd,'okUrl':okUrl,
              'failUrl':failUrl,'pan':pan,'cv2':cv2,
              'Ecom_Payment_Card_ExpDate_Year':Ecom_Payment_Card_ExpDate_Year,
              'Ecom_Payment_Card_ExpDate_Month':Ecom_Payment_Card_ExpDate_Month,
              'cardType':cardType,'clientid':clientid,'oid':oid,'amount':amount,'hash':hashed_data}


        enc_data=urllib.urlencode(data)
        req=urllib2.Request(self.secure3d_url, enc_data)
        resp=urllib2.urlopen(req)
        sonuc=resp.read()

        return sonuc

    def cc(self, *args, **kwargs):
        args=args[1]
        log.info('cc args:%s'%args)
        ccdata_dict={'pan':args['cardno'],'cv2':args['cvc'],
                            'exp_y':args['sktyil'][:2],'exp_m':args['sktay'],
                            'oid':args['odemeid'], 'amount':args['tutar'],
                            'cardType':'1' if args['type']=='Visa' else '2'
                            }
        secure3d_return=self.secure3d(ccdata_dict)
        return secure3d_return


def main():
    veri={'cardno':'4920244920244921',
          'sktyil':'12',
          'sktay':'12',
          'tutar':'10.02',
          'type':'Visa',
          'cvc':'001',
          'odemeid':'34'
    }
    sonuc=Banka(['DENIZBANKAPI','DENIZBANK08','800100000']).cc(['banka_verisi_gelecek_mi_acaba?'],veri)
    print sonuc

if __name__ == '__main__':
    main()
