#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pylekture.project import new_project

from pyossia import ossia

my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='osc', listening_port=3456, sending_port=5678, logger=True)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456, domain=[-2.1, 2.2])

my_project = new_project(name= 'My Supa Name')
a_ramp = my_project.new_event('ramp', parameter=my_int, name='event 1', description='my first event', destination=200, duration=2000)
a_random = my_project.new_event('random', parameter=my_int, name='event 2', description='a second event', destination=10)
print(a_random)
print(a_ramp)

a_ramp.play()
#a_random.play()


#my_project.play()

