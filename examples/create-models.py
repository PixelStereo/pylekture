#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.node import Node
from pydular.model import Model
from pydular.parameter import Parameter
from pydular.functions import prop_list
from pydular.application import application_new, applications, applications_export

import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

# create an application
my_app = application_new('My Python App', author='Renaud Rubiano', version='0.1.0')
# create another application
another_app = application_new('Another Py App')
# create a few models
model_1 = my_app.model_new('model.1', priority=2, tags=['init','video'])
model_2 = my_app.model_new('model.2', tags=['lol', 'lal'], priority='-1')
model_3 = another_app.model_new('model.1', tags=['pol', 'pal'], priority='-11')
model_2_bis = model_2.model_new('model.2.bis')
msg = ('BEFORE tags were {tags} and priority was {priority}')
print(msg.format(priority=model_2.priority, tags=model_2.tags))
model_2.priority = 10
model_2.tags = ['toto', 'tata']
msg = ('AFTER tags are {tags} and priority is {priority}')
print(msg.format(priority=model_2.priority, tags=model_2.tags))

pprint(model_2.export())

for app in applications():
	print(app)
	for model in app.models:
		print('    ' + str(model))
the_class = app
print('------------------ PROPERTIES OF AN APPLICATION-------------------------------')
print prop_list(my_app)
print('------------------ PROPERTIES OF A MODEL -------------------------------')
print prop_list(model_1)
print('------------------ EXPORT NAMESPACE -------------------------------')
pprint(applications_export())
