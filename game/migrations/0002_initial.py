# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table(u'game_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spaces', self.gf('django.db.models.fields.CharField')(default=u'         ', max_length=9)),
        ))
        db.send_create_signal(u'game', ['Board'])


    def backwards(self, orm):
        # Deleting model 'Board'
        db.delete_table(u'game_board')


    models = {
        u'game.board': {
            'Meta': {'object_name': 'Board'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spaces': ('django.db.models.fields.CharField', [], {'default': "u'         '", 'max_length': '9'})
        }
    }

    complete_apps = ['game']