#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import weakref
import devicemanager
from time import sleep
from functions import timestamp
from functions import unicode2_list
from functions import unicode2string_dict
from functions import unicode2string_list
from OSC import OSCMessage , OSCClientError
from socket import socket
from socket import error as socket_error
from pjlink import Projector
from devicemanager import OSCClient as OSCClient
client = OSCClient()

debug = True

def new_project():
    """Create a new project"""
    return Project()

def projects():
    """return a list of projects available"""
    project_list = []
    for proj in Project.getinstances():
        project_list.append(proj)
    return project_list

class Project(object):
    """docstring for Project"""

    # used  to make a list of projects 
    _instances = []

    def __init__(self):
        super(Project, self).__init__()
        self._instances.append(weakref.ref(self))
        if debug == 2:
            print
            print "........... PROJECT created ..........."
            print 
        self.author = None
        self.version = None
        self.path = None
        self.lastopened = timestamp()
        self.output_list = []
        self.scenario_list = []

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        for d in dead:
            cls._instances.remove(dead)

    def reset(self):
        """reset a project by deleting project.attributes, scenarios, outputs and events related"""
        # reset project attributes
        self.author = None
        self.version = None
        self.path = None
        # reset outputs
        for output in self.outputs():
            self.output_list.remove(output)
        # reset scenarios and events
        for scenario in self.scenarios():
            for event in scenario.events():
                scenario.event_list.remove(event)
            self.scenario_list.remove(scenario)

    def read(self,path) : 
        """open a lekture project"""
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print "ERROR - THIS PATH IS NOT VALID" , path
        else :
            print 'loading' , path
            try:
                with open(path) as in_file :
                    # clear the project
                    self.reset()
                    if debug : print 'file reading : ' , path
                    loaded = json.load(in_file,object_hook=unicode2string_dict)
                    in_file.close()
                    for key,val in loaded.items():
                        if key == 'scenario' :
                            for scenar_list in loaded['scenario']:
                                for attribute , value in scenar_list['attributes'].items():
                                    if attribute == 'name':
                                        name = value
                                    elif attribute == 'description':
                                        description = value
                                    elif attribute == 'output':
                                        output = value
                                    elif attribute == 'events':
                                        events = value
                                scenario = self.new_scenario()
                                scenario.name = name
                                scenario.description = description
                                scenario.output = output
                                for event in events:
                                    for attribute , value in event['attributes'].items():
                                        if attribute == 'name':
                                            name = value
                                        elif attribute == 'description':
                                            description = value
                                        elif attribute == 'output':
                                            output = value
                                        elif attribute == 'content':
                                            content = value
                                    event = scenario.new_event()
                                    event.name = name
                                    event.description = description
                                    event.output = output
                                    event.content = content
                        elif key == 'attributes' :
                            for attribute,value in loaded['attributes'].items():
                                if attribute == 'author':
                                    self.author = value
                                if attribute == 'version':
                                    self.version = value
                            self.lastopened = timestamp()
                        elif key == 'outputs' :
                            for out_list in loaded['outputs']:
                                for attribute , value in out_list['attributes'].items():
                                    if attribute == 'name':
                                        name = value
                                    if attribute == 'ip':
                                        address_ip = value
                                    if attribute == 'udp':
                                        udp = value
                                self.new_output(self,name=name,ip=address_ip,udp=udp)
                    if debug : print 'project loaded'
                    self.path = path
            # catch error if file is not valid or if file is not a lekture project
            except (IOError , ValueError):
                if debug : print 'error : project not loaded'
                return False
            return True

    def write(self,path=None):
        """write a project on the hard drive"""
        if path:
            savepath = path
        else:
            savepath = self.path
        if savepath:
            if not savepath.endswith('.json'):
                savepath = savepath + '.json'
            out_file = open(str(savepath), 'w')
            project = {}
            project.setdefault('scenario',self.export_scenario())
            project.setdefault('attributes',self.export_attributes())
            project.setdefault('outputs',self.export_outputs())
            out_file.write(json.dumps(project,sort_keys = True, indent = 4,ensure_ascii=False).encode('utf8'))
            if debug : print ("file has been written : " , savepath)
            return True
        else:
            return False

    def scenarios(self):
        """return a list of available scenario for this project"""
        return self.scenario_list

    def scenarios_set(self,old,new):
        """Change order of a scenario in the scenario list of the project"""
        s_list = self.scenarios()
        s_temp = s_list[old]
        s_list.pop(old)
        s_list.insert(new,s_temp)
        for scenario in s_list:
            self.scenario_list.remove(scenario)
        for scenario in s_list:
            self.scenario_list.append(scenario)

    def outputs(self,protocol='all'):
        """return a list of available output for this project"""
        outs = []
        if protocol == 'all' or protocol == None:
            return Output.getinstances(self)
        else:
            for out in self.output_list:
                if protocol == out.getprotocol():
                    outs.append(out)
            return outs

    def getprotocols(self):
        protocols = []
        for out in self.outputs():
            protocols.append(out.getprotocol())
        if protocols == []:
            return None
        else:
            return protocols

    def new_scenario(self,*args,**kwargs):
        """create a new scenario"""
        scenario = Scenario(self)
        self.scenario_list.append(scenario)
        return scenario

    def new_output(self,protocol,**kwargs):
        """create a new output for this project"""
        taille = len(self.output_list)
        the_output = None
        self.output_list.append(the_output)
        self.output_list[taille] = Output(self,protocol)
        for key, value in kwargs.items():
            setattr(self.output_list[taille], key, value)
        return self.output_list[taille]

    def del_scenario(self,scenario):
        """delete a scenario of this project
        This function will delete events of the scenario"""
        if scenario in self.scenarios():
            # delete events of this scenario
            for event in scenario.events():
                scenario.del_event(event)
            # delete the scenario itself
            self.scenario_list.remove(scenario)
            if debug == 2:
                print 'delete scenario' , scenario , len(self.scenario_list)
        else:
            if debug == 2:
                print 'ERROR - trying to delete a scenario which not exists in self.scenario_list' , scenario

    def export_attributes(self):
        """export attributes of the project"""
        attributes = {'author':self.author,'version':self.version,'lastopened':self.lastopened}
        return attributes

    def export_events(self):
        """export events of the project"""
        events = []
        for event in self.events():
            events.append({'attributes':{'output':event.output,'name':event.name,'description':event.description,'content':event.content}})
        return events
    
    def export_scenario(self):
        """export scenario of the project"""
        scenarios = []
        for scenario in self.scenarios():
            scenarios.append({'attributes':{'output':scenario.output,'name':scenario.name,'description':scenario.description,'events':scenario.export_events()}})
        return scenarios

    def export_outputs(self):
        """export outputs of the project"""
        outputs = {}
        for output in self.outputs():
            protocol = output.getprotocol()
            if not protocol in outputs:
                outputs.setdefault(protocol,[])
            outputs[protocol].append({'attributes':{}})
            index = len(outputs[protocol])
            index -= 1
            for attr in output.vars_():
                if not attr.startswith('_'):
                    outputs[protocol][index]['attributes'].setdefault(attr,getattr(output,attr))
        return outputs


