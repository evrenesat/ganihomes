# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Config'
        db.create_table('configuration_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_activation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('host_fee', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('guest_fee', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('nasil_slide_zaman', self.gf('django.db.models.fields.CharField')(default='0', max_length=200)),
            ('iban_countries', self.gf('django.db.models.fields.TextField')()),
            ('trans_langs', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('auto_trans_langs', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('configuration', ['Config'])


    def backwards(self, orm):
        
        # Deleting model 'Config'
        db.delete_table('configuration_config')


    models = {
        'configuration.config': {
            'Meta': {'object_name': 'Config'},
            'auto_trans_langs': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email_activation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guest_fee': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'host_fee': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'iban_countries': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nasil_slide_zaman': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '200'}),
            'trans_langs': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['configuration']
