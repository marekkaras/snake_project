# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from glob import glob

setup(
      name="snake_project",
      version="1.0.0",
      author="Marek Karas",
      description="Project Game AI",
      packages=find_packages(),
      scripts=glob("bin/*"),
      include_package_data=True
      )