class Scenario(Project):
    """Create a new scenario"""
    def __init__(self,project,name='',description = '',output=None):
        """create an scenario"""
        if debug == 2:
            print
            print "........... SCENARIO created ..........."
            print
        if output == '':
            output = ['OSC' , 1]
        if description == '':
            description = "write a comment"
        if name == '':
            name = timestamp(format='nice')
        self.name=name
        self._project = project
        self.output=output
        self.description=description
        self.event_list = []

    def getinstances(self):
        """return a list of all scenarios for this project""" 
        return self.project.scenario_list

    def events(self):
        """return a list of events for this scenario"""
        return Event.getinstances(self)

    def new_event(self,*args,**kwargs):
        """create a new event for this scenario"""
        taille = len(self.event_list)
        the_event = None
        self.event_list.append(the_event)
        self.event_list[taille] = Event(self)
        for key, value in kwargs.iteritems():
            setattr(self.event_list[taille], key, value)
        return self.event_list[taille]

    def del_event(self,index):
        """delete an event, by index or with object instance"""
        if type(index) == int:
            self.event_list.pop(index)
        else:
            self.event_list.remove(index)

    def play_from_here(self,index):
        """play scenario from a given index"""
        index = self.event_list.index(index)
        self.play(index)

    def play(self,index=0):
        """play a scenario from the beginning"""
        """play an scenario
        Started from the first event if an index has not been provided"""
        if debug : print '------ PLAY SCENARIO :' , self.name , 'FROM INDEX' , index , '-----'
        for event in self.events()[index:]:
            event.play()
        return self.name , 'play done'

    def getoutput(self):
        """get the output object for this scenario"""
        if self.output:
            out_protocol = self.output[0]
            out_index = self.output[1] - 1
            out_list = []
            for out in self._project.outputs():
                if out.getprotocol() == out_protocol:
                    out_list.append(out)
            if len(out_list) > out_index:
                output = out_list[out_index]
            else:
                output = None
        else:
            output = None
        return output

