#!/usr/bin/env python

from distutils.core import setup
import shutil

shutil.copyfile('timecard.py', 'tc')

setup(name='timecard', scripts=['tc'])
