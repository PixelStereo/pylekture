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
