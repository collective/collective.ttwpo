# -*- coding: utf-8 -*-
"""Installer for the example.package package."""
from setuptools import setup

setup(
    # thanks to this bug
    # https://github.com/pypa/setuptools/issues/1136
    # we need one line in here:
    package_dir={'': 'src'},
)
