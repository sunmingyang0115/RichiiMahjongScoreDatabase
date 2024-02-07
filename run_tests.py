#!/usr/bin/python
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("module/")
exitcode = os.system("python -m unittest discover")
exit(exitcode)