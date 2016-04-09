#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
e = s.new_event(content=['/polo', 232, 'ramp', 2000])
o = p.new_output('OSC')
s.output = ['OSC', 1]
#p.play()
s.play()
#e.play()