
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import weakref
debug = True

class Node(object):
	"""This is a node"""
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		_new = object.__new__(self)
		Node.instances[_new] = None
		if debug : print ("........... NODE %s created ..........." %args[0])
		return _new
	def __init__(self, name,parent='root',tags=None,priority=None):
		self.name = name
		self.__parent = parent
		self.__tags = tags
		self.__priority = priority
		print ('PARENT : ' , parent)
		if debug : print ("........... NODE %s Inited  ..........." %name)
		
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