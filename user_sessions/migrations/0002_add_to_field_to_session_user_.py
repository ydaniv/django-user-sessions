# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings


# Safe User import for Django < 1.5
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
session_user_to_field = getattr(settings, 'USER_SESSIONS_USER_TO_FIELD', None)


class Migration(SchemaMigration):

    def forwards(self, orm):

        if session_user_to_field:
            field_name = 'user_%s' % session_user_to_field

            # Adding the new column
            #TODO: get the field and its attributes dynamically
            db.add_column(u'user_sessions_session', field_name, self.gf('uuidfield.fields.UUIDField')(db_index=True, unique=True, max_length=32, blank=True))

            # Migrating data from old field 'Session.user' to the new one
            users = orm[user_orm_label].objects.all()
            for session in orm['user_sessions.Session'].objects.all():
                try:
                    setattr(session, field_name, getattr(users.get(users.get(id=session.user_id)), session_user_to_field))
                    session.save()
                except:
                    pass

            # Removing old field 'Session.user'
            db.delete_column(u'user_sessions_session', 'user_id')

            # Rename the new field back to `user_id`
            db.rename_column(u'user_sessions_session', field_name, 'user_id')

    def backwards(self, orm):

        # Changing field 'Session.user'
        db.alter_column(u'user_sessions_session', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'], null=True))

    models = {
        u'accounts.account': {
            'Meta': {'ordering': "['email', 'created_on']", 'object_name': 'Account'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user_sessions.session': {
            'Meta': {'object_name': 'Session'},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Account']", 'to_field': "'uuid'", 'null': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['user_sessions']