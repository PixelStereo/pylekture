#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()

s = p.new_scenario()

osc = p.new_output('OSC')
osc_2 = p.new_output('OSC', port='127.0.0.1:22222')

e = p.new_event('Osc')
s.add_event(e)
s.output = osc_2

e.play()
s.play()
p.play()