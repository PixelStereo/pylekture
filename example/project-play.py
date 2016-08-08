#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from pprint import pprint
from time import sleep

lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project
from pylekture.functions import prop_dict

p = new_project()
p.read(os.path.abspath('./../tests/the_file.lekture'))
p.export()
p.export()
p.write()
p.write()
p.read(os.path.abspath('./../tests/the_file.lekture'))
p.write(os.path.abspath('./../tests/the_file.lekture'))
p.read(os.path.abspath('./../tests/the_file.lekture'))


ss = p.scenarios
print(str(len(ss)) + ' scenarios')
s = ss[0]
#print(s.name.encode('utf8'))
print(type(s.name))
es = s.events
print(str(len(es)) + ' events')
p.loop = False
p.play()
print('-----------------------------------------------------------------------------')
for key, value in prop_dict(p).items():
	print(key + ' ----> ' + str(value))
