
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

#################
# Modular Module for Python
# Create Models and Parameters
# Pixel Stereo - 2015
################################

"""make a dictionary with the whole namespace of an application
#1 : container have 'data' and 'attributes' dict
#2 : parameters have 'attributes' dict
#3 : parameters are in the 'data' dict of its parent container"""


from modular_functions import *
import weakref

debug = True

class Node(object):
	"""This is a node"""
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		_new = object.__new__(self)
		Node.instances[_new] = None
		if debug : print "........... NODE %s created ..........." %args[0]
		return _new
	def __init__(self, name,parent='root',tags=None,priority=None):
		self.name = name
		self.__parent = parent
		self.__tags = tags
		self.__priority = priority
		print 'PARENT : ' , parent
		if debug : print "........... NODE %s Inited  ..........." %name
		
	# ----------- NAME -------------
	@property
	def name(self):
		"Current name of the model"
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@name.deleter
	def name(self):
		pass

	# ----------- TAGS -------------
	@property
	def tags(self):
		"Current tags of the model"
		return self.__tags

	@tags.setter
	def tags(self, tags):
		self.__tags = tags

	@tags.deleter
	def tags(self):
		pass

	# ----------- PRIORITY -------------
	@property
	def priority(self):
		"Current priority of the model"
		return self.__priority

	@priority.setter
	def priority(self, priority):
		self.__priority = priority

	@priority.deleter
	def priority(self):
		pass

	# ----------- PARENT -------------
	@property
	def parent(self):
		"Current parent of the model"
		return self.__parent

	@parent.setter
	def parent(self, parent):
		self.__parent = parent

	@parent.deleter
	def parent(self):
		pass


class Model(Node):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Node.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Model.instances[_new] = None
		if debug : print "........... MODEL %s created ..........." %args[0]
		return _new
	def __init__(self,*args,**kwargs):
		Node.__init__(self,*args,**kwargs)
		if debug : print "........... MODEL %s Inited  ..........." %args[0]


class Application(Model):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Model.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Application.instances[_new] = None
		if debug : print "........... APP %s created ..........." %args[0]
		return _new
	def __init__(self,*args,**kwargs):
		Model.__init__(self,args[0])
		if 'author' in kwargs:
			self.author = kwargs['author']
		else:
			self.author = 'unknown'
		if 'project' in kwargs:
			self.project = kwargs['project']
		else:
			self.project = 'unknown'
		if 'version' in kwargs:
			self.version = kwargs['version']
		else:
			self.version = 'unknown'
		self.name = args[0]
		if debug : print "........... APP %s inited ..........." %args[0]

	@staticmethod
	def getinstances():
		return Application.instances.keys()

	@staticmethod
	def export():
		apps = {'data':{}}
		for app in Application.getinstances():
			apps['data'].setdefault(app.name,{'attributes':{'author':app.author,'project':app.project,'version':app.version}})
		return apps

	# ----------- AUTHOR -------------
	@property
	def author(self):
		"Current author of the model"
		return self.__author

	@author.setter
	def author(self, author):
		self.__author = author

	@author.deleter
	def author(self):
		pass

	# ----------- PROJECT -------------
	@property
	def project(self):
		"Current project of the model"
		return self.__project

	@project.setter
	def project(self, project):
		self.__project = project

	@project.deleter
	def project(self):
		pass

	# ----------- VERSION -------------
	@property
	def version(self):
		"Current version of the model"
		return self.__version

	@version.setter
	def version(self, version):
		self.__version = version

	@version.deleter
	def version(self):
		pass

class Parameter(Node):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Node.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Parameter.instances[_new] = None
		if debug : print "........... PARAM %s created ..........." %args[0]
		return _new
	def __init__(self,*args,**kwargs):
		"""ERROR NEED TO SEND ARGS TO NODE. E.G. : IF I DEFINE A PRIORITY OR TAG WHEN CREATING PARAMETER, IT NEED TO BE SEND TO THE NODE"""
		Node.__init__(self,args[0])
		if 'value' in kwargs:
			self.value = kwargs['value']
		else:
			self.value = None
		if 'rangeClipmode' in kwargs:
			self.rangeClipmode = kwargs['rangeClipmode']
		else:
			self.rangeClipmode = None
		if 'rangeBounds' in kwargs:
			self.rangeBounds = kwargs['rangeBounds']
		else:
			self.rangeBounds = None
		if 'repetitionsFilter' in kwargs:
			self.repetitionsFilter = kwargs['repetitionsFilter']
		else:
			self.repetitionsFilter = 0
		if 'datatype' in kwargs:
			self.datatype = kwargs['datatype']
		else:
			self.datatype = 'generic'
		if debug : print "........... PARAM %s inited ..........." %args[0]


	# ----------- RAW VALUE -------------
	@property
	def raw(self):
		"raw value without rangeClipmode or rangeBoundsneither than datatype"
		return self.__value

	# ----------- VALUE -------------
	@property
	def value(self):
		"Current value of the parameter"
		if self.datatype == 'decimal':
			value = float(self.__value)
			value = m_clip(self,value)
		elif self.datatype == 'string':
			value = str(self.__value)
		elif self.datatype == 'integer':
			value = int(self.__value)
		return value

	@value.setter
	def value(self, value):
		self.__value = value

	@value.deleter
	def value(self):
		pass

	# ----------- RANGEBOUNDS -------------
	@property
	def rangeBounds(self):
		"Current rangeBounds of the parameter"
		return self.__rangeBounds

	@rangeBounds.setter
	def rangeBounds(self, rangeBounds):
		self.__rangeBounds = rangeBounds

	@rangeBounds.deleter
	def rangeBounds(self):
		pass

	# ----------- RANGECLIPMODE -------------
	@property
	def rangeClipmode(self):
		"Current rangeClipmode of the parameter"
		return self.__rangeClipmode

	@rangeClipmode.setter
	def rangeClipmode(self, rangeClipmode):
		self.__rangeClipmode = rangeClipmode

	@rangeClipmode.deleter
	def rangeClipmode(self):
		pass

	# ----------- DATATYPE -------------
	@property
	def repetitionsFilter(self):
		"Current repetitionsFilter of the parameter"
		return self.__repetitionsFilter

	@repetitionsFilter.setter
	def repetitionsFilter(self, repetitionsFilter):
		self.__repetitionsFilter = repetitionsFilter

	@repetitionsFilter.deleter
	def repetitionsFilter(self):
		pass


	# ----------- DATATYPE -------------
	@property
	def datatype(self):
		"Current value of the parameter"
		return self.__datatype

	@datatype.setter
	def datatype(self, datatype):
		self.__datatype = datatype

	@datatype.deleter
	def datatype(self):
		pass
