#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
s.name = 'my_scenario'
e = s.new_event(content=['/polo', 0])
e.name = 'my_event'
e1 = s.new_event(content=[1000])
e2 = s.new_event(content=['/polo', 232, 'ramp', 10])
e2.name = 'my_event_2'
o = p.new_output('OSC')
s.output = ['OSC', 1]
p.play()
#s.play()
#e.play()
#e1.play()
#e2.play()