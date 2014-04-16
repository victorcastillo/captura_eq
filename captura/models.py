from django.db import models
from django.contrib.auth.models import User


def unicode_user(self):
  return self.first_name + ' ' + self.last_name

User.add_to_class('__unicode__', unicode_user)



class Documento(models.Model):
	capturista = models.ForeignKey(User)
	universidad = models.CharField(max_length=200)
	programa_externo = models.ForeignKey('ProgramaExterno')
	alumno_prospecto = models.CharField(max_length=200)
	tipo_docto = models.ForeignKey('TipoDocto')
	folio = models.CharField(max_length=50, null=True)
	fecha_insert = models.DateTimeField(auto_now_add=True)
	fecha_update = models.DateTimeField(auto_now_add=True)

class LogDocto(models.Model):
	log_documento = models.ForeignKey('Documento')
	log_universidad = models.CharField(max_length=200)
	log_programa_externo = models.ForeignKey('ProgramaExterno')
	log_alumno_prospecto = models.CharField(max_length=200)
	log_tipo_docto = models.ForeignKey('TipoDocto')
	log_folio = models.CharField(max_length=50, null=True)
	log_fecha = models.DateTimeField()
	usuario = models.ForeignKey(User)


class MateriaExterna(models.Model):
	nombre = models.CharField(max_length = 100,unique=True)
	habilitado = models.BooleanField(default=True)


class DetalleDocumento(models.Model):
  documento = models.ForeignKey('Documento')
  materia_externa = models.ForeignKey('MateriaExterna')
  materia_utel = models.ForeignKey('Cat_Asignatura')
  calificacion = models.CharField(max_length=15, null=True)
  fecha_insert = models.DateTimeField(auto_now_add=True)
  fecha_update = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('documento', 'materia_externa')


  # class Meta:
  #   unique_together = ('documento', 'materia_externa')

class LogDetalleDocto(models.Model):
	log_detalle_documento = models.ForeignKey('DetalleDocumento')
	log_materia_externa = models.ForeignKey('MateriaExterna')
	log_materia_utel = models.ForeignKey('Cat_Asignatura')
	log_calificacion = models.CharField(max_length=15, null=True)
	log_fecha = models.DateTimeField()
	usuario = models.ForeignKey(User)


class TipoDocto(models.Model):
	tipo_docto = models.CharField(max_length=20, unique=True)
	habilitado = models.BooleanField(default=True)

	def __unicode__(self):
		return self.tipo_docto

class ProgramaExterno(models.Model):
	nombre = models.TextField()
	habilitado = models.BooleanField(default=True)
	clasificacion = models.ForeignKey('ClasificacionPrograma', null=True)

class ClasificacionPrograma(models.Model):
	clasificacion = models.CharField(max_length=100, unique=True)

class Modalidad(models.Model):
  MOD_LICENCIATURA = 1
  MOD_EC_DIPLOMADO = 2
  MOD_EC_CURSO = 3
  MOD_EC_CERTIFICACION = 4
  MOD_MAESTRIA = 5
  MOD_LICENCIATURA_EJECUTIVA = 6
  MOD_LICENCIATURA_MENTOREO = 7
  MOD_EC_INGLES = 8

  MOD_HE = (MOD_LICENCIATURA, MOD_MAESTRIA, MOD_LICENCIATURA_EJECUTIVA, MOD_LICENCIATURA_MENTOREO)
  MOD_STUDENT = (MOD_EC_DIPLOMADO, MOD_EC_CURSO, MOD_EC_CERTIFICACION)

  modalidad = models.CharField(max_length=100)
  contrato = models.TextField()
  matricula_requerida = models.BooleanField(default=True)
  nomenclatura_periodo = models.CharField(max_length=256)
  aplica_reinscripcion = models.BooleanField(default=False)
  permite_autoinscripcion = models.BooleanField(default=False)
  clave_power_campus = models.CharField(max_length=10, null=True, blank=True)
  long_referencia = models.IntegerField()
  permite_autoreinscripcion = models.BooleanField(default=False)
  # sites = models.ManyToManyField(Site, through='ModalidadSite')
  # metodos_pago = models.ManyToManyField('MetodoPago', through='ModalidadesMetodosPago')
  hay_periodo_ingreso = models.BooleanField(default=False)
  aplica_credencial = models.BooleanField(default=False)
  # objects = ModalidadManager()

  def __unicode__(self):
    return unicode(self.modalidad)

  class Meta:
  	managed=False
  	db_table = 'registro_modalidad'


class Cat_Area_Mayor(models.Model):
  area_mayor = models.CharField(max_length=250)
  abreviatura = models.CharField(max_length=30)
  en_jornada = models.BooleanField(default=False)
  descripcion = models.CharField(max_length=252, default="" )

  class Meta:
  	managed=False
  	db_table = 'registro_cat_area_mayor'


class Cat_Area_Menor( models.Model ):
	area_menor = models.CharField( max_length = 250 )
	abreviatura = models.CharField( max_length = 30 )
	area_mayor = models.ForeignKey( Cat_Area_Mayor )
	descripcion = models.CharField(max_length=252, default="" )

	class Meta:
		managed=False
  		db_table = 'registro_cat_area_menor'


class Cat_Asignatura( models.Model ):
  asignatura = models.CharField(max_length=250)
  descripcion = models.TextField()
  cat_area_menor = models.ForeignKey(Cat_Area_Menor, null=True) #NO SE USA, se agarran los de Asignatura_Licenciatura
  cat_area_mayor = models.ForeignKey(Cat_Area_Mayor, null=True) #NO SE USA, se agarran los de Asignatura_Licenciatura
  clave_asignatura = models.CharField(max_length=15, db_index=True)

  class Meta:
  	managed=False
  	db_table = 'registro_cat_asignatura'


class Licenciatura( models.Model ):
  licenciatura = models.CharField( max_length = 250 )
  abreviatura = models.CharField(max_length=20, blank=True)
  grupo = models.CharField(max_length=50, blank=True)
  clave_plan = models.CharField(max_length=10, db_index=True)
  habilitada = models.BooleanField()
  modalidad = models.ForeignKey(Modalidad)
  asignaturas = models.ManyToManyField('Cat_Asignatura', through='Asignatura_Licenciatura')

  class Meta:
  	managed=False
  	db_table = 'registro_licenciatura'


class Asignatura_Licenciatura( models.Model ):
  licenciatura = models.ForeignKey( Licenciatura)
  cat_asignatura = models.ForeignKey( Cat_Asignatura )
  cuatrimestre = models.IntegerField( max_length = 2 )
  cat_area_menor = models.ForeignKey(Cat_Area_Menor, null=True)
  cat_area_mayor = models.ForeignKey(Cat_Area_Mayor, null=True)
  oficial = models.BooleanField()

  class Meta:
  	managed=False
  	db_table = 'registro_asignatura_licenciatura'

