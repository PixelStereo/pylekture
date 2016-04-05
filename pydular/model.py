
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import weakref
from pydular.node import Node
from pydular import debug


class Model(Node):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Node.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Model.instances[_new] = None
		if debug:
			print("........... MODEL %s created ..........." %args[0])
		return _new
	def __init__(self,*args,**kwargs):
		Node.__init__(self,*args,**kwargs)
		if debug:
			print("........... MODEL %s Inited  ..........." %args[0])

	def __repr__(self):
		printer = 'Model (name:{name}, priority:{priority}, tags:{tags})'
		return printer.format(name=self.name, priority=self.priority, tags=self.tags)