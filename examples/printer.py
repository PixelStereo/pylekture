#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
import pydular
from pydular.project import Project

popo = Project()
print popo