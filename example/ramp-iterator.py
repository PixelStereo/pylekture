#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
s.name = 'Scenar avec une ramp $%ù€ù€ÛÁ7å5»[«¶Û»'
e = p.new_event('Osc', command=['/polo', 1, 'ramp', 1])
e.name = 'The ramp !!'
o = p.new_output('OSC')

#e.play()


def gen(duration):
	step = 0.005
	duration = duration / step
	duration = int(duration)
	for step in xrange(duration):
		debut = datetime.now()
		sleep(step)
		fin = datetime.now()
		print(fin - debut)        
		yield 'done'



debut = datetime.now()
gen(1)
fin = datetime.now()
print('-------', fin - debut)
