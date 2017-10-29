#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.ramp import Ramp

a = Ramp(origin=0, destination=100, duration=1000, grain=10)

print(a)
a.play()
