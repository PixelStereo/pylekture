#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.project import new_project

my_project = new_project(name= 'My Supa Name')
print(my_project.path)
my_project.write('./')
print(my_project.path)

my_project.play()