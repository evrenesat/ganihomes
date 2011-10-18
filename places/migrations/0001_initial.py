# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transaction'
        db.create_table('places_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('reciver_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('sender_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('places', ['Transaction'])

        # Adding model 'TagCategory'
        db.create_table('places_tagcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['TagCategory'])

        # Adding model 'Tag'
        db.create_table('places_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.TagCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Tag'])

        # Adding model 'Place'
        db.create_table('places_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('emergency_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('space', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('bedroom', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('bed_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('bathrooms', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('pets', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cancellation', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('min_stay', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('max_stay', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('manual', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('weekly_discount', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('monthly_discount', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('extra_limit', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('extra_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('cleaning_fee', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('street_view', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Place'])

        # Adding M2M table for field tags on 'Place'
        db.create_table('places_place_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm['places.place'], null=False)),
            ('tag', models.ForeignKey(orm['places.tag'], null=False))
        ))
        db.create_unique('places_place_tags', ['place_id', 'tag_id'])

        # Adding model 'Profile'
        db.create_table('places_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lastlogin', self.gf('django.db.models.fields.DateTimeField')()),
            ('usr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('brithdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Profile'])

        # Adding M2M table for field favorites on 'Profile'
        db.create_table('places_profile_favorites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['places.profile'], null=False)),
            ('place', models.ForeignKey(orm['places.place'], null=False))
        ))
        db.create_unique('places_profile_favorites', ['profile_id', 'place_id'])

        # Adding model 'Friendship'
        db.create_table('places_friendship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Profile'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('places', ['Friendship'])

        # Adding model 'Photo'
        db.create_table('places_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Place'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Photo'])

        # Adding model 'ReservedDates'
        db.create_table('places_reserveddates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['ReservedDates'])

        # Adding model 'Booking'
        db.create_table('places_booking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='host', to=orm['auth.User'])),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='guest', to=orm['auth.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Place'])),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.ReservedDates'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('payment_type', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('guest_payment', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('host_earning', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Booking'])

        # Adding model 'SessionalPrice'
        db.create_table('places_sessionalprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('weekend_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['SessionalPrice'])

        # Adding model 'Description'
        db.create_table('places_description', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Place'])),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Description'])

        # Adding model 'Message'
        db.create_table('places_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['auth.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['Message'])

        # Adding model 'UserReview'
        db.create_table('places_userreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='writer', to=orm['auth.User'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person', to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['UserReview'])

        # Adding model 'PlaceReview'
        db.create_table('places_placereview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Place'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('rating', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('places', ['PlaceReview'])


    def backwards(self, orm):
        
        # Deleting model 'Transaction'
        db.delete_table('places_transaction')

        # Deleting model 'TagCategory'
        db.delete_table('places_tagcategory')

        # Deleting model 'Tag'
        db.delete_table('places_tag')

        # Deleting model 'Place'
        db.delete_table('places_place')

        # Removing M2M table for field tags on 'Place'
        db.delete_table('places_place_tags')

        # Deleting model 'Profile'
        db.delete_table('places_profile')

        # Removing M2M table for field favorites on 'Profile'
        db.delete_table('places_profile_favorites')

        # Deleting model 'Friendship'
        db.delete_table('places_friendship')

        # Deleting model 'Photo'
        db.delete_table('places_photo')

        # Deleting model 'ReservedDates'
        db.delete_table('places_reserveddates')

        # Deleting model 'Booking'
        db.delete_table('places_booking')

        # Deleting model 'SessionalPrice'
        db.delete_table('places_sessionalprice')

        # Deleting model 'Description'
        db.delete_table('places_description')

        # Deleting model 'Message'
        db.delete_table('places_message')

        # Deleting model 'UserReview'
        db.delete_table('places_userreview')

        # Deleting model 'PlaceReview'
        db.delete_table('places_placereview')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'places.booking': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Booking'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guest'", 'to': "orm['auth.User']"}),
            'guest_payment': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host'", 'to': "orm['auth.User']"}),
            'host_earning': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.ReservedDates']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'places.description': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Description'},
            'auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.friendship': {
            'Meta': {'object_name': 'Friendship'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Profile']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'places.message': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.photo': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.place': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Place'},
            'bathrooms': ('django.db.models.fields.SmallIntegerField', [], {}),
            'bed_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'bedroom': ('django.db.models.fields.SmallIntegerField', [], {}),
            'cancellation': ('django.db.models.fields.SmallIntegerField', [], {}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cleaning_fee': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'extra_limit': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'extra_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'max_stay': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'min_stay': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'monthly_discount': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'space': ('django.db.models.fields.SmallIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'street_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['places.Tag']", 'symmetrical': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'weekly_discount': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'places.placereview': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'PlaceReview'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'places.profile': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Profile'},
            'brithdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'favorites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['places.Place']", 'symmetrical': 'False'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friend_profiles'", 'symmetrical': 'False', 'through': "orm['places.Friendship']", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'lastlogin': ('django.db.models.fields.DateTimeField', [], {}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'usr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'places.reserveddates': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'ReservedDates'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.sessionalprice': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'SessionalPrice'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'weekend_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        },
        'places.tag': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.TagCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.tagcategory': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'TagCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.transaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reciver_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'sender_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'places.userreview': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'UserReview'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['places']
