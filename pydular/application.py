#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application Class hosted nodes and models
An Application has some protocol/plugin for input/output
"""

import weakref
from pydular import debug
from pydular.model import Model
from pydular.node import Node


class Application(Model):
    """
    Application Class
    """
    instances = weakref.WeakKeyDictionary()
    def __new__(cls, *args, **kwargs):
        Model.__new__(cls, *args, **kwargs)
        _new = object.__new__(cls)
        Application.instances[_new] = None
        if debug:
            if args:
                print("........... APP %s created ..........." %args[0])
        return _new

    def __init__(self, *args, **kwargs):
        Model.__init__(self, args[0])
        if 'author' in kwargs:
            self._author = kwargs['author']
        else:
            self._author = 'unknown'
        if 'version' in kwargs:
            self._version = kwargs['version']
        else:
            self._version = 'unknown'
        self.name = args[0]
        self._nodes = []
        self._models = []
        if debug:
            print("........... APP %s inited ..........." %args[0])

    def __repr__(self):
        printer = 'Application (name:{name}, author:{author}, version:{version})'
        return printer.format(name=self.name, author=self.author, version=self.version)

    @staticmethod
    def getinstances():
        """return list of instances application"""
        return Application.instances.keys()

    @staticmethod
    def export():
        """Export Applications"""
        apps = {'data':{}}
        for app in Application.getinstances():
            apps['data'].setdefault(app.name, {'attributes': \
                {'author':app.author, 'name':app.name, 'version':app.version}})
        return apps

    def node_new(self, *args, **kwargs):
        """
        Create a new node in the parent node
            :return node object if successful
            :return False if name is not valid (already exists or is not provided)
        """
        size = len(self._nodes)
        self._nodes.append(Node(args[0]))
        for key, value in kwargs.items():
            setattr(self._nodes[size], key, value)
        return self._nodes[size]

    def nodes(self):
        """return all nodes"""
        return self._nodes

    def model_new(self, *args, **kwargs):
        """
        Create a new Model in the parent Model
            :return node object if successful
            :return False if name is not valid (already exists or is not provided)
        """
        size = len(self._models)
        self._models.append(Model(args[0]))
        for key, value in kwargs.items():
            setattr(self._models[size], key, value)
        return self._models[size]

    def models(self):
        """list all models"""
        return self._models

    # ----------- AUTHOR -------------
    @property
    def author(self):
        "Current author of the model"
        return self._author
    @author.setter
    def author(self, author):
        self._author = author
    @author.deleter
    def author(self):
        pass

    # ----------- VERSION -------------
    @property
    def version(self):
        "Current version of the model"
        return self._version
    @version.setter
    def version(self, version):
        self._version = version
    @version.deleter
    def version(self):
        pass
