#!/usr/bin/python
import os
import unittest

os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("module/")
os.system("python -m unittest discover")