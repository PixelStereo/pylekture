#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usefull functions for a pylecture projects
these are different functions directly involved in the project/scenario process
"""

def checkType(data):
    """
    Transform an unicode into its original type

    Args:
        an integer or float encoded as a string

    Returns:
        an integer or a float
    """
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
