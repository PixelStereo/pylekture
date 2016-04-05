
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import weakref
from pydular import debug

class Node(object):
	"""This is a node"""
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		_new = object.__new__(self)
		Node.instances[_new] = None
		if debug:
			print ("........... NODE %s created ..........." %args[0])
		return _new

	def __init__(self, name, tags=None, priority=None):
		self.name = name
		self._tags = tags
		self._priority = priority
		if debug:
			print ("........... NODE %s Inited  ..........." %name)
	
	def __repr__(self):
		printer = 'Node (name:{name}, priority:{priority}, tags:{tags})'
		return printer.format(name=self.name, priority=self.priority, tags=self.tags)

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
		return self._tags
	@tags.setter
	def tags(self, tags):
		self._tags = tags
	@tags.deleter
	def tags(self):
		pass

	# ----------- PRIORITY -------------
	@property
	def priority(self):
		"Current priority of the model"
		return self._priority
	@priority.setter
	def priority(self, priority):
		self._priority = priority
	@priority.deleter
	def priority(self):
		pass
