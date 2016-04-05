#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pydular import debug
from pydular.node import Node
from pydular.parameter import Parameter
from pydular.functions import prop_dict


class Model(Node):
    """the model"""
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self._models = []
        self._parameters = []
        if debug:
            print("........... MODEL %s Inited  ..........." %args[0])

    def __repr__(self):
        return str({self.name: prop_dict(self)})

    def parameter_new(self, *args, **kwargs):
        """
        Create a Parameter in the current Model
            :return node object if successful
            :return False if name is not valid (already exists or is not provided)
        """
        size = len(self._parameters)
        self._parameters.append(Parameter(args[0]))
        for key, value in kwargs.items():
            setattr(self._parameters[size], key, value)
        return self._parameters[size]

    @property
    def models(self):
        return self._models

    def export(self):
        return {self.name:prop_dict(self)}

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
    def parameters(self):
        return self._parameters
