
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
  name = 'pyprojekt',
  packages = ['pyprojekt'], 
  version = '0.1.6',
  description = 'A projekt management library',
  author = 'Pixel Stereo',
  install_requires=['PyOSC','pjlink'],
  url='https://github.com/PixelStereo/PyProjekt', 
  download_url = 'https://github.com/PixelStereo/PyProjekt/tarball/0.1.6', 
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
