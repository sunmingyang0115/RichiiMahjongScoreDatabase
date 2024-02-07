#!/usr/bin/python
import os
import subprocess

os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("module/")
code = subprocess.run(["python", "-m", "unittest", "discover"]).returncode
exit(code)