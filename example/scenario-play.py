#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
s.name = 'my_scenario'
e = s.new_event('OSC', command=['/polo', 0])
e.name = 'my_event'
e1 = s.new_event('WAIT', command=[1000])
e2 = s.new_event('OSC', command=['/polo', 232, 'ramp', 1000])
e2.name = 'my_event_2'
o = p.new_output('OSC')
# next line should be : s.output = o
s.output = o
p.play()
#s.play()
#e.play()
#e1.play()
#e2.play()