#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import weakref
import simplejson as json
from pydular.functions import timestamp

from pydular.scenario import Scenario
from pydular.output import Output

debug = False

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
    """
    A project handles everything you need. Ouputs and scenarios are all project-relative

    :param <author>: Name of the project author. Default is None
    :param <version>: Name of the project author. Default is None
    :param <lastopened>: Datetime of the last opened date of this project. Default is None
    """

    # used  to make a list of projects 
    _instances = []

    def __init__(self):
        super(Project, self).__init__()
        self._instances.append(weakref.ref(self))
        self.debug = debug
        if self.debug == 2:
            print ()
            print ("........... PROJECT created ...........")
            print ()
        self.author = None
        self.version = None
        self.path = None
        self.lastopened = None
        self.created = timestamp('nice')
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
        self.output_list = []
        # reset scenarios and events
        self.scenario_list = []

    def read(self,path) : 
        """open a lekture project"""
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print ("ERROR - THIS PATH IS NOT VALID" , path)
            return False
        else :
            print ('loading' , path)
            try:
                with open(path) as in_file :
                    # clear the project
                    self.reset()
                    if self.debug : print ('file reading : ' , path)
                    loaded = json.load(in_file)
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
                            self.lastopened = timestamp('nice')
                        elif key == 'outputs' :
                            for protocol in loaded['outputs']:
                                for out in loaded['outputs'][protocol]:
                                    for attribute , value in out['attributes'].items():
                                        if attribute == 'name':
                                            name = value
                                        if attribute == 'ip':
                                            address_ip = value
                                        if attribute == 'udp':
                                            udp = value
                                    self.new_output(protocol,name=name,ip=address_ip,udp=udp)
                    if self.debug : print ('project loaded')
                    self.path = path
            # catch error if file is not valid or if file is not a lekture project
            except (IOError , ValueError):
                if self.debug : print ('error : project not loaded')
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
            out_file = open(unicode(savepath), 'wb')
            project = {}
            project.setdefault('scenario',self.export_scenario())
            project.setdefault('attributes',self.export_attributes())
            project.setdefault('outputs',self.export_outputs())

            out_file.write(json.dumps(project,sort_keys = True, indent = 4,ensure_ascii=False).encode('utf8'))
            if self.debug : print ("file has been written : " , savepath)
            return True
        else:
            return False

    def scenarios(self):
        """return a list of available scenario for this project"""
        return self.scenario_list

    def scenarios_set(self,old,new):
        """Change order of a scenario in the scenario list of the project"""
        s_temp = self.scenario_list[old]
        self.scenario_list.pop(old)
        self.scenario_list.insert(new,s_temp)

    def outputs(self,protocol='all'):
        """return a list of available output for this project"""
        outs = []
        if protocol == 'all' or protocol == None:
            return Output.getinstances(self)
        else:
            for out in self.output_list:
                if out:
                    if protocol == out.getprotocol():
                        outs.append(out)
            return outs

    def getprotocols(self):
        protocols = []
        for out in self.outputs():
            proto = out.getprotocol()
            if not proto in protocols: 
                protocols.append(proto)
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
            if self.debug == 2:
                print ('delete scenario' , scenario , len(self.scenario_list))
        else:
            if self.debug == 2:
                print ('ERROR - trying to delete a scenario which not exists in self.scenario_list' , scenario)

    def export_attributes(self):
        """export attributes of the project"""
        attributes = {'author':self.author,'version':self.version,'lastopened':self.lastopened}
        return attributes
    
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