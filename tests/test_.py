#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

from pylekture import __version__
from pylekture.functions import checkType
from pylekture.project import new_project, projects
from pylekture.errors import LektureTypeError

from pybush import new_device

my_device = new_device('PyOssia Test Device')
my_device.new_output(protocol='OSC', port='127.0.0.1:1234')
my_int = my_device.new_parameter('test/numeric/int', datatype='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.new_parameter('test/numeric/float', datatype='float', default_value=0.123456, domain=[-2.1, 2.2])


class TestAll(unittest.TestCase):

    def test_a0_first(self):
        debug = 3
        self.assertEqual(debug, 3)

    def test_exceptions(self):
        try:
            raise LektureTypeError('o', 'b')
        except LektureTypeError:
            pass
        self.assertEqual(LektureTypeError.__name__, LektureTypeError.__name__)

    def test_project(self):
        # create projects
        self.assertEqual(len(projects()), 0)
        p = new_project()
        self.assertEqual(len(projects()), 1)
        my_project = new_project(name='Test project')
        self.assertEqual(my_project.name, 'Test project')
        print(my_project)
        self.assertEqual(len(projects()), 2)
        my_project.play()
        new_project()
        self.assertEqual(len(projects()), 3)
        self.assertEqual(my_project.version, __version__)
    def test_scenario(self):
        my_project = projects()[1]
        a_ramp = my_project.new_event('ramp', parameter=my_int, name='int ramp', description='my first event', destination=100, duration=2000)
        another_ramp = my_project.new_event('ramp', parameter=my_float, name='float ramp', description='my second event', destination=1, duration=2000)
        a_random = my_project.new_event('random', parameter=my_int, name='random int', description='a third event', destination=10)
        a_scenario = my_project.new_scenario()
        a_scenario.add_event(another_ramp)
        a_scenario.add_event(a_ramp)
        a_scenario.add_event(another_ramp)
        a_scenario.add_event(a_random)
        self.assertEqual(len(a_scenario.events), 4)
        print(a_random)
        print(a_ramp)
        print(a_scenario)
        a_scenario.del_event(2)
        self.assertEqual(len(a_scenario.events), 3)
        #my_project.play()

    def test_timestamp(self):
        """test_timestamp"""
        import datetime
        timestamp = str(datetime.datetime.now())
        self.assertEqual(isinstance(timestamp, str), True)


if __name__ == "__main__":
    unittest.main()
