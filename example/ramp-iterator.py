#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime

from pylekture.animations import Ramp

a = Ramp(origin=0, destination=100, duration=10000, grain=10)

print(a)
a.play()
