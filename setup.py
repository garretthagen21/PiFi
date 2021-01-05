#!/usr/bin/env python
from setuptools import setup
import os
import sys

__doc__ = """Command line tool and library wrapper around '/etc/wpa_supplicant/wpa_supplicant.conf'"""

version = '0.5.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'setuptools',
    'ifconfig-parser==0.0.5'
]
try:
    import argparse
except:
    install_requires.append('argparse')



should_install_cli = os.environ.get('PIFI_INSTALL_CLI') not in ['False', '0']
command_name = os.environ.get('PIFI_CLI_NAME', 'pifi')

if command_name == 'pifi.py':
    print(
        "Having a command name of pifi.py will result in a weird ImportError"
        " that doesn't seem possible to work around. Pretty much any other"
        " name seems to work though."
    )
    sys.exit(1)

entry_points = {}
data_files = []

if should_install_cli:
    entry_points['console_scripts'] = [
        '{command} = pifi.cli:main'.format(command=command_name),
    ]
    # make sure we actually have write access to the target folder and if not don't
    # include it in data_files
    if os.access('/etc/bash_completion.d/', os.W_OK):
        data_files.append(('/etc/bash_completion.d/', ['extras/pifi-completion.bash']))
    else:
        print("Not installing bash completion because of lack of permissions.")
long_desc = ''.join([read('README.rst'), read('CHANGES.rst')])
setup(
    name='pifi',
    version=version,
    author='Garrett Hagen, Rocky Meza, Gavin Wahl',
    author_email='garretthagen21@gmail.com',
    description=__doc__,
    url='https://github.com/garretthagen21/PiFi.git',
    long_description_content_type='text/x-rst',
    long_description='\n\n'.join([read('README.rst'), read('CHANGES.rst')]),
    packages=['pifi'],
    entry_points=entry_points,
    test_suite='tests',
    platforms=["Debian"],
    license='BSD',
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Topic :: System :: Networking",
        "Operating System :: POSIX :: Linux :: Raspbian",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    data_files=data_files
)
