# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Config.listed_langs'
        db.add_column('configuration_config', 'listed_langs', self.gf('django.db.models.fields.CharField')(default='en,English\ntr,T\xc3\xbcrk\xc3\xa7e\nes,Espa\xc3\xb1ol\nde,Deutsch\nit,Italiano', max_length=250), keep_default=False)

        # Changing field 'Config.nasil_slide_zaman'
        db.alter_column('configuration_config', 'nasil_slide_zaman', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Config.host_fee'
        db.alter_column('configuration_config', 'host_fee', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Config.guest_fee'
        db.alter_column('configuration_config', 'guest_fee', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Config.auto_trans_langs'
        db.alter_column('configuration_config', 'auto_trans_langs', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Config.trans_langs'
        db.alter_column('configuration_config', 'trans_langs', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Config.iban_countries'
        db.alter_column('configuration_config', 'iban_countries', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Deleting field 'Config.listed_langs'
        db.delete_column('configuration_config', 'listed_langs')

        # Changing field 'Config.nasil_slide_zaman'
        db.alter_column('configuration_config', 'nasil_slide_zaman', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Config.host_fee'
        db.alter_column('configuration_config', 'host_fee', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Config.guest_fee'
        db.alter_column('configuration_config', 'guest_fee', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'Config.auto_trans_langs'
        raise RuntimeError("Cannot reverse this migration. 'Config.auto_trans_langs' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Config.trans_langs'
        raise RuntimeError("Cannot reverse this migration. 'Config.trans_langs' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Config.iban_countries'
        raise RuntimeError("Cannot reverse this migration. 'Config.iban_countries' and its values cannot be restored.")


    models = {
        'configuration.config': {
            'Meta': {'object_name': 'Config'},
            'auto_trans_langs': ('django.db.models.fields.CharField', [], {'default': "'tr,en,es,fr,de'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email_activation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guest_fee': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'host_fee': ('django.db.models.fields.IntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'iban_countries': ('django.db.models.fields.TextField', [], {'default': "'TR'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed_langs': ('django.db.models.fields.CharField', [], {'default': "'en,English\\ntr,T\\xc3\\xbcrk\\xc3\\xa7e\\nes,Espa\\xc3\\xb1ol\\nde,Deutsch\\nit,Italiano'", 'max_length': '250'}),
            'nasil_slide_zaman': ('django.db.models.fields.CharField', [], {'default': "'1,4,10,20,30,-40,45'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'trans_langs': ('django.db.models.fields.CharField', [], {'default': "'tr,en,es,fr,de'", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']
