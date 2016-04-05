
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os, sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.application import Application

import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

my_app = Application('My Python App',author='Renaud Rubiano',project='My Project',version='0.1.0')
print(my_app)
another_app = Application('Another Py App')
print(another_app)

pprint(Application.export())