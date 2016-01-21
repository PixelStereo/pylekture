#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This file contains usefull functions for a project"""
import datetime

def timestamp(format='raw'):
    """Return a time stamp. Used to tag lastopened or to create unique ID"""
    timestamp = datetime.datetime.now()
    if format != 'nice':
        return timestamp
    else:
        return str(timestamp)

def unicode2string_dict(data):
    """convert a unicode dict to a stringed dict"""
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = unicode2string_list(value)
        elif isinstance(value, dict):
            value = unicode2string_dict(value)
        rv[key] = value
    return rv

def unicode2string_list(data):
    """convert a unicode list to a string list"""
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = unicode2string_list(item)
        elif isinstance(item, dict):
            item = unicode2string_dict(item)
        rv.append(item)
    return rv

def checkType(data):
    """Transform an unicode into its original type"""
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    if isinstance(data,list):
        for item in data:
            index = data.index(item)
            item = checkType(item)
            data[index] = item
    if isinstance(data,str):
        if data.isdigit():
            data = int(data)
        elif isList(data):
            print '-'
            data = list(data)
        else:
            try:
                data = float(data)
            except:
                pass
    elif isFloat(data):
        data = float(data)
    elif isInt(data):
        data = int(data)
    return data

def isString(value):
    """Check if value is a string.
    Return True or False""" 
    return isinstance(value,str)

def isList(value):
    """Check if value is a list.
    Return True or False"""
    return isinstance(value,list)

def isUnicode(value):
    """Check if value is a unicode string.
    Return True or False"""
    return isinstance(value,unicode)

def isFloat(value):
    """Check if value is a float.
    Return True or False"""
    return isinstance(value,float)

def isInt(value):
    """Check if value is an int.
    Return True or False"""
    return isinstance(value,int)


