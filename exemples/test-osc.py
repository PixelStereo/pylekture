#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
from pyprojekt import modular
from pyprojekt.modular import Application,Model,Parameter

#import pprint

modular.debug = True

def headerprint(args):
	print
	print '--------' , args , '--------'
	
# create the main application
my_app = Application('test_App',author='Pixel Stereo',version='0.0.1',project='my first project')

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
	print attr , ':' , getattr(my_app,attr)
headerprint('Get Children')
print 'root' , ':' , get_app_child()
for child in get_app_child():
	print child  , ':' , get_child(child)
	



"""NEED TO CREATE REQUEST FOR PARAMETERS NOW"""



quit()





headerprint('registering osc callback')
# create OSC server
from pydevicemanager.devicemanager import OSCServer
osc = OSCServer(22222,'span')
osc = osc.serverThread.oscServer


import Queue
queue = Queue.Queue()

def osc_handler( addr, tags, stuff, source):
    global queue
    print addr,tags,stuff,source
    queue.put( stuff[0] )

osc.addMsgHandler("/OSC", osc_handler) # adding our function



try :
	while 1 :
		pass
except KeyboardInterrupt :
	print "\nClosing OSCClient and OSCServer"
	osc.close()
	st.join()
	print "Done"