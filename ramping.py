from datetime import datetime
from time import sleep
from threading import Timer

def print_time():
	print('---END---')

def print_some_times():
	print('---START---')
	timer = Timer(5, print_time, ())
	timer.start()
	timer.join()
	

debut = datetime.now()
print_some_times()
fin = datetime.now()
delta = fin - debut
print(delta)