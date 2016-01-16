#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
print lib_path
lib_path = os.path.abspath('./../pyprojekt')
sys.path.append(lib_path)
print lib_path

from pyprojekt import project
from pyprojekt.project import new_project, projects

# create a project
my_project = new_project()
my_project.author = 'Renaud Rubiano'
my_project.version = version='0.1.0'

# create another project
my_other_project =  new_project()

# create a scenario
my_scenario = my_project.new_scenario()

# create an output
my_output = my_project.new_output('OSC')

# Attribute output to scenario
my_scenario.output = ['OSC' , 1]

# create another output with another protocol
second_out = my_project.new_output('PJLINK')
second_out.name = 'another output'
second_out.udp = 1234

third_out = my_project.new_output('OSC')
third_out.udp = 22222

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(my_project.author, "Renaud Rubiano")
        self.assertEqual(my_project.version, "0.1.0")
        self.assertEqual(len(projects()),2)
        self.assertEqual(my_project.getprotocols(),['OSC', 'PJLINK'])
        self.assertEqual(my_scenario.getoutput().getprotocol(),'OSC')
        self.assertEqual(my_scenario.getoutput().ip,'127.0.0.1')
        self.assertEqual(my_scenario.getoutput().udp,10000)
        self.assertEqual(my_scenario.getoutput().name,'no-name')
        self.assertEqual(len(my_project.outputs()),3)
        self.assertEqual(len(my_project.outputs('PJLINK')),1)
        self.assertEqual(len(my_project.outputs('OSC')),2)

if __name__ == '__main__':
    unittest.main()