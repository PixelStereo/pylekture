#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for an Animation of a Parameter

Make a menu for selecting parameter to animate
slider to test/follow interpolation
curve/easing

"""

from PySide6.QtWidgets import QGroupBox, QSpinBox, QGridLayout, QSlider, QPushButton, QLabel
from PySide6.QtCore import Qt, Slot, QRunnable, QThread


class Animation_UI(QGroupBox, QRunnable):
    """
    Animation of a Parameter
    """
    def __init__(self, anim):
        super(Animation_UI, self).__init__()
        self.setTitle('Animation Interface')
        self.anim = anim

        # create UI objects
        self.origin = QSpinBox()
        self.origin.setValue(self.anim.parameter.value)
        self.origin.valueChanged.connect(self.origin_update)

        self.destination = QSpinBox()
        #self.destination.setMaximum(1000)
        self.destination.setValue(self.anim.destination)
        self.destination.valueChanged.connect(self.destination_update)

        self.duration = QSpinBox()
        self.duration.setMaximum(100000)
        self.duration.setValue(self.anim.duration)
        self.duration.valueChanged.connect(self.duration_update)

        self.go = QPushButton()
        self.go.setText('GO')
        self.go.clicked.connect(self.anim.play)

        self.progressbar = QSlider(Qt.Horizontal, self)
        self.progressbar.setMaximum(self.anim.duration)
        self.anim.timing.connect(self.timing)

        self.value = QSlider(Qt.Horizontal, self)
        self.value.setMinimum(self.anim.origin)
        self.value.setMaximum(self.anim.destination)
        self.anim.new_val.connect(self.parameter_update)

        # set the layout
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel('origin'), 0, 0, 1, 1)
        self.layout.addWidget(self.origin, 0, 1, 1, 1)
        self.layout.addWidget(QLabel('destination'), 0, 2, 1, 1)
        self.layout.addWidget(self.destination, 0, 3, 1, 1)
        self.layout.addWidget(QLabel('duration'), 0, 4, 1, 1)
        self.layout.addWidget(self.duration, 0, 5, 1, 1)        
        self.layout.addWidget(self.go, 1, 0, 1, 6)
        self.layout.addWidget(QLabel('timing'), 2, 0, 1, 1)
        self.layout.addWidget(self.progressbar, 2, 1, 1, 5)
        self.layout.addWidget(QLabel('value'), 3, 0, 1, 1)
        self.layout.addWidget(self.value, 3, 1, 1, 5)
        #self.setFixedSize(400, 150)
        self.setLayout(self.layout)

    @Slot(int)
    def timing(self, val):
        self.progressbar.setValue(val)
    
    def origin_update(self, val):
        """
        update origin of the anim
        """
        self.anim.origin = val
        self.value.setMinimum(val)
    
    def destination_update(self, val):
        """
        update destination of the anim
        """
        self.anim.destination = val
        self.value.setMaximum(val)
    
    def duration_update(self, val):
        """
        update duration of the anim
        """
        self.anim.duration = val
        self.progressbar.setMaximum(val)
    
    @Slot(int)    
    def parameter_update(self, val):
        """
        update parameter to be animed
        """
        self.value.setValue(val)

class Animation_UI_Updater(QThread):
    """docstring for Animation_UI_Updater"""
    def __init__(self, arg):
        super(Animation_UI_Updater, self).__init__()
        self.arg = arg

        

class Ramp_UI(Animation_UI, QThread):
    """docstring for Ramp_UI"""
    def __init__(self, args):
        super(Ramp_UI, self).__init__(args)
        self.setTitle('Ramp Interface')
        self.args = args

    def run(self):
        pass
    
class Random_UI(Animation_UI, QThread):
    """docstring for Ramp_UI"""
    def __init__(self, args):
        super(Random_UI, self).__init__(args)
        self.setTitle('Random Interface')
        self.args = args    

    def run(self):
        pass