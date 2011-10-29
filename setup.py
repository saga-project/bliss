#!/usr/bin/env python

"""
Setup script.
"""

import os
import sys
import shutil
import fileinput

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.sdist import sdist

from bliss import version

scripts = [] # ["bin/bliss-run"]

# sdist is usually run on a non-Windows platform, but the buildslave.bat file
# still needs to get packaged.

#if 'sdist' in sys.argv or sys.platform == 'win32':
#    scripts.append("contrib/windows/air-run.bat")
#    scripts.append("contrib/windows/air-flow.bat")

class our_install_data(install_data):

    def finalize_options(self):
        self.set_undefined_options('install',
            ('install_lib', 'install_dir'),
        )
        install_data.finalize_options(self)

    def run(self):
        install_data.run(self)
        # ensure there's a bliss/VERSION file
        fn = os.path.join(self.install_dir, 'bliss', 'VERSION')
        open(fn, 'w').write(version)
        self.outfiles.append(fn)

class our_sdist(sdist):

    def make_release_tree(self, base_dir, files):
        sdist.make_release_tree(self, base_dir, files)
        # ensure there's a air/VERSION file
        fn = os.path.join(base_dir, 'bliss', 'VERSION')
        open(fn, 'w').write(version)

setup_args = {
    'name': "bliss",
    'version': version,
    'description': "A lightweight, 'laissez-faire' implementation of a subset of the OGF SAGA standard (GFD.90).",
    'long_description': "Bliss (BLiss IS SagaA) is a lightweight , 'laissez-faire' implementation of the OGF SAGA standard (GFD.90). Bliss is written 100% in Python and focuses on usability and ease of deployment rather than on feature completeness or blind standard obedience. ",
    'author': "Ole Christian Weidner",
    'author_email': "ole.weidner@me.com",
    'maintainer': "Ole Christian Weidner",
    'maintainer_email': "ole.weidner@me.com",
    'url': "http://oweidner.github.com/bliss/",
    'license': "MIT",
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Distributed Computing',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: AIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: BSD/OS',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: NetBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: GNU Hurd',
        'Operating System :: POSIX :: HP-UX',
        'Operating System :: POSIX :: IRIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Other',
        'Operating System :: POSIX :: SCO',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: Unix'
        ],

    'packages': [
        "bliss",
        "bliss.saga",
        "bliss.saga.job",
        "bliss.runtime",
        "bliss.plugins",
        "bliss.plugins.job",
        "bliss.plugins.job.local"
    ],
    'scripts': scripts,
    # mention data_files, even if empty, so install_data is called and
    # VERSION gets copied
    'data_files': [("bliss", [])],
    'cmdclass': {
        'install_data': our_install_data,
        'sdist': our_sdist
        }
    }

# set zip_safe to false to force Windows installs to always unpack eggs
# into directories, which seems to work better --
# see http://buildbot.net/trac/ticket/907
if sys.platform == "win32":
    setup_args['zip_safe'] = False

try:
    # If setuptools is installed, then we'll add setuptools-specific arguments
    # to the setup args.
    import setuptools #@UnusedImport
except ImportError:
    pass
else:
    setup_args['install_requires'] = [
        #'pika >= 0.9.5',
    ]

    if os.getenv('NO_INSTALL_REQS'):
        setup_args['install_requires'] = None

##
## PROCESS SETUP OPTIONS FOR DIFFERENT BACKENDS
##

# process AIR_AMQP_HOSTNAME and AIR_AMQP_PORT
#air_amqp_hostname = os.getenv('AIR_AMQP_HOST')
#air_amqp_port = os.getenv('AIR_AMQP_PORT')
#
#if not air_amqp_hostname:
#   air_amqp_hostname = "localhost"
#
#print "setting default amqp hostname to '%s' in air/scripts/config.py" % air_amqp_hostname
#
#if not air_amqp_port:
#   air_amqp_port = "5672"
#
#print "setting default amqp port to '%s' in air/scripts/config.py" % air_amqp_port
#
#
#shutil.copyfile("./air/scripts/config.py.in", "./air/scripts/config.py")


#s = open("./air/scripts/config.py.in").read()
#s = s.replace('###REPLACE_WITH_AMQP_HOSTNAME###', str(air_amqp_hostname))
#s = s.replace('###REPLACE_WITH_AMQP_PORT###', str(air_amqp_port))
#f = open("./air/scripts/config.py", 'w')
#f.write(s)
#f.close()


setup(**setup_args)
