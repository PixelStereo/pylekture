#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os,sys

# for 
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

# for Travis CI
lib_path = os.path.abspath('./../PyProjekt')
sys.path.append(lib_path)

from pyprojekt import project
from pyprojekt.project import new_project, projects
from pyprojekt.functions import timestamp, unicode2string_dict, unicode2string_list, checkType
import datetime

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
        # test functions file
        self.assertEqual(type(the_timestamp),datetime.datetime)
        self.assertEqual(type(the_raw_timestamp),datetime.datetime)
        self.assertEqual(type(the_nice_timestamp),str)
        self.assertEqual(type(string_dict.keys()[0]),str)
        self.assertEqual(type(string_list[0]),str)
        self.assertEqual(type(a_string),str)
        self.assertEqual(type(an_int),int)
        self.assertEqual(type(a_float),float)
        self.assertEqual(type(the_none),type(None))


if __name__ == '__main__':
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

    # test functions file
    the_timestamp = timestamp()
    the_raw_timestamp = timestamp(format='raw')
    the_nice_timestamp = timestamp('nice')

    unicode_dict = { u'spam': u'eggs', u'foo': True, u'bar': { u'baz': 97 } }
    string_dict = unicode2string_dict(unicode_dict)

    unicode_list = [u'toto' , 22, u'pouett']
    string_list = unicode2string_list(unicode_list)

    a_string = u'popo2'
    a_float = u'122.2'
    an_int = u'122'
    the_none = None
    a_string = checkType(a_string)
    a_float = checkType(a_float)
    an_int = checkType(an_int)
    the_none = checkType(the_none)

    unittest.main()