# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Documento', fields ['tipo_docto', 'alumno_prospecto']
        db.create_unique('captura_documento', ['tipo_docto_id', 'alumno_prospecto'])


    def backwards(self, orm):
        # Removing unique constraint on 'Documento', fields ['tipo_docto', 'alumno_prospecto']
        db.delete_unique('captura_documento', ['tipo_docto_id', 'alumno_prospecto'])


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
        'captura.asignatura_licenciatura': {
            'Meta': {'object_name': 'Asignatura_Licenciatura', 'db_table': "'registro_asignatura_licenciatura'", 'managed': 'False'},
            'cat_area_mayor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Area_Mayor']", 'null': 'True'}),
            'cat_area_menor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Area_Menor']", 'null': 'True'}),
            'cat_asignatura': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Asignatura']"}),
            'cuatrimestre': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licenciatura': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Licenciatura']"}),
            'oficial': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'captura.cat_area_mayor': {
            'Meta': {'object_name': 'Cat_Area_Mayor', 'db_table': "'registro_cat_area_mayor'", 'managed': 'False'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'area_mayor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '252'}),
            'en_jornada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'captura.cat_area_menor': {
            'Meta': {'object_name': 'Cat_Area_Menor', 'db_table': "'registro_cat_area_menor'", 'managed': 'False'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'area_mayor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Area_Mayor']"}),
            'area_menor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '252'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'captura.cat_asignatura': {
            'Meta': {'object_name': 'Cat_Asignatura', 'db_table': "'registro_cat_asignatura'", 'managed': 'False'},
            'asignatura': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'cat_area_mayor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Area_Mayor']", 'null': 'True'}),
            'cat_area_menor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Area_Menor']", 'null': 'True'}),
            'clave_asignatura': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'captura.clasificacionprograma': {
            'Meta': {'object_name': 'ClasificacionPrograma'},
            'clasificacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'captura.detalledocumento': {
            'Meta': {'unique_together': "(('documento', 'materia_externa'),)", 'object_name': 'DetalleDocumento'},
            'calificacion': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Documento']"}),
            'fecha_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materia_externa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.MateriaExterna']"}),
            'materia_utel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Asignatura']"})
        },
        'captura.documento': {
            'Meta': {'unique_together': "(('tipo_docto', 'alumno_prospecto'),)", 'object_name': 'Documento'},
            'alumno_prospecto': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'capturista': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'fecha_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'programa_externo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.ProgramaExterno']"}),
            'tipo_docto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.TipoDocto']"}),
            'universidad': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'captura.licenciatura': {
            'Meta': {'object_name': 'Licenciatura', 'db_table': "'registro_licenciatura'", 'managed': 'False'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'asignaturas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['captura.Cat_Asignatura']", 'through': "orm['captura.Asignatura_Licenciatura']", 'symmetrical': 'False'}),
            'clave_plan': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'grupo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'habilitada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licenciatura': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'modalidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Modalidad']"})
        },
        'captura.logdetalledocto': {
            'Meta': {'object_name': 'LogDetalleDocto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_calificacion': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'log_detalle_documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.DetalleDocumento']"}),
            'log_fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'log_materia_externa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.MateriaExterna']"}),
            'log_materia_utel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Cat_Asignatura']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'captura.logdocto': {
            'Meta': {'object_name': 'LogDocto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_alumno_prospecto': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'log_documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.Documento']"}),
            'log_fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'log_folio': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'log_programa_externo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.ProgramaExterno']"}),
            'log_tipo_docto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.TipoDocto']"}),
            'log_universidad': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'captura.materiaexterna': {
            'Meta': {'object_name': 'MateriaExterna'},
            'habilitado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'captura.modalidad': {
            'Meta': {'object_name': 'Modalidad', 'db_table': "'registro_modalidad'", 'managed': 'False'},
            'aplica_credencial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aplica_reinscripcion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clave_power_campus': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'contrato': ('django.db.models.fields.TextField', [], {}),
            'hay_periodo_ingreso': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_referencia': ('django.db.models.fields.IntegerField', [], {}),
            'matricula_requerida': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modalidad': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nomenclatura_periodo': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'permite_autoinscripcion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'permite_autoreinscripcion': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'captura.programaexterno': {
            'Meta': {'object_name': 'ProgramaExterno'},
            'clasificacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['captura.ClasificacionPrograma']", 'null': 'True'}),
            'habilitado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.TextField', [], {})
        },
        'captura.tipodocto': {
            'Meta': {'object_name': 'TipoDocto'},
            'habilitado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo_docto': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['captura']