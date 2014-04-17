# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def login_view(request):
	if not request.user.is_authenticated():
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/buscador')
		return render(request, 'captura/login.html', {})
	return HttpResponseRedirect('/buscador')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login')


@login_required
def home(request, id_documento):
	from .models import Documento, DetalleDocumento
	try:
		documento_ = Documento.objects.get(id=int(id_documento))
		detalles_documentos = DetalleDocumento.objects.filter(documento=documento_)
	except:
		pass
	return render(request, 'captura/home.html', locals())

@login_required
@require_http_methods(['GET'])
def agregar_documento(request):
	from .forms import DocumentoForm
	formulario = DocumentoForm()
	if request.GET:
		formulario = DocumentoForm(request.GET)
	return render(request, 'captura/agregar_eq.html', locals())


@login_required
@require_http_methods(['POST'])
def agregar_documento_post(request):
	from .forms import DocumentoForm
	import json
	from .models import Documento, LogDocto, ProgramaExterno
	formulario = DocumentoForm(request.POST)
	if formulario.is_valid():
		documento = Documento()
		log_documento = LogDocto()
		busqueda = Documento.objects.filter(alumno_prospecto=formulario.cleaned_data['alumno_prospecto'], tipo_docto=formulario.cleaned_data['tipo_docto'])
		if busqueda:
			response = {'errores': {"error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
			content = json.dumps(response)
			http_response = HttpResponse(content, mimetype='application/json')
			http_response.status_code = 500
			http_response.content = content
			return http_response				
		programa_externo = ProgramaExterno.objects.filter(nombre=formulario.cleaned_data['programa_externo'])
		if programa_externo:
			programa_externo = programa_externo[0]
		else:
			programa_externo = ProgramaExterno.objects.create(nombre=formulario.cleaned_data['programa_externo'])
		documento.capturista = request.user
		documento.universidad = formulario.cleaned_data['universidad']
		documento.alumno_prospecto = formulario.cleaned_data['alumno_prospecto']
		documento.folio = formulario.cleaned_data['folio']
		documento.tipo_docto = formulario.cleaned_data['tipo_docto']
		documento.programa_externo = programa_externo
		documento.save()

		log_documento.log_documento = documento
		log_documento.log_alumno_prospecto = documento.alumno_prospecto
		log_documento.log_folio  = documento.folio
		log_documento.log_programa_externo = documento.programa_externo
		log_documento.log_universidad = documento.universidad
		log_documento.usuario = request.user
		log_documento.log_tipo_docto = documento.tipo_docto
		log_documento.log_fecha = documento.fecha_insert
		log_documento.save()
		return HttpResponse('/documento/' + str(documento.id) + '/')
	else:
		response = {'errores': formulario.errors}
        content = json.dumps(response)
        http_response = HttpResponse(content, mimetype='application/json')
        http_response.status_code = 500
        http_response.content = content
        return http_response

@login_required
@require_http_methods(['GET'])
def editar_documento(request, id_documento):
	from .forms import DocumentoForm
	from .models import Documento
	documento = Documento.objects.get(id=int(id_documento))
	formulario = DocumentoForm({
		'universidad': documento.universidad,
		'programa_externo': documento.programa_externo.nombre,
		'alumno_prospecto': documento.alumno_prospecto,
		'folio': documento.folio,
		'tipo_docto': documento.tipo_docto.id
		})
	return render(request, 'captura/editar_documento.html', locals())

@login_required
@require_http_methods(['POST'])
def editar_documento_post(request, id_documento):
	from .forms import DocumentoForm
	import json
	from .models import Documento, LogDocto, ProgramaExterno
	import datetime
	formulario = DocumentoForm(request.POST)
	if formulario.is_valid():
		documento = Documento.objects.get(id=id_documento)
		log_documento = LogDocto()
		busqueda = Documento.objects.filter(alumno_prospecto=formulario.cleaned_data['alumno_prospecto'], tipo_docto=formulario.cleaned_data['tipo_docto'])
		if busqueda:
			if len(busqueda) == 1:
				if int(busqueda[0].id) != int(id_documento):
					response = {'errores': {"error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
					content = json.dumps(response)
					http_response = HttpResponse(content, mimetype='application/json')
					http_response.status_code = 500
					http_response.content = content
					return http_response
			else:
				response = {'errores': {"error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
				content = json.dumps(response)
				http_response = HttpResponse(content, mimetype='application/json')
				http_response.status_code = 500
				http_response.content = content
				return http_response				
		programa_externo = ProgramaExterno.objects.filter(nombre=formulario.cleaned_data['programa_externo'])
		if programa_externo:
			programa_externo = programa_externo[0]
		else:
			programa_externo = ProgramaExterno.objects.create(nombre=formulario.cleaned_data['programa_externo'])

		documento.universidad = formulario.cleaned_data['universidad']
		documento.alumno_prospecto = formulario.cleaned_data['alumno_prospecto']
		documento.folio = formulario.cleaned_data['folio']
		documento.tipo_docto = formulario.cleaned_data['tipo_docto']
		documento.programa_externo = programa_externo
		documento.fecha_update = datetime.datetime.now()
		documento.save()

		log_documento.log_documento = documento
		log_documento.log_alumno_prospecto = documento.alumno_prospecto
		log_documento.log_folio  = documento.folio
		log_documento.log_programa_externo = documento.programa_externo
		log_documento.log_universidad = documento.universidad
		log_documento.usuario = request.user
		log_documento.log_tipo_docto = documento.tipo_docto
		log_documento.log_fecha = datetime.datetime.now()
		log_documento.save()

		return HttpResponseRedirect('/documento/' + str(id_documento))
	else:
		response = {'errores': formulario.errors}
        content = json.dumps(response)
        http_response = HttpResponse(content, mimetype='application/json')
        http_response.status_code = 500
        http_response.content = content
        return http_response

@login_required
@require_http_methods(['GET'])
def asignar_documento(request, id_documento):
	if int(id_documento) == 0:
		try:
			del request.session['documento_id']
		except:
			pass
	else:
		request.session['documento_id'] = id_documento
	return HttpResponseRedirect('/')

@login_required
@require_http_methods(['GET'])
def agregar_pre_dic(request):
	from .forms import DetalleDocumentoForm
	formulario = DetalleDocumentoForm()
	if request.GET:
		formulario = DetalleDocumentoForm(request.GET)
	return render(request, 'captura/agregar_pre_dic.html', locals())


@login_required
@require_http_methods(['POST'])
def agregar_pre_dic_post(request, id_documento):
	from .forms import DetalleDocumentoForm
	import json
	from .models import DetalleDocumento, LogDetalleDocto, MateriaExterna, Documento, Cat_Asignatura
	formulario = DetalleDocumentoForm(request.POST)
	if formulario.is_valid():
		detalle_documento = DetalleDocumento()
		log_detalle_documento = LogDetalleDocto()
		documento = Documento.objects.get(id=int(id_documento))
		detalle_documento.documento = documento
		detalle_documento.calificacion = formulario.cleaned_data['calificacion']
		materia_externa = MateriaExterna.objects.filter(nombre=formulario.cleaned_data['materia_a_revalidar'])
		if materia_externa:
			materia_externa = materia_externa[0]
		else:
			materia_externa = MateriaExterna.objects.create(nombre=formulario.cleaned_data['materia_a_revalidar'])
		doc_existe = DetalleDocumento.objects.filter(materia_externa=materia_externa, documento=documento)
		if doc_existe:
			response = {'errores': {"error": "Ya existe una Materia con esta combinación de Documento y Materia Externa."}}
			content = json.dumps(response)
			http_response = HttpResponse(content, mimetype='application/json')
			http_response.status_code = 500
			http_response.content = content
			return http_response			
		detalle_documento.materia_externa = materia_externa
		detalle_documento.materia_utel = Cat_Asignatura.objects.get(asignatura=formulario.cleaned_data['materia_utel'])
		detalle_documento.save()

		log_detalle_documento.log_detalle_documento = detalle_documento
		log_detalle_documento.log_materia_utel = detalle_documento.materia_utel
		log_detalle_documento.log_materia_externa = detalle_documento.materia_externa
		log_detalle_documento.log_calificacion = detalle_documento.calificacion
		log_detalle_documento.log_fecha = detalle_documento.fecha_insert
		log_detalle_documento.usuario = request.user
		log_detalle_documento.save()
		
		return HttpResponse()
	else:
		response = {'errores': formulario.errors}
        content = json.dumps(response)
        http_response = HttpResponse(content, mimetype='application/json')
        http_response.status_code = 500
        http_response.content = content
        return http_response


@login_required
@require_http_methods(['GET'])
def editar_materia(request, id_materia):
	from .forms import DetalleDocumentoForm
	from .models import DetalleDocumento
	detalle_documento = DetalleDocumento.objects.get(id=int(id_materia))
	formulario = DetalleDocumentoForm({
		'materia_a_revalidar': detalle_documento.materia_externa.nombre,
		'materia_utel': detalle_documento.materia_utel.asignatura,
		'calificacion': detalle_documento.calificacion
		})
	return render(request, 'captura/editar_materia.html', locals())



@login_required
@require_http_methods(['POST'])
def editar_materia_post(request, id_materia):
	from .forms import DetalleDocumentoForm
	import json
	from .models import LogDetalleDocto, DetalleDocumento, MateriaExterna, Cat_Asignatura
	import datetime
	
	formulario = DetalleDocumentoForm(request.POST)
	if formulario.is_valid():
		detalle_documento = DetalleDocumento.objects.get(id=int(id_materia))
		log_detalle_documento = LogDetalleDocto()
		detalle_documento.calificacion = formulario.cleaned_data['calificacion']
		materia_externa = MateriaExterna.objects.filter(nombre=formulario.cleaned_data['materia_a_revalidar'])
		if materia_externa:
			materia_externa = materia_externa[0]
		else:
			materia_externa = MateriaExterna.objects.create(nombre=formulario.cleaned_data['materia_a_revalidar'])
		
		doc_existe = DetalleDocumento.objects.filter(materia_externa=materia_externa, documento=detalle_documento.documento).values_list('id', flat=True)
		doc_existe = [int(x) for x in doc_existe]
		try:
			doc_existe.remove(int(id_materia))
		except: pass
		if doc_existe:
			response = {'errores': {"error": "Ya existe una Materia con esta combinación de Documento y Materia Externa."}}
			content = json.dumps(response)
			http_response = HttpResponse(content, mimetype='application/json')
			http_response.status_code = 500
			http_response.content = content
			return http_response			
		detalle_documento.materia_externa = materia_externa
		detalle_documento.materia_utel = Cat_Asignatura.objects.get(asignatura=formulario.cleaned_data['materia_utel'])
		detalle_documento.fecha_update = datetime.datetime.now()
		detalle_documento.save()

		log_detalle_documento.log_detalle_documento = detalle_documento
		log_detalle_documento.log_materia_utel = detalle_documento.materia_utel
		log_detalle_documento.log_materia_externa = detalle_documento.materia_externa
		log_detalle_documento.log_calificacion = detalle_documento.calificacion
		log_detalle_documento.log_fecha =detalle_documento.fecha_update
		log_detalle_documento.usuario = request.user
		log_detalle_documento.save()
		
		return HttpResponse()
	else:
		response = {'errores': formulario.errors}
        content = json.dumps(response)
        http_response = HttpResponse(content, mimetype='application/json')
        http_response.status_code = 500
        http_response.content = content
        return http_response

@require_http_methods(['GET'])
def autocomplete_materia_utel(request):
	from .models import Cat_Asignatura
	import json
	materias = Cat_Asignatura.objects.filter(asignatura__contains=request.GET['term']).values_list('asignatura', flat=True)
	_materias = [unicode(x) for x in materias]
	materias_json = json.dumps(_materias)
	return HttpResponse(materias_json, mimetype="application/json")


@require_http_methods(['GET'])
def autocomplete_materias_externas(request):
	from .models import MateriaExterna
	import json
	materias = MateriaExterna.objects.filter(nombre__contains=request.GET['term'], habilitado=True).values_list('nombre', flat=True)
	_materias = [unicode(x) for x in materias]
	materias_json = json.dumps(_materias)
	return HttpResponse(materias_json, mimetype="application/json")


@require_http_methods(['GET'])
def autocomplete_programas_externos(request):
	from .models import ProgramaExterno
	import json
	programas = ProgramaExterno.objects.filter(nombre__contains=request.GET['term'], habilitado=True).values_list('nombre', flat=True)
	_programas = [unicode(x) for x in programas]
	programas_json = json.dumps(_programas)
	return HttpResponse(programas_json, mimetype="application/json")



def buscador(request):
	from .forms import BuscadorForm
	from .models import Documento
	formulario = BuscadorForm()
	parametros = {}
	resultados = []
	if request.GET:
		formulario = BuscadorForm(request.GET)
		if request.GET.has_key('capturista'):
			if len(request.GET['capturista']) != 0:
				parametros['capturista__id'] = int(request.GET['capturista'])
		if request.GET.has_key('nombre'):
			if len(request.GET['nombre']) != 0:
				parametros['alumno_prospecto__contains'] = request.GET['nombre']
		if request.GET.has_key('tipo_documento'):
			if len(request.GET['tipo_documento']) != 0:
				parametros['tipo_docto__id'] = request.GET['tipo_documento']
		resultados = Documento.objects.filter(**parametros)
	return render(request, 'captura/buscador.html', locals())

