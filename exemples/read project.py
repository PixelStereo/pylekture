#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
from pydular import project

# create a project
my_project = project.new_project()

my_project.read(path='test.json')
print ('-----------------------------------------')

for scenario in my_project.scenarios():
	print ('name :' , scenario.name)
	for event in scenario.events():
		print ('event :' , event.content)

for scenario in my_project.scenarios():
	scenario.play()
