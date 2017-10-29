#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.project import new_project

from pyossia import *
my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='osc', listening_port=3456, sending_port=5678, logger=True)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456, domain=[-2.1, 2.2])


my_project = new_project(name= 'My Supa Name')
e = my_project.new_ramp(parameter=my_int, name='event 1', description='event first', destination=100)
print(e)
e.play()

for truc in dir(e):
	print(str(truc), getattr(e, truc))