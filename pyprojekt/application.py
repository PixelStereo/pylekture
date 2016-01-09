
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import weakref

debug = True

from node import Node
from model import Model

class Application(Model):
	instances = weakref.WeakKeyDictionary()
	def __new__(self,*args,**kwargs):
		Model.__new__(self,*args,**kwargs)
		_new = object.__new__(self)
		Application.instances[_new] = None
		if debug : (print "........... APP %s created ..........." %args[0])
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
		if debug : (print "........... APP %s inited ..........." %args[0])

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
