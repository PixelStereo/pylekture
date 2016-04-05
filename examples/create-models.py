
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os, sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.node import Node
from pydular.model import Model
from pydular.parameter import Parameter
from pydular.application import Application

import pprint

# create an application
my_app = Application('My Python App', author='Renaud Rubiano', project='My Project', version='0.1.0')
# create another application
another_app = Application('Another Py App')
# create a node 
node_1 = my_app.node_new('node.1', priority=-1, tags=['uno','dos'])
node_2 = my_app.node_new('node.2', priority=10, tags=['lol','video'])
# create a few models
model_1 = my_app.model_new('model.1', priority=2, tags=['init','video'])
model_2 = my_app.model_new('model.2', tags=['lol', 'lal'], priority='-1')
model_3 = another_app.model_new('model.1', tags=['pol', 'pal'], priority='-11')
msg = ('BEFORE tags were {tags} and priority was {priority}')
print('')
print(msg.format(priority=model_2.priority, tags=model_2.tags))
model_2.priority = 10
model_2.tags = ['toto', 'tata']
msg = ('AFTER tags are {tags} and priority is {priority}')
print(msg.format(priority=model_2.priority, tags=model_2.tags))
for app in Application.instances.keys():
	print('')
	print(app)
	for node in app.nodes():
		print('           ' + str(node))
	for model in app.models():
		print('           ' + str(model))
