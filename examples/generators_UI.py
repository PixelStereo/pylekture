#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of a ramp UI
"""



from pylekture.project import new_project

from pybush import new_device

my_device = new_device(name='test device', author='Pixel Stereo', version='0.1.0')
osc_output = my_device.new_output(protocol='OSC', port='127.0.0.1:1234')

my_int = my_device.add_param({
                                    'name':'my_int',
                                    'value':8,
                                    'tags':['int', 'no_dot'],
                                    'datatype':'integer',
                                    'domain':[1,35],
                                    'clipmode':'low',
                                    'unique':False})



my_other_int = my_device.add_param({
                                    'name':'my_other_int',
                                    'value':2,
                                    'tags':['int', 'another one without any dot'],
                                    'datatype':'int',
                                    'domain':[-1,1],
                                    'clipmode':'both',
                                    'unique':True})

my_project = new_project(name= 'Demo Project')
a_ramp = my_project.new_event('ramp', parameter=my_int, name='event 1', description='my first event', destination=200, duration=2000)
a_random = my_project.new_event('random', parameter=my_other_int, name='event 2', description='my second event', destination=100, duration=2000)


from pylekture.animation_UI import Animation_UI
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    """
    Main Window Doc String
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAutoFillBackground(True)
        self.rampui = Animation_UI(a_ramp)
        self.randomui = Animation_UI(a_random)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.rampui)
        self.layout.addWidget(self.randomui)
        main_box = QWidget()
        main_box.setLayout(self.layout)
        # assign this device to the mainwindow
        self.setCentralWidget(main_box)
        self.move(0, 40)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
