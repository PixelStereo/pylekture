from datetime import datetime
from time import sleep
from threading import Timer

def print_time():
	print "From print_time", datetime.now()

def print_some_times():
    print datetime.now()
    Timer(5, print_time, ()).start()
    Timer(10, print_time, ()).start()
    sleep(11)  # sleep while time-delay events execute
    print datetime.now()

print_some_times()