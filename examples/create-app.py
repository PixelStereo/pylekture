
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os, sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

import pydular
from pydular.application import application_new, applications_export

import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

my_app = application_new('My Python App',author='Renaud Rubiano',version='0.1.0')
print(my_app)
another_app = application_new('Another Py App')
print(another_app)

pprint(applications_export())