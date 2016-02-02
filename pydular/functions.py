#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains usefull functions for a project"""

import datetime

def timestamp(display='raw'):
    """Return a time stamp. Used to tag lastopened or to create unique ID"""
    timestamp = datetime.datetime.now()
    return str(timestamp)

def checkType(data):
    """Transform an unicode into its original type"""
    try:
        if data.isdigit():
            data = int(data)
        else:
            try:
                data = float(data)
            except:
                pass
    except:
        pass
    return data

def isString(value):
    """Check if value is a string.
    Return True or False"""
    try:
        isinstance(value, unicode)
        return isinstance(value, str)
    except:
        return isinstance(value, bytes)
