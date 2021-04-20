#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
      print("This script requires Python version 3.5 or higher")
      sys.exit(1)
elif sys.version_info[0] == 3 and sys.version_info[1] < 5:
      print("This script requires Python version 3.5 or higher")
      sys.exit(1)

from setuptools import setup

setup(name="YetAnotherProgrammingLanguage",
      packages=["."],
      )