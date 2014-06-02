# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import smart_unicode


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
    from .models import Documento, LogDocto, ProgramaExterno, Pais, Entidad, Municipio, Universidad

    formulario = DocumentoForm(request.POST)
    if formulario.is_valid():
        documento = Documento()
        log_documento = LogDocto()
        busqueda = Documento.objects.filter(alumno_prospecto=formulario.cleaned_data['alumno_prospecto'],
                                            tipo_docto=formulario.cleaned_data['tipo_docto'])
        if busqueda:
            response = {
                'errores': {
                    "error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
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

        universidad = Universidad.objects.filter(nombre=formulario.cleaned_data['universidad'])
        if universidad:
            universidad = universidad[0]
        else:
            universidad = Universidad.objects.create(nombre=formulario.cleaned_data['universidad'])

        pais = Pais.objects.filter(pais=formulario.cleaned_data['pais'])
        if pais:
            pais = pais[0]
        else:
            pais = Pais.objects.create(pais=formulario.cleaned_data['pais'])
        entidad = Entidad.objects.filter(entidad=formulario.cleaned_data['entidad'], pais=pais)
        if entidad:
            entidad = entidad[0]
        else:
            entidad = Entidad.objects.create(pais=pais, entidad=formulario.cleaned_data['entidad'])
        municipio = Municipio.objects.filter(municipio=formulario.cleaned_data['municipio'], entidad=entidad)
        if municipio:
            municipio = municipio[0]
        else:
            municipio = Municipio.objects.create(municipio=formulario.cleaned_data['municipio'], entidad=entidad)
        documento.capturista = request.user
        documento.universidad = universidad
        documento.alumno_prospecto = formulario.cleaned_data['alumno_prospecto']
        documento.folio = formulario.cleaned_data['folio']
        documento.tipo_docto = formulario.cleaned_data['tipo_docto']
        documento.programa_externo = programa_externo
        if not formulario.cleaned_data['programa_utel']:
            response = {'errores': {"error":"No hay programa UTEL, ponlo de nuevo, si te vuelve a marcar error dile a Martín o Victor."}}
            content = json.dumps(response)
            http_response = HttpResponse(content, mimetype='application/json')
            http_response.status_code = 500
            http_response.content = content
            return http_response
        documento.programa_utel = formulario.cleaned_data['programa_utel']
        documento.municipio = municipio
        documento.numero_materias = 0
        documento.save()

        log_documento.log_documento = documento
        log_documento.log_alumno_prospecto = documento.alumno_prospecto
        log_documento.log_folio = documento.folio
        log_documento.log_programa_externo = documento.programa_externo
        log_documento.log_universidad = documento.universidad.nombre
        log_documento.usuario = request.user
        log_documento.log_tipo_docto = documento.tipo_docto
        log_documento.log_fecha = documento.fecha_insert
        log_documento.log_programa_utel = documento.programa_utel
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
        'universidad': documento.universidad.nombre,
        'programa_externo': documento.programa_externo.nombre,
        'programa_utel': documento.programa_utel.id if documento.programa_utel else None,
        'alumno_prospecto': documento.alumno_prospecto,
        'folio': documento.folio,
        'tipo_docto': documento.tipo_docto.id,
        'municipio': documento.municipio.municipio,
        'entidad': documento.municipio.entidad.entidad,
        'pais': documento.municipio.entidad.pais.pais
    })
    return render(request, 'captura/editar_documento.html', locals())


