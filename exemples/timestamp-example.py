
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.application import Application
from pydular.functions import timestamp

print (timestamp())
print (type(timestamp()))
print (timestamp().year)
print (timestamp().month)
print (timestamp().day)
print (timestamp().hour)
print (timestamp().minute)
print (timestamp().second)
print (timestamp().microsecond)

print ('---------------------')
print (timestamp('nice'))