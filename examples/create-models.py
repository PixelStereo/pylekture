#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.node import Node
from pydular.model import Model
from pydular.parameter import Parameter
from pydular.application import application_new, applications

import pprint

# create an application
my_app = application_new('My Python App', author='Renaud Rubiano', version='0.1.0')
# create another application
another_app = application_new('Another Py App')
# create a node 
node_1 = my_app.node_new('node.1', priority=-1, tags=['uno','dos'])
node_2 = my_app.node_new('node.2', priority=10, tags=['lol','video'])
# create a few models
model_1 = my_app.model_new('model.1', priority=2, tags=['init','video'])
model_2 = my_app.model_new('model.2', tags=['lol', 'lal'], priority='-1')
model_3 = another_app.model_new('model.1', tags=['pol', 'pal'], priority='-11')
msg = ('BEFORE tags were {tags} and priority was {priority}')
print(msg.format(priority=model_2.priority, tags=model_2.tags))
model_2.priority = 10
model_2.tags = ['toto', 'tata']
msg = ('AFTER tags are {tags} and priority is {priority}')
print(msg.format(priority=model_2.priority, tags=model_2.tags))
for app in applications():
	print(app)
	for model in app.models:
		print('    ' + str(model))
	for node in app.nodes:
		print('    ' + str(node))
the_class = app
# make a list of all properties of 'parent'
def prop_list(the_class):
	return [p for p in dir(the_class.__class__) if isinstance(getattr(the_class.__class__, p), property)]
print('------------------ PROPERTIES OF AN APPLICATION-------------------------------')
for prop in prop_list(app):
    print('property ' + prop)
print('------------------ PROPERTIES OF A MODEL -------------------------------')
for prop in prop_list(model_1):
    print('property ' + prop)
print('------------------ PROPERTIES OF A NODE -------------------------------')
for prop in prop_list(node_1):
    print('property ' + prop)