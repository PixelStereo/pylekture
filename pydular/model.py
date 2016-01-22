
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

from pydular.node import Node
import weakref

debug = True

class Model(Node):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Node.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Model.instances[_new] = None
		if debug : print ("........... MODEL %s created ..........." %args[0])
		return _new
	def __init__(self,*args,**kwargs):
		Node.__init__(self,*args,**kwargs)
		if debug : print ("........... MODEL %s Inited  ..........." %args[0])
