# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SavedEmbed'
        db.create_table('embeds_savedembed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('maxwidth', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('embeds', ['SavedEmbed'])

        # Adding unique constraint on 'SavedEmbed', fields ['url', 'maxwidth']
        db.create_unique('embeds_savedembed', ['url', 'maxwidth'])

    def backwards(self, orm):
        # Removing unique constraint on 'SavedEmbed', fields ['url', 'maxwidth']
        db.delete_unique('embeds_savedembed', ['url', 'maxwidth'])

        # Deleting model 'SavedEmbed'
        db.delete_table('embeds_savedembed')

    models = {
        'embeds.savedembed': {
            'Meta': {'unique_together': "(('url', 'maxwidth'),)", 'object_name': 'SavedEmbed'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'maxwidth': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['embeds']
