#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

from time import sleep

p = new_project()
p.name = 'la la land'
print(p)
p.write('./')
quit()
o = p.new_output('OSC')
s = p.new_scenario()
s.name = 'Scenar avec une ramp $%ù€ù€ÛÁ7å5»[«¶Û»'
e = p.new_event('Osc', command=['/polo', 1, 'ramp', 6])
print(e)
print(s.name)
print(e.name)
e.name = 'The ramp !!'
s.add_event(e)

e.play()
sleep(0.3)


quit()


p.play()
p.stop()
p.write(os.path.abspath('./event-play_test'))