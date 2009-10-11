#!/usr/bin/env python

from distutils.core import setup

import funpy

setup(name='funpy',
      version='.'.join(map(str, funpy.__version__)),
      description='A library for functional programming in Python',
      author='Nicolas Trangez',
      author_email='eikke eikke com',
      packages=['funpy', ],
      license='LGPL-2.1',
     )
