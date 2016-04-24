from datetime import datetime
from time import sleep
from threading import Timer


import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.parameter import Parameter


def print_time():
	print('---END---')

def print_some_times():
	print('---START---')
	timer = Timer(5, print_time, ())
	timer.start()
	timer.join()
	
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

quit()

debut = datetime.now()
print_some_times()
fin = datetime.now()
delta = fin - debut
print(delta)