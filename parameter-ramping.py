from datetime import datetime
from time import sleep
from threading import Timer


import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.parameter import Parameter


	
p = Parameter()
#p = Parameter(datatype='integer', domain=[1,2])
p.value = 42
print(p.value)
p.datatype = 'integer'
p.clipmode = 'both'
p.domain = [2,3]
print('clipped')
print(p.value)
p.value = 2.2
print(p.value)
p.datatype = 'decimal'
print(p.value)

before = datetime.now()
p.ramp(2.754, 10000)
after = datetime.now()
print(p.value, p.raw)
print(after - before)
