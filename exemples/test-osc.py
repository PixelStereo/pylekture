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


def headerprint(args):
	print ()
	print ('--------' , args , '--------')
	
# create the main application
my_app = Application('test_App',author='Pixel Stereo',version='0.0.1',project='my first application')

# create two models
model_1 = Model('model.1')
model_2 = Model('model.2')
model_3 = Model('model.3',parent='model.2')

# create a few parameters for app
param_0 = Parameter('param.0',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)
# create a few parameters for model_1 and model_2
param_1 = Parameter('param.1',parent='model.1',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)
param_2 = Parameter('param.2',parent='model.1',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)
param_3 = Parameter('param.3',parent='model.2',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)
param_4 = Parameter('param.4',parent='model.2',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)
param_5 = Parameter('param.5',parent='model.3',value=-1,datatype='decimal',tags=['uno','dos'],priority=-1,rangeBounds=[0,1],rangeClipmode='both',repetitionsFilter=1)


def get_app_attr():
	attr_list = []
	for app in Application.instances:
		for attribute in dir(app):
			if not attribute.startswith('__'):
				if not attribute.startswith('_'):
					if not attribute == 'instances':
						if not attribute == 'name':
							attr_list.append(attribute)
		return attr_list


def get_app_child():
	child_list = []
	for child in Model.instances:
		if child.parent == 'root':
			child_list.append(child.name)
	return child_list

def get_child(arg):
	child_list = []
	for child in Model.instances.keys():
		if child.parent == arg:
			child_list.append(child.name)
	return child_list

headerprint('Application attributes')
for attr in get_app_attr():
	print (attr , ':' , getattr(my_app,attr))
headerprint('Get Children')
print ('root' , ':' , get_app_child())
for child in get_app_child():
	print (child  , ':' , get_child(child))
	


headerprint('registering osc callback')
#from __future__ import print_function
import liblo
import time

st = liblo.ServerThread(22222)
print("Created Server Thread on Port", st.port)


def print_handler():
	pass

print ('-----')

for var in vars(my_app):
	var = var.split('__')
	var = var[1]
	root = getattr(my_app,'name')
	if var != 'name':
		print ('/'+root+'/'+var)
		st.add_method('/baz', 'f', print_handler, 456)
	print var , ':' , getattr(my_app,var)


quit()



class Blah:
    def __init__(self, x):
        self.x = x
    def baz_cb(self, path, args, types, src, user_data):
        print("baz_cb():")
        print(args)
        print("self.x is", self.x, ", user data was", user_data)

b = Blah(123)
st.add_method('/baz', 'f', b.baz_cb, 456)
st.start()


try :
	while 1 :
		pass
except KeyboardInterrupt :
	print ("\nClosing OSCClient and OSCServer")
	st.stop()
	print ("Done")


