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
