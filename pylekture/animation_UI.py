#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for an Animation of a Parameter

Make a menu for selecting parameter to animate
slider to test/follow interpolation
curve/easing

"""

from PySide6.QtWidgets import QGroupBox, QSpinBox, QGridLayout, QSlider, QPushButton, QLabel
from PySide6.QtCore import Qt


class Animation_UI(QGroupBox):
    """
    Animation of a Parameter
    """
    def __init__(self, ramp):
        super(Animation_UI, self).__init__()
        self.setTitle('Animation Interface')
        self.ramp = ramp

        # create UI objects
        self.origin = QSpinBox()
        self.origin.setValue(self.ramp.parameter.value)
        self.origin.valueChanged.connect(self.origin_update)

        self.destination = QSpinBox()
        #self.destination.setMaximum(1000)
        self.destination.setValue(self.ramp.destination)
        self.destination.valueChanged.connect(self.destination_update)

        self.duration = QSpinBox()
        self.duration.setMaximum(100000)
        self.duration.setValue(self.ramp.duration)
        self.duration.valueChanged.connect(self.duration_update)

        self.go = QPushButton()
        self.go.setText('GO')
        self.go.clicked.connect(self.ramp.play)

        self.progressbar = QSlider(Qt.Horizontal, self)
        self.progressbar.setMaximum(self.ramp.duration)
        self.ramp.timing.connect(self.timing)

        self.value = QSlider(Qt.Horizontal, self)
        self.value.setMaximum(self.ramp.parameter.domain[1])
        self.ramp.new_val.connect(self.parameter_update)

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

    def timing(self, val):
        self.progressbar.setValue(val)
    
    def origin_update(self, val):
        """
        update origin of the ramp
        """
        self.ramp.origin = val
    
    def destination_update(self, val):
        """
        update destination of the ramp
        """
        self.ramp.destination = val
    
    def duration_update(self, val):
        """
        update duration of the ramp
        """
        self.ramp.duration = val
        self.progressbar.setMaximum(val)
    
    def parameter_update(self, val):
        """
        update parameter to be ramped
        """
        self.ramp.parameter.value = val

class Ramp_UI(Animation_UI):
    """docstring for Ramp_UI"""
    def __init__(self, args):
        super(Ramp_UI, self).__init__(args)
        self.setTitle('Ramp Interface')
        self.args = args
    
class Random_UI(Animation_UI):
    """docstring for Ramp_UI"""
    def __init__(self, args):
        super(Random_UI, self).__init__(args)
        self.setTitle('Random Interface')
        self.args = args    
