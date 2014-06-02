#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp, sys

from django.core.management import setup_environ

### INTEGRACION Django
try:
  imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
  sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
  sys.exit(1)

import settings

setup_environ(settings)


from captura.models import Documento, Universidad

if __name__ == '__main__':
	archivo = open('catalogo_universidades.txt', 'r')
	while True:
		id_documento, universidad = archivo.readline().strip().split('|,')
		documento = Documento.objects.get(id=id_documento)
		uni = Universidad.objects.filter(nombre=universidad)
		if not uni:
			uni = Universidad.objects.create(nombre=universidad)
		else:
			uni = uni[0]
		documento.universidad = uni
		documento.save()
