# !/usr/bin/env python
# coding: utf-8

import os
import sys

from setuptools import setup

from saviour import __version__ as saviour_version

if sys.version_info < (3, 6):
    sys.exit('python 3.6or higher is required for legendary')


setup(
    name='saviour',
    version=saviour_version,
    # license='GPL-3',
    author='youssef',
    author_email='youssefaswad@gmail.com',
    packages=[
        'saviour',
    ],
    entry_points=dict(
        console_scripts=['saviour = saviour.cli:main']
    ),
    # install_requires=[
    #     'requests<3.0',
    #     'setuptools',
    #     'wheel'
    # dateutil
    # ],
    url='https://github.com/youssefaswad/saviour',
    # description='Free and open-source replacement for the Epic Games Launcher application',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # python_requires='>=3.6',
    # classifiers=[
    #     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3.9',
    #     'Operating System :: POSIX :: Linux',
    #     'Operating System :: Microsoft',
    #     'Intended Audience :: End Users/Desktop',
    #     'Topic :: Games/Entertainment',
    #     'Development Status :: 4 - Beta',
    # ]
)
