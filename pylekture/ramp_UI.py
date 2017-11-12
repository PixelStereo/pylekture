#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for Ramp

Make a menu for selecting parameter to animate
SpinBox for origin, destination and duration
progressbar
slider to check
curve/easing

"""

from PyQt5.QtWidgets import QGroupBox, QSpinBox, QGridLayout, QProgressBar, QPushButton

class Ramp_UI(QGroupBox):
    """docstring for Ramp_UI"""
    def __init__(self, ramp):
        super(Ramp_UI, self).__init__()
        self.setTitle('Ramp Interface')
        self.ramp = ramp

        # create UI objects
        self.origin = QSpinBox()
        self.origin.setValue(self.ramp.parameter.value)

        self.destination = QSpinBox()
        self.destination.setMaximum(1000)
        self.destination.setValue(self.ramp.destination)

        self.duration = QSpinBox()
        self.duration.setMaximum(100000)
        self.duration.setValue(self.ramp.duration)

        self.go = QPushButton()
        self.go.clicked.connect(self.ramp.play)

        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(2000)
        self.progressbar.setValue(1000)

        # set the layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.origin, 0, 0)
        self.layout.addWidget(self.destination, 0, 1)
        self.layout.addWidget(self.duration, 1, 0)
        self.layout.addWidget(self.go, 1, 1)
        self.layout.addWidget(self.progressbar, 2, 0, 2, 2)
        self.setLayout(self.layout)