class Event(object):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, scenario,content=[],name='',description='',output=''):
        if debug == 2:
            print
            print "........... Event created ..........."
            print
        if description == '':
            description = "event's description"
        if name == '':
            name = 'untitled event'
        if content == []:
            content = ['no content for this event']
        self.name=name
        self.scenario = scenario
        self.description=description
        self.content = content
        self.output = 'parent'
        
    @staticmethod
    def getinstances(scenario):
        """return a list of events for a given scenario"""
        return scenario.event_list

    def play(self):
        """play the current event"""
        if type(self.content) is int or type(self.content) is float:
            wait = float(self.content)
            wait = wait/1000
            if debug : print 'waiting' , wait
            sleep(wait)
        else:
            out = self.getoutput()
            if out.getprotocol() == 'OSC':
                address = self.content[0]
                args = self.content[1:]
                ip = out.ip
                port = out.udp
                for arg in args:
                    try:
                        if debug : 
                            print 'connecting to : ' + ip + ':' + str(port)
                        client.connect((ip , int(port)))
                        msg = OSCMessage()
                        msg.setAddress(address)
                        msg.append(arg)
                        client.send(msg)
                        sleep(0.001)
                        msg.clearData()
                    except OSCClientError :
                        print 'Connection refused'
            elif out.getprotocol() == 'PJLINK':
                try:
                    sock = socket()
                    sock.connect((out.ip, out.udp))
                    f = sock.makefile()
                    proj = Projector(f)
                    proj.authenticate(lambda:'admin')
                    command = self.content[0]
                    value = self.content[1:]
                    if command == 'POWR':
                        proj.set_power(value)
                    elif command == 'INPT':
                        proj.set_input(value)
                    elif command == 'AVMT':
                        proj.set_mute(value)
                    else:
                        'print PJLINK command' , command , 'is not implemented ('+value+')'
                except socket_error:
                    print 'Connection refused'
            else:
                print 'protocol' , out.getprotocol() , 'is not yet implemented'

    def getoutput(self):
        """rerurn the current output for this event.
        If no output is set for this event,
        parent scenario output will be used"""
        if self.output == 'parent':
            output = self.scenario.output
        else:
            output = self.output
        if output:
            protocol = output[0]
            output = output[1] - 1
            output = self.scenario._project.outputs(protocol)[output]
        return output

class Output(Project):
    """Create a new output"""
    def __init__(self,project,protocol='OSC',name='no-name'):
        if debug == 2:
            print
            print "........... OUTPUT created ..........."
            print
        self._protocol = protocol
        self._project = project
        self.name = name
        if protocol == 'OSC':
            osc = OSC()
            self.ip = osc.ip
            self.udp = osc.udp
        if protocol == 'PJLINK':
            pjlink = PJLINK()
            self.ip = pjlink.ip
            self.udp = pjlink.udp
        if protocol == 'MIDI':
            midi = MIDI()
            self.port = midi.port
            self.channel = midi.channel
            self.type = midi.type

    @staticmethod
    def getinstances(project):
        """return a list of outputs for a given project"""
        return project.output_list

    @staticmethod
    def protocols():
        return ['OSC','MIDI','PJLINK']

    def getprotocol(self):
        return self._protocol

    def getproject(self):
        return self._project

    def vars_(self):
        # make a copy
        attrs = list(vars(self).keys())
        for attr in attrs:
            if attr.startswith('_'):
                attrs.remove(attr)
        return attrs


class OSC(Output):
    """Create an OSC output"""
    def __init__(self,ip='127.0.0.1',udp =10000):
        if debug == 2:
            print
            print "........... OSC OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

class PJLINK(Output):
    """Create a PJLINK output"""
    def __init__(self,ip='10.0.0.10',udp =4352):
        if debug == 2:
            print
            print "........... PJLINK OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

class MIDI(Output):
    """Create a MIDI output"""
    def __init__(self,port=0,channel=0,midi_type='CC'):
        if debug == 2:
            print
            print "........... MIDI OUTPUT created ..........."
            print
        self.port = port
        self.channel=channel
        self.type = midi_type
