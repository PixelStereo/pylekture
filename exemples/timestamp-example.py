
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.project import new_project

import datetime

def timestamp():
	return datetime.datetime.now()

print(type(timestamp()))
print(timestamp().year)
print(timestamp().month)
print(timestamp().day)
print(timestamp().hour)
print(timestamp().minute)
print(timestamp().second)
print(timestamp().microsecond)

project = new_project()
scenario = project.new_scenario()
print(scenario.name)