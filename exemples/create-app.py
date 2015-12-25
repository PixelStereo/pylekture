
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

from modular import modular
from modular.modular import Application,Model,Parameter,Node

import pprint

modular.debug = True

print '--Creating an application--'
print '---------------------------'
my_app = Application('My Python App',author='Renaud Rubiano',project='My Project',version='0.1.0')
print 'app-name : ' , my_app.name
print 'app-author : ' , my_app.author
print 'app-project : ' , my_app.project
print 'app-version : ' , my_app.version
print
print '--Creating another App--'
print '------------------------'
another_app = Application('Another Py App')

print Application.export()