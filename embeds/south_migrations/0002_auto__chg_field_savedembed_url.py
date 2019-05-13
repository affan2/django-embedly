# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SavedEmbed.url'
        db.alter_column(u'embeds_savedembed', 'url', self.gf('django.db.models.fields.URLField')(max_length=2000))

    def backwards(self, orm):

        # Changing field 'SavedEmbed.url'
        db.alter_column(u'embeds_savedembed', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

    models = {
        u'embeds.savedembed': {
            'Meta': {'unique_together': "(('url', 'maxwidth'),)", 'object_name': 'SavedEmbed'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'maxwidth': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['embeds']