#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture import project
from pylekture import debug
from pylekture.project import new_project, projects
from pydular.functions import timestamp, checkType
from pydular.modular_functions import m_bool, m_int, m_string
import datetime
import liblo
import time


class TestAll(unittest.TestCase):

    def test_project(self):
        """create projects"""
        my_project = new_project()
        my_project.author = 'Renaud Rubiano'
        my_project.version = version='0.1.0'
        my_other_project =  new_project()
        # we should have two projects, as we created two of them
        self.assertEqual(len(projects()), 2)
        self.assertEqual(my_project.author, "Renaud Rubiano")
        self.assertEqual(my_project.version, "0.1.0")
        my_scenario = my_project.new_scenario()
        my_other_scenario = my_project.new_scenario()
        my_scenario.name = 'the scenario test'
        my_other_scenario.name = 'the other scenario'
        my_scenario.wait = 0.1
        my_scenario.post_wait = 0.05
        """create an output"""
        my_output = my_project.new_output('OSC')
        # Attribute output to scenario
        my_scenario.output = ['OSC', 1]
        my_other_scenario.output = ['MIDI', 1]
        # create another output with another protocol
        second_out = my_project.new_output('PJLINK')
        second_out.name = 'another output'
        second_out.udp = 1234
        third_out = my_project.new_output('OSC')
        third_out.udp = 22222
        forth_out = my_project.new_output('MIDI')
        # failed in poython3
        #assert(my_output.vars_() ==['ip', 'udp', 'name'])
        self.assertEqual(my_output.getprotocol(), 'OSC')
        self.assertEqual(second_out.getprotocol(), 'PJLINK')
        self.assertEqual(third_out.getprotocol(), 'OSC')
        self.assertEqual(forth_out.getprotocol(), 'MIDI')
        self.assertEqual(project.Output.protocols(), ['OSC'])
        self.assertEqual(len(project.Output.getinstances(my_project)), 4)
        self.assertEqual(my_output.getproject().version, '0.1.0')
        self.assertEqual(my_scenario.getoutput().getprotocol(), 'OSC')
        self.assertEqual(my_scenario.getoutput().ip, '127.0.0.1')
        self.assertEqual(my_scenario.getoutput().udp, 1234)
        self.assertEqual(my_scenario.getoutput().name, 'no-name')
        """fill in scenario with events"""
        first_event = my_scenario.new_event(content=['/previous', 232, 'ramp', 500])
        second_event = my_scenario.new_event(content=200)
        third_event = my_scenario.new_event(content=['/zob', 232, 'list', 'uno', 2])
        third_half_event = my_scenario.new_event(content=[200])
        fourth_event = my_scenario.new_event(content='/address_only')
        midi_event = my_other_scenario.new_event(content=['CC', 16, 1, 64])
        """test scenario file"""
        self.assertEqual(my_scenario.getduration(), 900)
        self.assertEqual(len(my_scenario.events()), 5)
        my_scenario.play()
        sleep(1)
        my_scenario.play_from_here(third_event)
        sleep(0.5)
        my_scenario.play_from_here(2)
        my_other_scenario.play(index=1)
        sleep(0.01)
        my_project.autoplay = 1
        my_project.loop = 1
        my_scenario.del_event(4)
        my_project.loop = 0
        self.assertEqual(my_project.getprotocols(), ['OSC', 'PJLINK', 'MIDI'])
        self.assertEqual(my_project.scenarios[0].name, 'the scenario test')
        my_project.scenarios_set(0, 1)
        self.assertEqual(my_project.scenarios[0].name, 'the other scenario')
        my_project.del_scenario(my_scenario)
        self.assertEqual(len(my_project.scenarios), 1)
        self.assertEqual(len(my_project.outputs()), 4)
        self.assertEqual(len(my_project.outputs('PJLINK')), 1)
        self.assertEqual(len(my_project.outputs('OSC')), 2)
        my_project.path = 'my_file'
        my_project.write()
        self.assertEqual(my_project.read('my_file.json'), True)
        sleep(0.5)
        self.assertEqual(my_project.read('test_pylekture.py'), False)
        self.assertEqual(my_project.read('bogus'), False)
        my_project.reset()
        self.assertEqual(my_project.outputs(), [])
        self.assertEqual(my_project.scenarios, [])
        del my_project

    def test_timestamp(self):
        """test_timestamp"""
        the_timestamp = timestamp()

    def test_modular_functions(self):
        b = 2
        self.assertEqual(type(b), int)
        b = m_bool(b)
        self.assertEqual(type(b), bool)
        i = 22.22
        self.assertEqual(type(i), float)
        i = m_int(i)
        self.assertEqual(type(i), int)
        i = [22.22]
        self.assertEqual(type(i), list)
        i = m_int(i)
        self.assertEqual(type(i), int)
        s = 2
        self.assertEqual(type(s), int)
        s = m_string(s)
        self.assertEqual(type(s), str)
        s = [2]
        self.assertEqual(type(s), list)
        s = m_string(s)
        self.assertEqual(type(s), str)

    def test_checktypes(self):
        """test_checkType"""
        a_string = u'popo2'
        a_float = u'122.2'
        a_list = [u'2.2', u'renaud', u'22']
        an_int = u'122'
        string_int = '2'
        string_float = '2.2'
        simple_int = 2
        simple_float = 2.2
        simple_int = checkType(simple_int)
        simple_float = checkType(simple_float)
        string_int = checkType(string_int)
        string_float = checkType(string_float)
        the_none = None
        a_float = checkType(a_float)
        a_list = checkType(a_list)
        an_int = checkType(an_int)
        the_none = checkType(the_none)
        # test functions file
        #assert(type(list(string_dict)[0])==unicode)
        #assert(type(string_list[0])==unicode)
        #assert(type(a_string)==unicode)
        #assert(type(an_int)==int)
        #assert(type(a_list)==list)
        #assert(type(a_list[0])==unicode)
        #assert(type(a_list[0])==unicode)
        #assert(type(a_list[1])==unicode)
        #assert(type(a_list[2])==unicode)
        assert(type(a_float)==float)
        assert(type(the_none)==type(None))
        assert(type(string_float)==float)
        assert(type(string_int)==int)
        assert(type(simple_float)==float)
        assert(type(simple_int)==int)


if __name__ == '__main__':
    unittest.main()
