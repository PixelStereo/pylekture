
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pyprojekt
from pyprojekt.application import Application
from pyprojekt.node import Node
from pyprojekt.model import Model
from pyprojekt.parameter import Parameter

import pprint
pp = pprint.PrettyPrinter(indent=4)

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

pp.pprint(Application.export())