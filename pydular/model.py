#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pydular import debug
from pydular.node import Node
from pydular.parameter import Parameter


class Model(Node):
    """the model"""
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self._parameters = []
        if debug:
            print("........... MODEL %s Inited  ..........." %args[0])

    def __repr__(self):
        printer = 'Model (name:{name}, priority:{priority}, tags:{tags})'
        return printer.format(name=self.name, priority=self.priority, tags=self.tags)

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
    def parameters(self):
        return self._parameters