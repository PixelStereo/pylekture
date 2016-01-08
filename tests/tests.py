#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pyprojekt import application
from pyprojekt.application import Application

my_app = Application('My Python App',author='Renaud Rubiano',project='My Project',version='0.1.0')
my_other_app =  Application('My Other Python App')


class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(my_app.name, "My Python App")
        self.assertEqual(my_app.author, "Renaud Rubiano")
        self.assertEqual(my_app.project, "My Project")
        self.assertEqual(my_app.version, "0.1.0")


if __name__ == '__main__':
    unittest.main()