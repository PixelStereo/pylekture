#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project
from pylekture.functions import prop_dict

p = new_project()
print('project ' + p.name)
s = p.new_scenario()
print('scenario ' + s.name)
e = p.new_event('OSC')
print('event ' + e.name)
o = p.new_output()
print('outtput ' + o.name)