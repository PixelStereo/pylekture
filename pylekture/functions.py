#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usefull functions for a pylecture projects
these are different functions directly involved in the project/scenario process
"""

def checkType(data):
    """
    Transform an unicode into its original type

    data:
        an integer or float encoded as a string

    Returns:
        an integer or a float
    """
    try:
        if len(data) == 1 and isinstance(data, list):
            data = data[0]
    except TypeError:
        pass
    try:
        if data.isdigit():
            data = int(data)
        else:
            try:
                data = float(data)
            except ValueError:
                pass
    except AttributeError:
        pass
    return data


def m_bool(value):
    """Transform to a bool if it is not already"""
    if not isinstance(value, bool):
        # check if it is a list
        try:
            value = value[0]
        except TypeError:
            pass
        # simplify to a boolean
        value = bool(value)
    return value


def prop_list(the_class):
    """
    Make a list of properties presents in a class

    Args:
        an object that is an instance of a class.
        We will check what properties exists for this class

    Returns:
        A list with all properties

    Raises:
        Error: Not already implemented
    """
    the_class = the_class.__class__
    return [p for p in dir(the_class) if isinstance(getattr(the_class, p), property)]

def prop_dict(the_class):
    """
    Make a dict of properties presents in a class, with their values

    Args:
        an object that is an instance of a class.
        We will check what properties exists for this class

    Returns:
        A dict with all properties and their values

    Raises:
        Error: Not already implemented
    """
    plist = prop_list(the_class)
    pdict = {}
    for prop in plist:
        if prop == 'output':
            newprop = '_' + prop
            newprop = getattr(the_class, newprop)
            #newprop = newprop
            pdict.setdefault(prop, newprop)
        else:
            pdict.setdefault(prop, getattr(the_class, prop))
    return pdict
