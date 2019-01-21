#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for an Animation of a Parameter

Make a menu for selecting parameter to animate
slider to test/follow interpolation
curve/easing

"""

from PyQt5.QtWidgets import QGroupBox, QSpinBox, QGridLayout, QSlider, QPushButton
from PyQt5.QtCore import Qt


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
        self.destination.setMaximum(1000)
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

        # set the layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.origin, 0, 0)
        self.layout.addWidget(self.destination, 0, 1)
        self.layout.addWidget(self.duration, 1, 0)
        self.layout.addWidget(self.go, 1, 1)
        self.layout.addWidget(self.progressbar, 2, 0, 1, 2)
        self.setFixedSize(200, 150)
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
        self.ramp.parameter = val

"""
random_UI.py file
"""

class Random_UI(QGroupBox):
    """docstring for Ramp_UI"""
    def __init__(self, random):
        super(Random_UI, self).__init__()
        self.setTitle('Random Interface')
        self.random = random

        # create UI objects
        self.origin = QSpinBox()
        self.origin.setValue(self.random.parameter.value)

        self.destination = QSpinBox()
        self.destination.setMaximum(1000)
        self.destination.setValue(self.random.destination)

        self.duration = QSpinBox()
        self.duration.setMaximum(100000)
        self.duration.setValue(self.random.duration)

        self.go = QPushButton()
        self.go.clicked.connect(self.random.play)

        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(200)
        self.random.started.connect(self.progressbar.reset)
        #self.random.new_val.connect(self.progressbar.setValue)
        self.random.new_val.connect(self.popo)

        # set the layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.origin, 0, 0)
        self.layout.addWidget(self.destination, 0, 1)
        self.layout.addWidget(self.duration, 1, 0)
        self.layout.addWidget(self.go, 1, 1)
        self.layout.addWidget(self.progressbar, 2, 0, 2, 2)
        self.setLayout(self.layout)

    def popo(self, val):
        self.progressbar.setValue(val)