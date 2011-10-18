# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dil'
        db.create_table('website_dil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('adi', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('kodu', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('website', ['Dil'])

        # Adding model 'Kelime'
        db.create_table('website_kelime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kelime', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('durum', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('website', ['Kelime'])

        # Adding model 'Ceviriler'
        db.create_table('website_ceviriler', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kelime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Kelime'])),
            ('asil', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('kod', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('dil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Dil'])),
            ('ceviri', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('website', ['Ceviriler'])

        # Adding model 'Medya'
        db.create_table('website_medya', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tip', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True)),
            ('ad', self.gf('django.db.models.fields.CharField')(max_length=185)),
            ('dil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Dil'], null=True, blank=True)),
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sablon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('dosya', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('dil_kodu', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('website', ['Medya'])

        # Adding model 'Sayfa'
        db.create_table('website_sayfa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['website.Sayfa'])),
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sablon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('menude', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sadece_uyeler', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('website', ['Sayfa'])

        # Adding M2M table for field medya on 'Sayfa'
        db.create_table('website_sayfa_medya', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sayfa', models.ForeignKey(orm['website.sayfa'], null=False)),
            ('medya', models.ForeignKey(orm['website.medya'], null=False))
        ))
        db.create_unique('website_sayfa_medya', ['sayfa_id', 'medya_id'])

        # Adding model 'Icerik'
        db.create_table('website_icerik', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Dil'])),
            ('dil_kodu', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('metin', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('baslik', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('menu_baslik', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('tanim', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('anahtar', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('html_baslik', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sayfa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Sayfa'])),
            ('olusturma', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('guncelleme', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('website', ['Icerik'])

        # Adding unique constraint on 'Icerik', fields ['dil', 'sayfa']
        db.create_unique('website_icerik', ['dil_id', 'sayfa_id'])

        # Adding model 'Haber'
        db.create_table('website_haber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Dil'])),
            ('dil_kodu', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('baslik', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('anahtar_kelime', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('tanim', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('icerik', self.gf('tinymce.models.HTMLField')()),
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('son_guncelleme', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sabit', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('website', ['Haber'])

        # Adding M2M table for field medya on 'Haber'
        db.create_table('website_haber_medya', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('haber', models.ForeignKey(orm['website.haber'], null=False)),
            ('medya', models.ForeignKey(orm['website.medya'], null=False))
        ))
        db.create_unique('website_haber_medya', ['haber_id', 'medya_id'])

        # Adding model 'Vitrin'
        db.create_table('website_vitrin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('banner', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('dil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Dil'], null=True, blank=True)),
            ('dil_kodu', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=5, null=True, blank=True)),
            ('gorsel', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sira', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True)),
        ))
        db.send_create_signal('website', ['Vitrin'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Icerik', fields ['dil', 'sayfa']
        db.delete_unique('website_icerik', ['dil_id', 'sayfa_id'])

        # Deleting model 'Dil'
        db.delete_table('website_dil')

        # Deleting model 'Kelime'
        db.delete_table('website_kelime')

        # Deleting model 'Ceviriler'
        db.delete_table('website_ceviriler')

        # Deleting model 'Medya'
        db.delete_table('website_medya')

        # Deleting model 'Sayfa'
        db.delete_table('website_sayfa')

        # Removing M2M table for field medya on 'Sayfa'
        db.delete_table('website_sayfa_medya')

        # Deleting model 'Icerik'
        db.delete_table('website_icerik')

        # Deleting model 'Haber'
        db.delete_table('website_haber')

        # Removing M2M table for field medya on 'Haber'
        db.delete_table('website_haber_medya')

        # Deleting model 'Vitrin'
        db.delete_table('website_vitrin')


    models = {
        'website.ceviriler': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Ceviriler'},
            'asil': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ceviri': ('django.db.models.fields.TextField', [], {}),
            'dil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Dil']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kelime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Kelime']"}),
            'kod': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.dil': {
            'Meta': {'object_name': 'Dil'},
            'adi': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kodu': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.haber': {
            'Meta': {'ordering': "['-sabit', '-pul']", 'object_name': 'Haber'},
            'anahtar_kelime': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Dil']"}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icerik': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medya': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Medya']", 'null': 'True', 'blank': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sabit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'son_guncelleme': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'tanim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'website.icerik': {
            'Meta': {'unique_together': "(('dil', 'sayfa'),)", 'object_name': 'Icerik'},
            'anahtar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Dil']"}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'guncelleme': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'html_baslik': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_baslik': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metin': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'olusturma': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sayfa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Sayfa']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'tanim': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'website.kelime': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Kelime'},
            'durum': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kelime': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.medya': {
            'Meta': {'object_name': 'Medya'},
            'ad': ('django.db.models.fields.CharField', [], {'max_length': '185'}),
            'dil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Dil']", 'null': 'True', 'blank': 'True'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'dosya': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sablon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'})
        },
        'website.sayfa': {
            'Meta': {'object_name': 'Sayfa'},
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'medya': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Medya']", 'null': 'True', 'blank': 'True'}),
            'menude': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['website.Sayfa']"}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sablon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sadece_uyeler': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'website.vitrin': {
            'Meta': {'ordering': "['sira']", 'object_name': 'Vitrin'},
            'banner': ('django.db.models.fields.SmallIntegerField', [], {}),
            'dil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Dil']", 'null': 'True', 'blank': 'True'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gorsel': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sira': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['website']
