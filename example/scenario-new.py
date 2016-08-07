#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
print('project ' + p.name)
s = p.new_scenario()
print('scenario ' + s.name)
e = p.new_event('Osc')
print('event ' + e.name)
o = p.new_output('OSC')
print('output ' + o.name)