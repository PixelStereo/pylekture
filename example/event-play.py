#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
s.name = 'Scenar avec une ramp $%ù€ù€ÛÁ7å5»[«¶Û»'
e = p.new_event('Osc', command=['/polo', 1, 'ramp', 1])
print(e)
e.name = 'The ramp !!'
o = p.new_output('OSC')
s.add_event(e)

p.play()
p.write(os.path.abspath('./event-play_test'))