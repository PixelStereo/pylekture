#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
import pydular
from pydular.application import application_new, applications
from pydular.node import Node
from pydular.model import Model
from pydular.parameter import Parameter

def headerprint(args):
	print('')
	print(args)
	print('-----------------------')
	
headerprint('create the main application')
app = application_new('My App')

headerprint('create two models')
model_1 = app.model_new('model.1')
model_2 = app.model_new('model.2')

headerprint('create a parameter for model.1')
param_1 = model_1.parameter_new('param.1', value=-1, datatype='decimal', tags=['uno','dos'], \
                                 priority=-1, rangeBounds=[0,1], rangeClipmode='both', \
                                 repetitionsFilter=1)
headerprint('list app, models and parameters')
for app in applications():
    print('    ' +  str(app))
    for model in app.models:
        print('        ' +  str(model))
        for parameter in model.parameters:
            print('            ' +  str(parameter))


headerprint('try rangeClipmode function')
print ('rangeClipmode is : ' , param_1.rangeBounds)
print ('raw value is ' , param_1.raw)
print ('rangeClipmode is : ' , param_1.rangeClipmode)
print ('value is : ' , param_1.value)
param_1.rangeClipmode = 'low'
print ('raw value is ' , param_1.raw)
print ('rangeClipmode is : ' , param_1.rangeClipmode)
print ('value is : ' , param_1.value)
param_1.value = 2
param_1.rangeClipmode = 'high'
print ('raw value is ' , param_1.raw)
print ('rangeClipmode is : ' , param_1.rangeClipmode)
print ('value is : ' , param_1.value)
param_1.rangeClipmode = 'both'
print ('raw value is ' , param_1.raw)
print ('rangeClipmode is : ' , param_1.rangeClipmode)
print ('value is : ' , param_1.value)

headerprint('repetitionsFilter')
print (param_1.repetitionsFilter)
param_1.repetitionsFilter = 0
print (param_1.repetitionsFilter)

headerprint('try priority function')
print (param_1.priority)
param_1.priority = 0
print (param_1.priority)

headerprint('tags')
print (param_1.tags)
param_1.tags = ['ein','zwei']
print (param_1.tags)

headerprint('name')
param_1.name = 22
print (param_1.name , type(param_1.name))
param_1.name = 'zobi'
print (param_1.name , type(param_1.name))

headerprint('datatype')
print (param_1.datatype)
param_1.datatype = 'integer'
print (param_1.datatype)

headerprint('set value and rangeClipmode')
param_1.value = 999.99
param_1.rangeClipmode = [0,1000]
print ('raw value is : ' , param_1.raw , 'and rangeClipmode is : ' , param_1.rangeClipmode)
print ('datatype is : ' , param_1.datatype , 'and value is so : ' , type(param_1.value) , param_1.value)
param_1.datatype = 'decimal'
print ('datatype is : ' , param_1.datatype , 'and value is so : ' , type(param_1.value) , param_1.value)