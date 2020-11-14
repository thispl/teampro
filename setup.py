# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in teampro/__init__.py
from teampro import __version__ as version

setup(
	name='teampro',
	version=version,
	description='TeamPRO Custom App',
	author='TeamPRO',
	author_email='hr@groupteampro.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
