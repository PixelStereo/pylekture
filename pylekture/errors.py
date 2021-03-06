#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
All the Exceptions declared by the package are here
---
"""

class LektureTypeError(Exception):
    """
    Waiting for an object of class 'expected', but received an object of class 'received'
    """
    def __init__(self, expected, received):
        super(LektureTypeError, self).__init__()
        dbg = 'Wait for an {expected} instance object but receive a {received}'
        print(dbg.format(expected=expected, received=received.__class__))
