# pydular
=====
Python Modular framework for real-time inter-media applications

**This is an alpha version - Do not use it for production, because API must changes a lot before release**

A framework for creating applications managed through OSC
---------------------------------------------------------

**pydular** can be defined as a framework for creating applications for real-time intermedia
that can be easily accessed through OSC (Open Sound Control) messages.
It offers a way to organise your application hierarchicaly and creating events and scenario.

OK, I think I get the idea, but what is it good for?
----------------------------------------------------

For the moment, **PyProjekt** is capable of:

-  Creating application with parameters organised hierarchicaly
-  Navigate and access your app through OSC prootocol
-  Create dynamic scenario and events
-  Save projects to json files

[![Code Climate](https://codeclimate.com/github/PixelStereo/PyProjekt/badges/gpa.svg)](https://codeclimate.com/github/PixelStereo/PyProjekt)
[![Coverage Status](https://coveralls.io/repos/github/PixelStereo/PyProjekt/badge.svg?branch=master)](https://coveralls.io/github/PixelStereo/PyProjekt?branch=master)
[![Issue Count](https://codeclimate.com/github/PixelStereo/PyProjekt/badges/issue_count.svg)](https://codeclimate.com/github/PixelStereo/PyProjekt)
[![Build Status](https://travis-ci.org/PixelStereo/PyProjekt.svg?branch=master)](https://travis-ci.org/PixelStereo/PyProjekt)

Build Documentation
=======================

    pip install sphinx
    cd doc
    make html
