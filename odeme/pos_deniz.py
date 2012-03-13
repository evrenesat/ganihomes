# -*-  coding: utf-8 -*-


from lib_genel import *





class Banka(GenelBanka): #
    def __init__(self, *args, **kwargs):
        self.adi='DenizBank'
        self.id='DenizBank POS'
        self.store_type='3d'
        GenelBanka.__init__(self, *args, **kwargs)


        self.store_key='123456'






def main():
    veri={'cardno':'4920244920244921',
          'sktyil':'12',
          'sktay':'12',
          'tutar':'10.02',
          'cvc':'001',
          'odemeid':'34'
    }
    sonuc=Banka(['DENIZBANKAPI','DENIZBANK08','800100000']).cc(veri)
    print sonuc

if __name__ == '__main__':
    main()
