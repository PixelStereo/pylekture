#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application Class hosted nodes and models
An Application has some protocol/plugin for input/output
"""

from pydular import debug, _applications
from pydular.model import Model
from pydular.node import Node

def application_new(*args, **kwargs):
    """Create a new application
        :return node object if successful
        :return False if name is not valid (already exists or is not provided)"""
    size = len(_applications)
    _applications.append(Application(args[0]))
    for key, value in kwargs.items():
        setattr(_applications[size], key, value)
    return _applications[size]

def applications():
    return _applications

def export():
    """Export Applications"""
    apps = {'data':{}}
    for app in applications():
        apps['data'].setdefault(app.name, {'attributes': \
            {'author':app.author, 'name':app.name, 'version':app.version}})
    return apps


class Application(Model):
    """Application Class"""
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        if 'author' in kwargs:
            self._author = kwargs['author']
        else:
            self._author = 'unknown'
        if 'version' in kwargs:
            self._version = kwargs['version']
        else:
            self._version = 'unknown'
        self._name = args[0]
        self._nodes = []
        self._models = []
        if debug:
            print("........... APP %s inited ..........." %args[0])

    def __repr__(self):
        printer = 'Application (name:{name}, author:{author}, version:{version})'
        return printer.format(name=self.name, author=self.author, version=self.version)

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

    @property
    def models(self):
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
