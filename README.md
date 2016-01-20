# PyProjekt
=====

Alpha version - Do not use it for production
============================================


A framework for creating applications managed through OSC
---------------------------------------------------------

**PyProjekt** can be defined as a project manager for creating applications
that can be easily accessed through OSC (Open Sound Control) messages.
It offers a way to organise your application hierarchicaly and creating events and scenario.

OK, I think I get the idea, but what is it good for?
----------------------------------------------------

**PyProjekt**'s purpose in life is to make your life a little bit easier by
allowing you organise an application.

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

Change Log
==========

0.1.2
-----
- output attribute of scenario is now a list of two elements [protocol,index]
- add a new method for getting available protocols for a project

Copyright and Licensing
=======================

Copyright (c) Pixel Stereo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software. Every change must be 
submitted to the author. The software cannot be sell or use in any commercial 
application without authorisation.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
