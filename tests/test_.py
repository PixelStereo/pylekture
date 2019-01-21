#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

from pylekture import __version__
from pylekture.functions import checkType
from pylekture.constants import debug
from pylekture.project import new_project, projects
from pylekture.errors import LektureTypeError

class TestAll(unittest.TestCase):

    def test_a0_first(self):
        debug = 3
        self.assertEqual(debug, 3)


    def test_exceptions(self):
        self.assertEqual(len(projects()), 0)
        p = new_project()
        self.assertEqual(len(projects()), 1)
        try:
            raise LektureTypeError('o', 'b')
        except LektureTypeError:
            pass
        self.assertEqual(LektureTypeError.__name__, LektureTypeError.__name__)

    def test_project(self):
        # create projects
        my_project = new_project(name='Test project')
        self.assertEqual(my_project.name, 'Test project')
        print(my_project)
        my_project.play()
        new_project()
        self.assertEqual(my_project.version, __version__)

    def test_timestamp(self):
        """test_timestamp"""
        import datetime
        timestamp = str(datetime.datetime.now())
        self.assertEqual(isinstance(timestamp, str), True)


if __name__ == "__main__":
    unittest.main()
