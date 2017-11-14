#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of a ramp UI
"""



from pylekture.project import new_project

from pyossia import ossia

my_device = ossia.LocalDevice('PyOssia Test Device')
my_device.expose(protocol='osc', listening_port=3456, sending_port=5678, logger=True)
my_int = my_device.add_param('test/numeric/int', value_type='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.add_param('test/numeric/float', value_type='float', default_value=0.123456, domain=[-2.1, 2.2])

my_project = new_project(name= 'Demo Project')
a_ramp = my_project.new_event('ramp', parameter=my_int, name='event 1', description='my first event', destination=200, duration=2000)
a_random = my_project.new_event('random', parameter=my_float, name='event 2', description='my second event', destination=1, duration=2000)


from pylekture.ramp_UI import Ramp_UI
from pylekture.random_UI import Random_UI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    """
    Main Window Doc String
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAutoFillBackground(True)
        self.rampui = Ramp_UI(a_ramp)
        self.randomui = Random_UI(a_random)
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
    sys.exit(app.exec_())
