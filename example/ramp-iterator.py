#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.ramp import Ramp

# create the OSSIA Device and some parameters
from pyossia import *
# create the OSSIA Device with the name provided
my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='osc', listening_port=3456, sending_port=5678, logger=True)
#my_device.expose(protocol='osc', listening_port=11111, sending_port=22222, logger=False)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456, domain=[-2.1, 2.2])
#my_bool = my_device.add_param('test/special/bool', value_type='bool', default_value=True, repetition_filter=True)
#my_string = my_device.add_param('test/string', value_type='string', default_value='Hello world !', domain=['once', 'loop'])
#my_list = my_device.add_param('test/list', value_type='list', default_value=[44100, "my_track.wav", 0.6])
#my_char = my_device.add_param('test/special/char', value_type='char', default_value=chr(97))
my_vec2f = my_device.add_param('test/list/vec2f', value_type='vec2f', default_value=[0.5, 0.5], domain=[[-0.6, 1.2], [-0.3, 0.6]])
#my_vec3f = my_device.add_param('test/list/vec3f', value_type='vec3f', default_value=[-960, -270, 180],  domain=[0, 360])
#my_vec4f = my_device.add_param('test/list/vec4f', value_type='string', unit='argb8', default_value=[0, 146, 206, 222])

my_device.root_node.init()
from time import sleep
#sleep(3)
a = Ramp(parameter=my_int, destination=100, duration=100, grain=10)

#a.play()

b = Ramp(parameter=my_float, destination=1, duration=100, grain=10)
my_float.value = 0
b.play()
