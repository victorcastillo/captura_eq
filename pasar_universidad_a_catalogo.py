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


from captura.models import Documento
from django.utils.encoding import smart_str

if __name__ == '__main__':
	_universidades = Documento.objects.all()
	universidades = _universidades.values('id', 'universidad')
	archivo = open('catalogo_universidades.txt', 'w+')
	for universidad in universidades:
		archivo.write(str(universidad['id']) + '|,' + smart_str(universidad['universidad'])  + '\n')
