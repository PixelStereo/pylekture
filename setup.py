
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), 'rb') as f:
    long_description = f.read()

setup(
  name = 'pyprojekt',
  packages = ['pyprojekt'], 
  version = '0.1.4',
  description = 'A projekt management library',
  author = 'Pixel Stereo',
  install_requires=['PyOSC','pjlink'],
  url='https://github.com/PixelStereo/PyProjekt', 
  download_url = 'https://github.com/PixelStereo/PyProjekt/tarball/0.1.4', 
  classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
