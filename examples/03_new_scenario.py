#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pylekture.project import new_project

from pyossia import ossia

my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='osc', listening_port=3456, sending_port=5678, logger=False)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456, domain=[-2.1, 2.2])

my_project = new_project(name= 'Demo Project')
a_ramp = my_project.new_event('ramp', parameter=my_int, name='event 1', description='my first event', destination=200, duration=2000)
a_random = my_project.new_event('random', parameter=my_int, name='event 2', description='a second event', destination=10)
a_scenario = my_project.new_scenario()

my_device.root_node.init()

print(a_scenario)

a_scenario.add_event(a_ramp)
a_scenario.add_event(a_random)
a_scenario.add_event(a_ramp)


print(a_random)
print(a_ramp)

print(a_scenario)

a_scenario.del_event(2)
print(a_scenario)

my_project.play()


