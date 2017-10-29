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

    def test_checkType(self):
        uni = u"22"
        uni = checkType(uni)
        self.assertEqual(isinstance(uni, int), True)
        uni = u"22.22"
        uni = checkType(uni)
        self.assertEqual(isinstance(uni, float), True)
        uni = u"twenty-two-22"
        uni = checkType(uni)
        try:
            # this is python 2
            self.assertEqual(isinstance(uni, basestring), True)
        except NameError:
            # this is python 3
            self.assertEqual(isinstance(uni, (str, bytes)), True)

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
        my_project = new_project()
        print(my_project)
        my_project.play()
        new_project()
        print(my_project.path, my_project.autoplay, my_project.loop)

        self.assertEqual(my_project.version, __version__)

    def test_scenario(self):
        my_project = new_project()
        my_scenario = my_project.new_scenario()
        my_other_scenario = my_project.new_scenario()
        my_scenario.name = "the scénario è © • test"
        my_other_scenario.name = "the other scenario"
        my_scenario.wait = 0.1
        my_scenario.post_wait = 0.05

        # print the scenario
        print(my_scenario)

        # fill in scenario with events
        my_event = my_project.new_event('Osc', command=["/previous", 232, "ramp", 0.5])
        my_event.play()
        my_scenario.add_event(my_event)
        my_second_event = my_project.new_event('Wait', command=0.2)
        my_scenario.add_event(my_second_event)
        my_third_event = my_project.new_event('Osc', command=["/zob", 232, "list", "uno", 2])
        my_forth_event = my_project.new_event('Wait', command=0.3)
        my_fifth_event = my_project.new_event('Osc', command="/address_only")
        my_scenario.add_event(my_forth_event)
        my_scenario.add_event(my_third_event)
        other_event = my_project.new_event('MidiNote', command=[16, 64, 100])
        my_sixth_event = my_project.new_event('ScenarioPlay', command=my_other_scenario)
        my_scenario.add_event(my_sixth_event)
        my_other_scenario.add_event(other_event)
        my_scenario.add_event(other_event)

        # test scenario file
        #self.assertEqual(my_scenario.getduration(), 900)
        self.assertEqual(len(my_scenario.events), 6)
        my_scenario.play()
        sleep(0.1)
        my_scenario.play_from_here(my_third_event)
        sleep(0.2)
        my_scenario.play_from_here(2)
        my_other_scenario.play(index=1)
        sleep(0.01)

        # need to be debug then test again
        my_project.autoplay = 0
        my_project.loop = 1
        # calling del event must check first if the event is in other place.
        self.assertEqual(len(my_project.events), 7)
        my_project.del_event(my_fifth_event)
        self.assertEqual(len(my_project.events), 6)
        # try to delete an event present in other scenario
        my_project.del_event(my_forth_event)
        self.assertEqual(len(my_project.events), 6)

        self.assertEqual(my_project.getprotocols(), ["OutputUdp", "OutputMidi"])
        self.assertEqual(my_project.scenarios[0].name, "the scénario è © • test")
        my_project.scenarios_set(0, 1)
        self.assertEqual(my_project.scenarios[0].name, "the other scenario")
        my_project.del_scenario(my_other_scenario)
        my_project.del_scenario("bogus")
        self.assertEqual(len(my_project.scenarios), 1)
        my_project.write()
        my_project.path = "my_file"
        my_project.write()
        self.assertEqual(my_project.write("the_file"), True)
        my_project.write("/Users/pop")
        self.assertEqual(my_project.read("my_file.lekture"), True)
        sleep(0.01)
        my_project.loop = 0
        sleep(0.2)
        self.assertEqual(len(my_project.scenarios), 1)
        #print(my_project.scenarios[0].name.encode('utf-8'))
        self.assertEqual(my_project.read("test_.py"), False)
        self.assertEqual(my_project.read("bogus"), False)
        self.assertEqual(my_project.read("the_file.lekture"), True)
        self.assertEqual(len(my_project.events), 6)
        self.assertEqual(len(my_project.scenarios), 1)
        sleep(1)
        my_project.reset()
        self.assertEqual(my_project.scenarios, [])
        del my_project

    def test_timestamp(self):
        """test_timestamp"""
        import datetime
        timestamp = str(datetime.datetime.now())
        self.assertEqual(isinstance(timestamp, str), True)


if __name__ == "__main__":
    unittest.main()
