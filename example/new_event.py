#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.project import new_project

my_project = new_project(name= 'My Supa Name')

e = my_project.new_event(name='event 1', description='event first')
print(e)

s = my_project.new_scenario(name='scenario test', description='foo bar')
