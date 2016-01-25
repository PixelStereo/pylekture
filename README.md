# pydular
=====
####Python Modular framework for real-time inter-media applications
---------------------------------------------------------------

**This is an alpha version - Do not use it for production, because API must changes a lot before release**

----------------------------------------------------

**pydular** can be defined as a framework for creating applications for real-time intermedia
that can be easily accessed through OSC (Open Sound Control) messages.
It offers a way to organise your application hierarchicaly and creating events and scenario.

----------------------------------------------------

For the moment, **pydular** is will be capable of:

-  Creating application with parameters organised hierarchicaly
-  ~~Navigate and access your app through OSC protocol~~
-  Create dynamic scenario and events
-  Save projects to json files

####Development
Development is made on OSX with python 2.7.11    
Continious integration is made on linux for python 2 and 3, and on appveyor too.    

####Roadmap
Roadmap is available [on this page]((../../wiki/roadmap)

####Tests & Continious Integration
[![Code Climate](https://codeclimate.com/github/PixelStereo/pydular/badges/gpa.svg)](https://codeclimate.com/github/PixelStereo/pydular)
[![Coverage Status](https://coveralls.io/repos/github/PixelStereo/pydular/badge.svg?branch=master)](https://coveralls.io/github/PixelStereo/pydular?branch=master)
[![Issue Count](https://codeclimate.com/github/PixelStereo/pydular/badges/issue_count.svg)](https://codeclimate.com/github/PixelStereo/pydular)
[![Build Status](https://travis-ci.org/PixelStereo/pydular.svg?branch=master)](https://travis-ci.org/PixelStereo/pydular)

####Documentation

Documentation is available online [on this page](http://pixelstereo.github.io/pydular) thanks to @Syntaf for [his nice script](https://github.com/Syntaf/travis-sphinx)

If you need/want to build the documentation from the repo, here are the steps : 

    pip install sphinx
    cd docs/source
    make html
