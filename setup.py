
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup,find_packages
setup(
  name = 'pyprojekt',
  packages = ['pyprojekt'], 
  version = '0.1.1',
  description = 'A projekt management library',
  author = 'Pixel Stereo',
  packages=find_packages(),
  include_package_data=True,
  author_email = 'contact@pixelstereo.org',
  url = 'https://github.com/PixelStereo/PyProjekt', 
  download_url = 'https://github.com/PixelStereo/PyProjekt/tarball/0.1.1', 
  keywords = ['modular', 'model', 'parameter' , 'project' , 'projekt'], 
  classifiers = [
    'Development Status :: 1 - draft',
    'Environment :: Application',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GPL',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    ],
)