@login_required
@require_http_methods(['POST'])
def editar_documento_post(request, id_documento):
    from .forms import DocumentoForm
    import json
    from .models import Documento, LogDocto, ProgramaExterno, Pais, Entidad, Municipio, Universidad
    import datetime

    formulario = DocumentoForm(request.POST)
    if formulario.is_valid():
        try:
            documento = Documento.objects.get(id=id_documento)
            log_documento = LogDocto()
            busqueda = Documento.objects.filter(
                alumno_prospecto=smart_unicode(formulario.cleaned_data['alumno_prospecto']),
                tipo_docto=formulario.cleaned_data['tipo_docto'])
            if busqueda:
                if len(busqueda) == 1:
                    if int(busqueda[0].id) != int(id_documento):
                        response = {'errores': {
                            "error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
                        content = json.dumps(response)
                        http_response = HttpResponse(content, mimetype='application/json')
                        http_response.status_code = 500
                        http_response.content = content
                        return http_response
                else:
                    response = {'errores': {
                        "error": "La combinación de el tipo del documento con el nombre del alumno debe ser único."}}
                    content = json.dumps(response)
                    http_response = HttpResponse(content, mimetype='application/json')
                    http_response.status_code = 500
                    http_response.content = content
                    return http_response
            programa_externo = ProgramaExterno.objects.filter(
                nombre=smart_unicode(formulario.cleaned_data['programa_externo']))
            if programa_externo:
                programa_externo = programa_externo[0]
            else:
                programa_externo = ProgramaExterno.objects.create(
                    nombre=smart_unicode(formulario.cleaned_data['programa_externo']))

            universidad = Universidad.objects.filter(nombre=smart_unicode(formulario.cleaned_data['universidad']))
            if universidad:
                universidad = universidad[0]
            else:
                universidad = Universidad.objects.create(nombre=smart_unicode(formulario.cleaned_data['universidad']))
            pais = Pais.objects.filter(pais=smart_unicode(formulario.cleaned_data['pais']))
            if pais:
                pais = pais[0]
            else:
                pais = Pais.objects.create(pais=smart_unicode(formulario.cleaned_data['pais']))
            entidad = Entidad.objects.filter(entidad=smart_unicode(formulario.cleaned_data['entidad']), pais=pais)
            if entidad:
                entidad = entidad[0]
            else:
                entidad = Entidad.objects.create(pais=pais, entidad=smart_unicode(formulario.cleaned_data['entidad']))
            municipio = Municipio.objects.filter(municipio=smart_unicode(formulario.cleaned_data['municipio']),
                                                 entidad=entidad)
            if municipio:
                municipio = municipio[0]
            else:
                municipio = Municipio.objects.create(municipio=smart_unicode(formulario.cleaned_data['municipio']),
                                                     entidad=entidad)
            documento.universidad = universidad
            documento.alumno_prospecto = smart_unicode(formulario.cleaned_data['alumno_prospecto'])
            documento.folio = formulario.cleaned_data['folio']
            documento.tipo_docto = formulario.cleaned_data['tipo_docto']
            documento.programa_externo = programa_externo
            documento.programa_utel = formulario.cleaned_data['programa_utel']
            documento.fecha_update = datetime.datetime.now()
            documento.municipio = municipio
            documento.save()

            log_documento.log_documento = documento
            log_documento.log_alumno_prospecto = documento.alumno_prospecto
            log_documento.log_folio = documento.folio
            log_documento.log_programa_externo = documento.programa_externo
            log_documento.log_programa_utel = documento.programa_utel
            log_documento.log_universidad = documento.universidad.nombre
            log_documento.usuario = request.user
            log_documento.log_tipo_docto = documento.tipo_docto
            log_documento.log_fecha = datetime.datetime.now()
            log_documento.save()

            return HttpResponseRedirect('/documento/' + str(id_documento))
        except Exception as e:
            print
            e, "error documento_editar_post"
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
    from .models import DetalleDocumento, LogDetalleDocto, MateriaExterna, Documento, Cat_Asignatura, \
        Asignatura_Licenciatura

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
        detalle_documento.materia_externa = materia_externa
        materia_utel = Cat_Asignatura.objects.filter(asignatura=formulario.cleaned_data['materia_utel']).values_list(
            'id', flat=True)
        asig_utel = Asignatura_Licenciatura.objects.filter(licenciatura__modalidad__id=1,
                                                           cat_asignatura__id__in=materia_utel).distinct().values_list(
            'cat_asignatura__id', flat=True)
        _materia_utel = Cat_Asignatura.objects.get(id=asig_utel[0])
        doc_existe = DetalleDocumento.objects.filter(materia_externa=materia_externa, documento=documento,
                                                     materia_utel=_materia_utel)
        if doc_existe:
            response = {'errores': {
                "error": "Ya existe una Materia con esta combinación de Documento-Materia Externa y Materia UTEL."}}
            content = json.dumps(response)
            http_response = HttpResponse(content, mimetype='application/json')
            http_response.status_code = 500
            http_response.content = content
            return http_response
        detalle_documento.materia_utel = _materia_utel
        detalle_documento.save()

        documento.numero_materias = documento.numero_materias + 1
        documento.save()
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
    from .models import LogDetalleDocto, DetalleDocumento, MateriaExterna, Cat_Asignatura, Asignatura_Licenciatura
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

        materia_utel = Cat_Asignatura.objects.filter(asignatura=formulario.cleaned_data['materia_utel']).values_list(
            'id', flat=True)
        asig_utel = Asignatura_Licenciatura.objects.filter(licenciatura__modalidad__id=1,
                                                           cat_asignatura__id__in=materia_utel).distinct().values_list(
            'cat_asignatura__id', flat=True)
        _materia_utel = Cat_Asignatura.objects.get(id=asig_utel[0])
        doc_existe = DetalleDocumento.objects.filter(materia_externa=materia_externa,
                                                     documento=detalle_documento.documento,
                                                     materia_utel=_materia_utel).values_list('id', flat=True)
        doc_existe = [int(x) for x in doc_existe]
        try:
            doc_existe.remove(int(id_materia))
        except:
            pass
        if doc_existe:
            response = {
                'errores': {"error": "Ya existe una Materia con esta combinación de Documento y Materia Externa."}}
            content = json.dumps(response)
            http_response = HttpResponse(content, mimetype='application/json')
            http_response.status_code = 500
            http_response.content = content
            return http_response
        detalle_documento.materia_externa = materia_externa
        detalle_documento.materia_utel = _materia_utel
        detalle_documento.fecha_update = datetime.datetime.now()
        detalle_documento.save()

        log_detalle_documento.log_detalle_documento = detalle_documento
        log_detalle_documento.log_materia_utel = detalle_documento.materia_utel
        log_detalle_documento.log_materia_externa = detalle_documento.materia_externa
        log_detalle_documento.log_calificacion = detalle_documento.calificacion
        log_detalle_documento.log_fecha = detalle_documento.fecha_update
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
    from .models import Cat_Asignatura, Asignatura_Licenciatura
    import json

    materias = Cat_Asignatura.objects.filter(asignatura__istartswith=request.GET['term']).values_list('id', flat=True)
    asig_lic = Asignatura_Licenciatura.objects.filter(licenciatura__modalidad__id=1,
                                                      cat_asignatura__id__in=materias).distinct().values_list(
        'cat_asignatura__asignatura', flat=True)
    _materias = [unicode(x) for x in asig_lic]
    materias_json = json.dumps(_materias)
    return HttpResponse(materias_json, mimetype="application/json")


@require_http_methods(['GET'])
def autocomplete_materias_externas(request):
    from .models import MateriaExterna
    import json

    materias = MateriaExterna.objects.filter(nombre__istartswith=request.GET['term'], habilitado=True).values_list(
        'nombre', flat=True).order_by('nombre')
    _materias = [unicode(x) for x in materias]
    materias_json = json.dumps(_materias)
    return HttpResponse(materias_json, mimetype="application/json")


@require_http_methods(['GET'])
def autocomplete_programas_externos(request):
    from .models import ProgramaExterno
    import json

    programas = ProgramaExterno.objects.filter(nombre__istartswith=request.GET['term'], habilitado=True).values_list(
        'nombre', flat=True)
    _programas = [unicode(x) for x in programas]
    programas_json = json.dumps(_programas)
    return HttpResponse(programas_json, mimetype="application/json")


@require_http_methods(['GET'])
def autocomplete_universidades(request):
    from .models import Universidad
    import json

    unis = Universidad.objects.filter(nombre__istartswith=request.GET['term']).values_list('nombre', flat=True)
    _unis = [unicode(x) for x in unis]
    unis_json = json.dumps(_unis)
    return HttpResponse(unis_json, mimetype="application/json")


def buscador(request):
    from .forms import BuscadorForm
    from .models import Documento

    formulario = BuscadorForm()
    parametros = {}
    resultados = []
    if request.GET:
        caracteristicas_url = []
        formulario = BuscadorForm(request.GET)
        # if request.GET.has_key('id_doc'):
        #     if len(request.GET['id_doc']) != 0:
        #         parametros['id'] = int(request.GET['id_doc'])
        #         caracteristicas_url.append("id_doc=%s" % request.GET['id_doc'])
        if request.GET.has_key('capturista'):
            if len(request.GET['capturista']) != 0:
                parametros['capturista__id'] = int(request.GET['capturista'])
                caracteristicas_url.append("capturista=%s" % request.GET['capturista'])
        if request.GET.has_key('nombre'):
            if len(request.GET['nombre']) != 0:
                parametros['alumno_prospecto__icontains'] = smart_unicode(request.GET['nombre'])
                caracteristicas_url.append("nombre=%s" % smart_unicode(request.GET['nombre']))
        if request.GET.has_key('tipo_documento'):
            if len(request.GET['tipo_documento']) != 0:
                parametros['tipo_docto__id'] = request.GET['tipo_documento']
                caracteristicas_url.append("tipo_documento=%s" % request.GET['tipo_documento'])
        resultados = Documento.objects.filter(**parametros).order_by('id')
        paginator = Paginator(resultados, 20)
        page = request.GET.get('page', 1)
        if caracteristicas_url:
            caracteristicas_url = "&" + '&'.join(caracteristicas_url)
        else:
            caracteristicas_url = ''
        try:
            resultados = paginator.page(page)
        except PageNotAnInteger:
            resultados = paginator.page(1)
        except EmptyPage:
            resultados = paginator.page(1)
    return render(request, 'captura/buscador.html', locals())


def calcular_pronostico(documentos_pronostico):
    from .models import DetalleDocumento, Documento
    import itertools
    import datetime

    fecha = datetime.datetime.now().strftime("%d-%B-%Y")
    suma_todos = 0
    archivo_hoy = open('/opt/django_apps/captura_eq/archivo_' + fecha + '.txt', 'w+')
    archivo_hoy.write(
        'ID DOCUMENTO | FECHA | # Materias del PreDic | # Materias que coincidieron (casos) | Porcentaje \n')
    for docpro in documentos_pronostico:
        doc = Documento.objects.get(id=docpro.id_doc)
        detalles_documento_doc_eliminado = DetalleDocumento.objects.filter(documento=doc).values_list(
            'materia_externa__id', flat=True)
        tupla_ids = tuple(set([int(x) for x in detalles_documento_doc_eliminado]))
        cuenta = len(tupla_ids)
        concuerda = DetalleDocumento.objects.raw("SELECT DISTINCT captura_detalledocumento.id, captura_detalledocumento.materia_externa_id,\
												captura_detalledocumento.materia_utel_id FROM captura_detalledocumento WHERE \
												captura_detalledocumento.materia_externa_id IN %s AND captura_detalledocumento.eliminado=0" % str(
            tupla_ids))
        agrupados = itertools.groupby(list(concuerda), lambda c: c.materia_externa_id)
        suma = len(list(agrupados))
        archivo_hoy.write(str(docpro.id_doc) + "|\t" + fecha + "|\t" + str(cuenta) + "|\t" + str(suma) + "|\t" + str(
            float(suma * 100) / float(cuenta)) + "%\n")
        suma_todos += (float(suma * 100) / float(cuenta))
    archivo_hoy.write(
        "Porcentaje del día %s fue de %s porciento" % (fecha, str(suma_todos / float(len(documentos_pronostico)))))
    nombre = archivo_hoy.name
    archivo_hoy.close()
    return nombre


def calcular_pronostico_xdocumento():
    from .models import DetalleDocumento, Documento
    import itertools
    import datetime

    fecha = datetime.datetime.now().strftime("%d-%B-%Y")
    suma_todos = 0
    documentos = Documento.objects.all()
    for docpro in documentos:
        detalles_documento_doc_eliminado = DetalleDocumento.objects.filter(documento=docpro).values_list(
            'materia_externa__id', flat=True)
        tupla_ids = tuple(set([int(x) for x in detalles_documento_doc_eliminado]))
        cuenta = len(tupla_ids)
        concuerda = DetalleDocumento.objects.filter(materia_externa__id__in=tupla_ids).exclude(documento=docpro)
        agrupados = itertools.groupby(list(concuerda), lambda c: c.materia_externa)
        suma = len(list(agrupados))
        try:
            porcentaje = (float(suma * 100) / float(cuenta))
        except:
            porcentaje = 0
        suma_todos += porcentaje
    archivo_hoy = open('/opt/django_apps/captura_eq/pronostico_por_documento_' + fecha + '.txt', 'w+')
    archivo_hoy.write("Porcentaje del día %s fue de %s porciento" % (fecha, str(suma_todos / float(len(documentos)))))
    nombre = archivo_hoy.name
    archivo_hoy.close()
    print "Finished"
    return nombre

def calcular_pronostico_predictamenes():
    from .models import DetalleDocumento, Documento
    import itertools
    import datetime

    fecha = datetime.datetime.now().strftime("%d-%B-%Y")
    suma_todos = 0
    archivo_hoy = open('/opt/django_apps/captura_eq/pronostico_predictamenes_' + fecha + '.txt', 'w+')
    archivo_hoy.write(
        'ID DOCUMENTO | FECHA | # Materias del PreDic | # Materias que coincidieron (casos) | Porcentaje \n')
    documentos = Documento.objects.filter(tipo_docto__id=2).order_by('id')
    for docpro in documentos:
        detalles_documento_doc_eliminado = DetalleDocumento.objects.filter(documento=docpro).values_list(
            'materia_externa__id', flat=True)
        tupla_ids = tuple(set([int(x) for x in detalles_documento_doc_eliminado]))
        cuenta = len(tupla_ids)
        #concuerda = DetalleDocumento.objects.raw("SELECT DISTINCT captura_detalledocumento.id, captura_detalledocumento.materia_externa_id,\
        #                                       captura_detalledocumento.materia_utel_id FROM captura_detalledocumento WHERE \
        #                                       captura_detalledocumento.materia_externa_id IN %s AND captura_detalledocumento.eliminado=0" % str(
        #   tupla_ids))
        concuerda = DetalleDocumento.objects.filter(materia_externa__id__in=tupla_ids).exclude(documento=docpro)
        agrupados = itertools.groupby(list(concuerda), lambda c: c.materia_externa)
        suma = len(list(agrupados))
        try:
            porcentaje = (float(suma * 100) / float(cuenta))
        except:
            porcentaje = 0
        archivo_hoy.write(str(docpro.id) + "|\t" + fecha + "|\t" + str(cuenta) + "|\t" + str(suma) + "|\t" + str(porcentaje) + "%\n")
        suma_todos += porcentaje
    archivo_hoy.write(
        "Porcentaje del día %s fue de %s porciento" % (fecha, str(suma_todos / float(len(documentos)))))
    nombre = archivo_hoy.name
    archivo_hoy.close()
    return nombre


def sacar_pronostico_equivalencias_hoy(request):
    from captura.models import DocumentosIdsPronostico

    documentos_pronostico = DocumentosIdsPronostico.objects.all()
    nombre_file = calcular_pronostico(documentos_pronostico)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s"' % nombre_file
    response.write(open(nombre_file, 'r').read())
    return response

def sacar_pronostico_equivalencias_hoy_por_documento(request):
    nombre_archivo = calcular_pronostico_xdocumento()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s"' % nombre_archivo
    response.write(open(nombre_archivo, 'r').read())
    return response