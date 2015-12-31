#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import random
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
# test will create events each time we create a scenario
test = True

# this is not the best way to do.
#But if i don't do that, I can't create scenario objects 
# because when I call Scenario.getinstances(), the instances list is empty
project_list = []
scenario_list = []
event_list = []
output_list = []

def new_project():
    """Create a new project"""
    taille = len(project_list)
    the_project = None
    project_list.append(the_project)
    project_list[taille] = Project()
    return project_list[taille]

def projects():
    """return a list of projects available"""
    return project_list


class Project(object):
    """docstring for Project"""
    def __init__(self):
        super(Project, self).__init__()
        if debug == 2:
            print
            print "........... PROJECT created ..........."
            print 
        self.author = None
        self.version = None
        self.path = None
        self.lastopened = timestamp()

    def reset(self):
        """reset a project by deleting project.attributes, scenarios, outputs and events related"""
        # reset project attributes
        self.author = None
        self.version = None
        self.path = None
        # reset outputs
        for output in self.outputs():
            output_list.remove(output)
        # reset scenarios and events
        for scenario in self.scenarios():
            for event in scenario.events():
                event_list.remove(event)
            scenario_list.remove(scenario)

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
                            for scenario_list in loaded['scenario']:
                                for attribute , value in scenario_list['attributes'].items():
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
        return Scenario.getinstances(self)

    def scenarios_set(self,old,new):
        """Change order of a scenario in the scenario list of the project"""
        s_list = self.scenarios()
        s_temp = s_list[old]
        s_list.pop(old)
        s_list.insert(new,s_temp)
        for scenario in s_list:
            scenario_list.remove(scenario)
        for scenario in s_list:
            scenario_list.append(scenario)

    def outputs(self,protocol='all'):
        """return a list of available output for this project"""
        outs = []
        if protocol == 'all':
            return Output.getinstances(self)
        else:
            for out in Output.getinstances(self):
                if protocol == out.protocol:
                    outs.append(out)
            return outs

    def new_scenario(self,*args,**kwargs):
        """create a new scenario"""
        taille = len(scenario_list)
        the_scenario = None
        scenario_list.append(the_scenario)
        scenario_list[taille] = Scenario(self)
        for key, value in kwargs.iteritems():
            setattr(scenario_list[taille], key, value)
        return scenario_list[taille]

    def new_output(self,*args,**kwargs):
        """create a new output for this project"""
        taille = len(output_list)
        the_output = None
        output_list.append(the_output)
        output_list[taille] = Output(self)
        for key, value in kwargs.items():
            setattr(output_list[taille], key, value)
        return output_list[taille]

    def del_scenario(self,scenario):
        """delete a scenario of this project
        This function will delete events of the scenario"""
        if scenario in scenario_list:
            # delete events of this scenario
            for event in scenario.events():
                scenario.del_event(event)
            # delete the scenario itself
            scenario_list.remove(scenario)
            if debug == 2:
                print 'delete scenario' , scenario , len(scenario_list)
        else:
            if debug == 2:
                print 'ERROR - trying to delete a scenario which not exists in scenario_list' , scenario

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
            if not output.protocol in outputs:
                outputs.setdefault(output.protocol,[])
            outputs[output.protocol].append({'attributes':{'ip':output.ip,'udp':output.udp,'name':output.name}})
        return outputs


class Scenario(Project):
    """Create a new scenario"""
    def __init__(self,project,name='',description = '',output=''):
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
        self.project = project
        self.output=output
        self.description=description
        if test:
            self.new_event(content=['/node/integer',random.randint(65e2,65e3)]),self.new_event(content=random.randint(500,3000)),self.new_event(content=['/node/list',[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]])

    @staticmethod
    def getinstances(project):
        """return a list of scenario for a given project""" 
        instances = []
        for scenario in scenario_list:
            if project == scenario.project:
                instances.append(scenario)
        return instances

    def events(self):
        """return a list of events for this scenario"""
        return Event.getinstances(self)

    def new_event(self,*args,**kwargs):
        """create a new event for this scenario"""
        taille = len(event_list)
        the_event = None
        event_list.append(the_event)
        event_list[taille] = Event(self)
        for key, value in kwargs.iteritems():
            setattr(event_list[taille], key, value)
        return event_list[taille]

    def del_event(self,index):
        """delete an event, by index or with object instance"""
        if type(index) == int:
            event_list.pop(index)
        else:
            event_list.remove(index)

    def play_from_here(self,index):
        """play scenario from a given index"""
        index = event_list.index(index)
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
        """get the default output for this scenario"""
        output = self.output - 1
        output = self.project.outputs()[output]
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
        instances = []
        for event in event_list:
            if scenario == event.scenario:
                instances.append(event)
        return instances

    def play(self):
        """play the current event"""
        if type(self.content) is int or type(self.content) is float:
            wait = float(self.content)
            wait = wait/1000
            if debug : print 'waiting' , wait
            sleep(wait)
        else:
            out = self.getoutput()
            if out.protocol == 'OSC':
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
            elif out.protocol == 'PJLINK':
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
                print 'protocol' , out.protocol , 'is not yet implemented'

    def getoutput(self):
        """rerurn the current output for this event.
        If no output is set for this event,
        parent scenario output will be used"""
        if self.output == 'parent':
            output = self.scenario.output
        else:
            output = self.output
        protocol = output[0]
        output = output[1] - 1
        output = self.scenario.project.outputs(protocol)[output]
        return output


class Output(Project):
    """Create a new output"""
    def __init__(self,project,protocol='OSC',name='no-name'):
        if debug == 2:
            print
            print "........... OUTPUT created ..........."
            print
        self.protocol=protocol
        self.project = project
        self.name = name
        if protocol == 'OSC':
            self.osc = OSC()
            self.ip = self.osc.ip
            self.udp = self.osc.udp
        if protocol == 'PJLINK':
            self.pjlink = PJLINK()
            self.ip = self.pjlink.ip
            self.udp = self.pjlink.udp

    @staticmethod
    def getinstances(project):
        """return a list of outputs for a given project"""
        instances = []
        for output in output_list:
            if project == output.project:
                instances.append(output)
        return instances

class OSC(Output):
    """Create an OSC output"""
    def __init__(self,ip='127.0.0.1',udp =10000):
        if debug == 2:
            print
            print "........... OSC OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

    @staticmethod
    def getinstances(project):
        """return a list of osc outputs for a given project"""
        instances = []
        for output_osc in output_osc_list:
            if project == output_osc.project:
                instances.append(output_osc)
        return instances

class PJLINK(Output):
    """Create a PJLINK output"""
    def __init__(self,ip='10.0.0.10',udp =4352):
        if debug == 2:
            print
            print "........... PJLINK OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

    @staticmethod
    def getinstances(project):
        """return a list of pjlink outputs for a given project"""
        instances = []
        for output_pjlink in output_pjlink_list:
            if project == output_pjlink.project:
                instances.append(output_pjlink)
        return instances

class MIDI(Output):
    """Create a MIDI output"""
    def __init__(self,port=0,channel=0):
        if debug == 2:
            print
            print "........... MIDI OUTPUT created ..........."
            print
        self.port = port
        self.channel=channel

    @staticmethod
    def getinstances(project):
        """return a list of pjlink outputs for a given project"""
        instances = []
        for output_midi in output_midi_list:
            if project == output_midi.project:
                instances.append(output_midi)
        return instances