#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os,sys
from time import sleep
# for 
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

# for Travis CI
lib_path = os.path.abspath('./../pydular')
sys.path.append(lib_path)


from pydular import project
from pydular.project import new_project, projects
from pydular.functions import timestamp, unicode2string_dict, unicode2string_list, checkType, isString, isList
import datetime

project.debug = 2

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(my_scenario.getoutput().getprotocol(),'OSC')
        self.assertEqual(my_scenario.getoutput().ip,'127.0.0.1')
        self.assertEqual(my_scenario.getoutput().udp,1234)
        self.assertEqual(my_scenario.getoutput().name,'no-name')
        # test functions file
        self.assertEqual(type(the_timestamp),datetime.datetime)
        self.assertEqual(type(the_raw_timestamp),datetime.datetime)
        self.assertEqual(type(the_nice_timestamp),str)
        self.assertEqual(type(list(string_dict)[0]),bytes)
        self.assertEqual(type(string_list[0]),bytes)
        self.assertEqual(type(a_string),bytes)
        self.assertEqual(type(an_int),int)
        self.assertEqual(type(a_list),list)
        self.assertEqual(type(a_list[0]),float)
        self.assertEqual(type(a_list[0]),float)
        self.assertEqual(type(a_list[1]),bytes)
        self.assertEqual(type(a_list[2]),int)
        self.assertEqual(type(a_float),float)
        self.assertEqual(type(the_none),type(None))
        self.assertEqual(test_list,True)
        self.assertEqual(test_list2,False)
        self.assertEqual(type(string_float),float)
        self.assertEqual(type(string_int),int)
        self.assertEqual(type(simple_float),float)
        self.assertEqual(type(simple_int),int)
        self.assertEqual(a_string_Bool,True)
        # test output file
        # failed in poython3
        #self.assertEqual(my_output.vars_(),['ip', 'udp', 'name'])
        self.assertEqual(my_output.getprotocol(),'OSC')
        self.assertEqual(second_out.getprotocol(),'PJLINK')
        self.assertEqual(third_out.getprotocol(),'OSC')
        self.assertEqual(forth_out.getprotocol(),'MIDI')
        self.assertEqual(project.Output.protocols(),['OSC'])
        self.assertEqual(len(project.Output.getinstances(my_project)),4)
        self.assertEqual(my_output.getproject().version,'0.1.0')
        #test scenario file
        self.assertEqual(my_scenario.getduration(),700)
        self.assertEqual(len(my_scenario.events()),2)
        # test project file
        self.assertEqual(len(projects()),2)
        self.assertEqual(my_project.author, "Renaud Rubiano")
        self.assertEqual(my_project.version, "0.1.0")
        self.assertEqual(my_project.getprotocols(),['OSC', 'PJLINK','MIDI'])
        self.assertEqual(my_project.scenarios()[0].name,'the scenario test')
        my_project.scenarios_set(0,1)
        self.assertEqual(my_project.scenarios()[0].name,'the other scenario')
        my_project.del_scenario(my_scenario)
        self.assertEqual(len(my_project.scenarios()),1)
        self.assertEqual(len(my_project.outputs()),4)
        self.assertEqual(len(my_project.outputs('PJLINK')),1)
        self.assertEqual(len(my_project.outputs('OSC')),2)
        my_project.path = 'my_file'
        my_project.write()
        self.assertEqual(my_project.read('my_file.json'),True)
        sleep(0.5)
        self.assertEqual(my_project.read('tests.py'),False)
        self.assertEqual(my_project.read('bogus'),False)
        my_project.reset()
        self.assertEqual(my_project.outputs(),[])
        self.assertEqual(my_project.scenarios(),[])


if __name__ == '__main__':

    import liblo
    import time

    st = liblo.ServerThread(1235)
    if project.debug :
        print("Created Server Thread on Port", st.port)


    # create a project
    my_project = new_project()
    my_project.author = 'Renaud Rubiano'
    my_project.version = version='0.1.0'

    # create another project
    my_other_project =  new_project()

    # create a scenario
    my_scenario = my_project.new_scenario()
    my_other_scenario = my_project.new_scenario()
    my_scenario.name = 'the scenario test'
    my_other_scenario.name = 'the other scenario'

    # create an output
    my_output = my_project.new_output('OSC')

    # Attribute output to scenario
    my_scenario.output = ['OSC' , 1]
    my_other_scenario.output = ['MIDI' , 1]

    # fill in scenario with events
    first_event = my_scenario.new_event(content=['/previous',[232,'ramp',500]])
    second_event = my_scenario.new_event(content=200)
    third_event = my_scenario.new_event(content=['/zob',[232,'list']])

    # create another output with another protocol
    second_out = my_project.new_output('PJLINK')
    second_out.name = 'another output'
    second_out.udp = 1234

    third_out = my_project.new_output('OSC')
    third_out.udp = 22222

    forth_out = my_project.new_output('MIDI')


    my_scenario.wait = 0.1
    my_scenario.post_wait = 0.05
    
    # play the scenario
    my_scenario.play()
    sleep(1)
    my_scenario.play_from_here(third_event)
    sleep(0.5)
    my_scenario.play_from_here(2)

    midi_event = my_other_scenario.new_event(content=['CC',[16,1,64]])
    my_other_scenario.play(index=1)

    sleep(0.01)

    my_scenario.del_event(3)

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
    a_string = checkType(a_string)
    a_string_Bool = isString(a_string)
    another_string_Bool = isString(string_int)
    a_float = checkType(a_float)
    a_list = checkType(a_list)
    an_int = checkType(an_int)
    the_none = checkType(the_none)
    test_list = isList([1,2])
    test_list2 = isList(u'[1,2]')

    unittest.main()

    del my_project