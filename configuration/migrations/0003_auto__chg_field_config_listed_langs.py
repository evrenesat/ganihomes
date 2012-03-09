# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Config.listed_langs'
        db.alter_column('configuration_config', 'listed_langs', self.gf('django.db.models.fields.TextField')())


    def backwards(self, orm):
        
        # Changing field 'Config.listed_langs'
        db.alter_column('configuration_config', 'listed_langs', self.gf('django.db.models.fields.CharField')(max_length=250))


    models = {
        'configuration.config': {
            'Meta': {'object_name': 'Config'},
            'auto_trans_langs': ('django.db.models.fields.CharField', [], {'default': "'tr,en,es,fr,de'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email_activation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guest_fee': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'host_fee': ('django.db.models.fields.IntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'iban_countries': ('django.db.models.fields.TextField', [], {'default': "'TR'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed_langs': ('django.db.models.fields.TextField', [], {'default': "'en,English\\ntr,T\\xc3\\xbcrk\\xc3\\xa7e\\nes,Espa\\xc3\\xb1ol\\nde,Deutsch\\nit,Italiano'"}),
            'nasil_slide_zaman': ('django.db.models.fields.CharField', [], {'default': "'1,4,10,20,30,-40,45'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'trans_langs': ('django.db.models.fields.CharField', [], {'default': "'tr,en,es,fr,de'", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']
