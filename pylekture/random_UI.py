#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for Random

Make a menu for selecting parameter to animate
SpinBox for min, max, destination and duration
progressbar
slider to navigate
curve/easing

"""

from PyQt5.QtWidgets import QGroupBox, QSpinBox, QGridLayout, QProgressBar, QPushButton

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