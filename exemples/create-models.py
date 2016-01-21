
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
import pydular
from pydular.application import Application
from pydular.node import Node
from pydular.model import Model
from pydular.parameter import Parameter

import pprint

print ('--Creating an application--')
print ('---------------------------')
my_app = Application('My Python App',author='Renaud Rubiano',project='My Project',version='0.1.0')
print ('app-name : ' , my_app.name)
print ('app-author : ' , my_app.author)
print ('app-project : ' , my_app.project)
print ('app-version : ' , my_app.version)
print ()
print ('--Creating another App--')
print ('------------------------')
another_app = Application('Another Py App')
print ()
print ('--Creating a node--')
print ('-------------------')
node_0 = Node('node.0',priority=-1,tags=['uno','dos'])
print ('node-object : ' ,  node_0)
print ('node-name : ' , node_0.name)
print ('node-priority : ' , node_0.priority)
print ('node-tags : ' , node_0.tags)
print ('node-parent : ' , node_0.parent)
print ()
print ('--Creating a model--')
print ('--------------------')
model_0 = Model('model.0',priority=2,tags=['init','video'])
print ('model-object : ' ,  model_0)
print ('model-name : ' , model_0.name)
print ('model-priority : ' , model_0.priority)
print ('model-tags : ' , model_0.tags)
print ('model-parent : ' , model_0.parent)

# Create two models
model_1 = Model('model.1',tags='lol,lal',priority='-1')
print ('1-name : ' , model_1.name)
print ('1-priority : ' , model_1.priority)
print ('1-tags : ' , model_1.tags)
print ('1-parent : ' , model_1.parent)
print ()

model_2 = Model('model.2','root',tags='pol,pal',priority='-11')
print ('2-name : ' , model_2.name)
print ('2-priority : ' , model_2.priority)
print ('2-tags : ' , model_2.tags)
print ()

model_1.priority = 10
model_1.tags='toto,tata'
print ('1-name : ' , model_1.name)
print ('1-priority : ' , model_1.priority)
print ('1-tags : ' , model_1.tags)
print ()

model_1.name = 'toto'
model_1.priority = 20
model_1.tags = 'un autre tag'
print ('1-name : ' , model_1.name)
print ('1-priority : ' , model_1.priority)
print ('1-tags : ' , model_1.tags)
print ()
print ('--Application Instances--')
print ('-------------------------')
for app in Application.instances.keys():
	print (app.name)
print ()
print ('--Node Instances--')
print ('--------------------')
for node in Node.instances.keys():
	print (node.name)
print ()
print ('--Model Instances--')
print ('--------------------')
for model in Model.instances.keys():
	print (model.name)
print ()