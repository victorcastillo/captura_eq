# -*- coding: utf-8 -*-
from django import forms
from .models import TipoDocto, Cat_Asignatura, Licenciatura
from django.utils.encoding import smart_unicode 
from django.contrib.auth.models import User

class DocumentoForm(forms.Form):
	alumno_prospecto = forms.CharField(required=True, error_messages = {'required': "El nombre del Alumno/Prospecto es requerido."})
	universidad = forms.CharField(required=True, error_messages = {'required': "La universidad es requerida."})
	programa_externo = forms.CharField(required=True, error_messages = {'required': "El programa externo es requerido."})
	programa_utel = forms.ModelChoiceField(required=True,label="Programa UTEL a revalidar", queryset=Licenciatura.objects.filter(habilitada=True, modalidad__id=1), error_messages = {'required': "El programa UTEL es requerido."})
	tipo_docto = forms.ModelChoiceField(required=True, queryset=TipoDocto.objects.filter(habilitado=True), error_messages = {'required': "El tipo de documento es requerido."})
	folio = forms.CharField(required=False)
	municipio = forms.CharField(required=True,error_messages = {'required': "El municipio es requerido."})
	entidad = forms.CharField(required=True,error_messages = {'required': "La entidad es requerida."})
	pais = forms.CharField(required=True,error_messages = {'required': "El país es requerido."})

	def clean(self):
		tipo_docto = self.data['tipo_docto']
		if tipo_docto:
			tipo_docto = TipoDocto.objects.get(id=tipo_docto)
			folio = self.data['folio']
			if tipo_docto.tipo_docto != "Predictamen":
				if (folio is None) or len(folio) == 0:
					self._errors['folio'] = self.error_class([smart_unicode('Cuando es un Dictamen debe proporcionar el folio que viene en el documento.')])
					try:
						del self.cleaned_data['folio']
					except: pass
		return self.cleaned_data

class DetalleDocumentoForm(forms.Form):
	materia_a_revalidar = forms.CharField(required=True, error_messages = {'required': "La Materia externa es requerida."})
	materia_utel = forms.CharField(required=True, error_messages = {'required': "La Materia UTEL es requerida"})
	calificacion = forms.CharField(required=False)

	def clean(self):
		if self.data['materia_utel']			:
			materia = Cat_Asignatura.objects.filter(asignatura = self.data['materia_utel'])
			if not materia:
				self._errors['materia_utel'] = self.error_class([smart_unicode('La materia que usted escribió no esta dentro del catalogo de materias de la UTEL.')])
		return self.cleaned_data

class BuscadorForm(forms.Form):
	# id_doc = forms.CharField(required=False)
	capturista = forms.ModelChoiceField(required=False, queryset=User.objects.all())
	nombre = forms.CharField(required=False)
	tipo_documento = forms.ModelChoiceField(required=False, queryset=TipoDocto.objects.filter(habilitado=True))
