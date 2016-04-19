#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

sys.path.append(os.path.abspath("./../"))
from pylekture import __version__
from pylekture.functions import checkType
from pylekture.constants import protocols
from pylekture.project import new_project, projects
from pylekture.errors import LektureTypeError
from pylekture.output import OutputMidi, OutputUdp


class TestAll(unittest.TestCase):

    def test_output(self):
        p = new_project()
        o = p.new_output('OSC')
        s = p.new_scenario()
        e = p.new_event('Osc', command=['/test', 22222])
        s.add_event(e)
        self.assertEqual(p.output, o)
        self.assertEqual(s.output, o)
        self.assertEqual(e.output, o)

    def test_exceptions(self):
        p = new_project()
        o = p.new_output()
        try:
            raise LektureTypeError(OutputMidi, o)
        except LektureTypeError:
            print('we raised LektureTypeError')

    def test_project(self):
        # create projects
        my_project = new_project()
        print(my_project)
        my_project.play()
        my_project.getprotocols()
        new_project()
        print(my_project.path, my_project.autoplay, my_project.loop)

        # we should have two projects, as we created two of them
        self.assertEqual(len(projects()), 4)
        self.assertEqual(my_project.version, __version__)
        my_scenario = my_project.new_scenario()
        my_other_scenario = my_project.new_scenario()
        my_scenario.name = "the scénario è © • test"
        my_other_scenario.name = "the other scenario"
        my_scenario.wait = 0.1
        my_scenario.post_wait = 0.05

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
        self.assertEqual(my_output.service, "OutputUdp")
        self.assertEqual(second_out.service, "OutputMidi")
        self.assertEqual(isinstance(second_out.service, str), True)
        self.assertEqual(third_out.service, "OutputUdp")
        self.assertEqual(forth_out.service, "OutputMidi")
        self.assertEqual(protocols, ["OSC", 'MIDI'])
        self.assertEqual(len(my_project.outputs), 4)
        self.assertEqual(my_project.version, __version__)
        self.assertEqual(my_scenario.output.service, "OutputUdp")
        self.assertEqual(my_scenario.output.ip, "127.0.0.1")
        self.assertEqual(my_scenario.output.udp, 1234)
        #self.assertEqual(my_scenario.output.name, "no-name")

        # fill in scenario with events
        my_event = my_project.new_event('Osc', command=["/previous", 232, "ramp", 0.5])
        my_scenario.add_event(my_event)
        my_second_event = my_project.new_event('Wait', command=0.2)
        my_scenario.add_event(my_second_event)
        my_third_event = my_project.new_event('Osc', command=["/zob", 232, "list", "uno", 2])
        my_forth_event = my_project.new_event('Wait', command=0.3)
        my_project.new_event('Osc', command="/address_only")
        my_scenario.add_event(my_forth_event)
        my_scenario.add_event(my_third_event)
        other_event = my_project.new_event('MidiNote', command=[16, 64, 100])
        my_other_scenario.add_event(other_event)
        my_scenario.add_event(other_event)

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
        my_project.del_event(5)
        self.assertEqual(len(my_project.events), 5)
        # try to delete an event present in other scenario
        my_project.del_event(3)
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
        #self.assertEqual(my_project.write("the_file"), True)
        my_project.write("/Users/pop")
        #self.assertEqual(my_project.read("my_file.lekture"), True)
        sleep(0.01)
        my_project.loop = 0
        sleep(0.2)
        self.assertEqual(len(my_project.scenarios), 1)
        #print(my_project.scenarios[0].name.encode('utf-8'))
        self.assertEqual(my_project.read("test_.py"), False)
        self.assertEqual(my_project.read("bogus"), False)
        #self.assertEqual(my_project.read("the_file.lekture"), True)
        self.assertEqual(len(my_project.outputs), 4)
        my_project.reset()
        self.assertEqual(my_project.outputs, [])
        self.assertEqual(my_project.scenarios, [])
        del my_project

    def test_timestamp(self):
        """test_timestamp"""
        import datetime
        timestamp = str(datetime.datetime.now())
        self.assertEqual(isinstance(timestamp, str), True)

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


if __name__ == "__main__":
    unittest.main()
