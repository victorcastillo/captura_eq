from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('captura.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^login/', 'login_view'),
    url(r'^agregar_documento/', 'agregar_documento'),
    url(r'^agregar_documento_post/', 'agregar_documento_post'),
    url(r'^autocomplete_materia_utel/', 'autocomplete_materia_utel'),
    url(r'^autocomplete_materias_externas/', 'autocomplete_materias_externas'),
    url(r'^autocomplete_programas_externos/', 'autocomplete_programas_externos'),
    url(r'^agregar_pre_dic/', 'agregar_pre_dic'),
    url(r'^agregar_pre_dic_post/', 'agregar_pre_dic_post'),
    url(r'^buscador/', 'buscador'),
    url(r'^editar_documento/(?P<id_documento>\d+)/', 'editar_documento'),
    url(r'^editar_documento_post/(?P<id_documento>\d+)/', 'editar_documento_post'),
    url(r'^asignar_documento/(?P<id_documento>\d+)/', 'asignar_documento'),
    url(r'^editar_materia/(?P<id_materia>\d+)/', 'editar_materia'),
    url(r'^editar_materia_post/(?P<id_materia>\d+)/', 'editar_materia_post'),
    url(r'^admin/', include(admin.site.urls)),
)
