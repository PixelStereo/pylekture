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

def prop_list(the_class):
        return [p for p in dir(the_class.__class__) if isinstance(getattr(the_class.__class__, p), property)]

def prop_dict(the_class):
        plist = prop_list(the_class)
        pdict = {}
        for prop in plist:
            pdict.setdefault(prop, getattr(the_class, prop))
        return pdict