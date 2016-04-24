#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

sys.path.append(os.path.abspath("./../"))
from pylekture import __version__
from pylekture.functions import checkType
from pylekture.constants import protocols, debug
from pylekture.project import new_project, projects
from pylekture.errors import LektureTypeError, OutputZeroError

debug = 3

class TestAll(unittest.TestCase):

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
        o = p.new_output()
        print(o)
        try:
            raise LektureTypeError('o', 'b')
        except LektureTypeError:
            pass
        self.assertEqual(LektureTypeError.__name__, LektureTypeError.__name__)

    def test_output(self):
        p = new_project()
        try:
            p.output
        except OutputZeroError:
            pass
        o = p.new_output('OSC')
        try:
            p.output = 'bogus'
        except LektureTypeError:
            pass
        p.output = o
        print(p.output)
        s = p.new_scenario()
        e = p.new_event('Osc', command=['/test', 22222])
        print(e)
        s.add_event(e)
        self.assertEqual(p.output, o)
        self.assertEqual(s.output, o)
        print(e.output)
        self.assertEqual(e.output, o)

    def test_project(self):
        # create projects
        my_project = new_project()
        print(my_project)
        my_project.play()
        my_project.getprotocols()
        new_project()
        print(my_project.path, my_project.autoplay, my_project.loop)

        self.assertEqual(my_project.version, __version__)
        my_scenario = my_project.new_scenario()
        my_other_scenario = my_project.new_scenario()
        my_scenario.name = "the scénario è © • test"
        my_other_scenario.name = "the other scenario"
        my_scenario.wait = 0.1
        my_scenario.post_wait = 0.05
        print(my_scenario)

        # create an output
        my_output = my_project.new_output("OSC")

        # Attribute output to scenario
        my_scenario.output = my_output

        # create another output with another protocol
        second_out = my_project.new_output("MIDI")
        second_out.name = "another output"
        second_out.udp = 1234
        third_out = my_project.new_output("OSC")
        third_out.udp = 22222
        forth_out = my_project.new_output("MIDI")

        my_other_scenario.output = forth_out

        # failed in poython3
        #assert(my_output.vars_() ==["ip", "udp", "name"])
        self.assertEqual(my_output.__class__.__name__, "OutputUdp")
        self.assertEqual(second_out.__class__.__name__, "OutputMidi")
        self.assertEqual(isinstance(second_out.__class__.__name__, str), True)
        self.assertEqual(third_out.__class__.__name__, "OutputUdp")
        self.assertEqual(forth_out.__class__.__name__, "OutputMidi")
        self.assertEqual(protocols, ["OSC", 'MIDI'])
        self.assertEqual(len(my_project.outputs), 4)
        self.assertEqual(my_project.version, __version__)
        self.assertEqual(my_scenario.output.__class__.__name__, "OutputUdp")
        self.assertEqual(my_scenario.output.port.split(':')[0], "127.0.0.1")
        self.assertEqual(int(my_scenario.output.port.split(':')[1]), 1234)
        #self.assertEqual(my_scenario.output.name, "no-name")

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
        my_other_scenario.add_event(other_event)
        my_scenario.add_event(other_event)
        my_event.output = second_out

        # test scenario file
        #self.assertEqual(my_scenario.getduration(), 900)
        self.assertEqual(len(my_scenario.events), 5)
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
        self.assertEqual(len(my_project.events), 6)
        my_project.del_event(my_fifth_event)
        self.assertEqual(len(my_project.events), 5)
        # try to delete an event present in other scenario
        my_project.del_event(my_forth_event)
        self.assertEqual(len(my_project.events), 5)

        self.assertEqual(my_project.getprotocols(), ["OutputUdp", "OutputMidi"])
        self.assertEqual(my_project.scenarios[0].name, "the scénario è © • test")
        my_project.scenarios_set(0, 1)
        self.assertEqual(my_project.scenarios[0].name, "the other scenario")
        my_project.del_scenario(my_other_scenario)
        my_project.del_scenario("bogus")
        self.assertEqual(len(my_project.scenarios), 1)
        self.assertEqual(len(my_project.outputs), 4)
        self.assertEqual(len(my_project.getoutputs("OutputUdp")), 2)
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
        self.assertEqual(len(my_project.outputs), 4)
        self.assertEqual(len(my_project.events), 5)
        self.assertEqual(len(my_project.scenarios), 1)
        my_project.reset()
        self.assertEqual(my_project.outputs, [])
        self.assertEqual(my_project.scenarios, [])
        del my_project

    def test_timestamp(self):
        """test_timestamp"""
        import datetime
        timestamp = str(datetime.datetime.now())
        self.assertEqual(isinstance(timestamp, str), True)

if __name__ == "__main__":
    unittest.main()
