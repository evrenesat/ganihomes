# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Dil'
        db.delete_table('website_dil')


    def backwards(self, orm):
        
        # Adding model 'Dil'
        db.create_table('website_dil', (
            ('pul', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('kodu', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etkin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('adi', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('website', ['Dil'])


    models = {
        'website.ceviriler': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Ceviriler'},
            'asil': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ceviri': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kelime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Kelime']"}),
            'kod': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.haber': {
            'Meta': {'ordering': "['-sabit', '-pul']", 'object_name': 'Haber'},
            'anahtar_kelime': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'Meta': {'unique_together': "(('dil_kodu', 'sayfa'),)", 'object_name': 'Icerik'},
            'anahtar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'dil_kodu': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gorsel': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sira': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['website']
