
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

#################
# Modular Module for Python
# Create Models and Parameters
# Pixel Stereo - 2015
################################

from modular_functions import *
import weakref

debug = True

from node import Node
from model import Model


class Parameter(Node):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Node.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Parameter.instances[_new] = None
		if debug : print ("........... PARAM %s created ..........." %args[0])
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
		if debug : print ("........... PARAM %s inited ..........." %args[0])


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
