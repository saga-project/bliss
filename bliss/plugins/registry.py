#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.pbs import PBSJobAndSDPlugin
from bliss.plugins.sftp import SFTPFilesystemPlugin
from bliss.plugins.local import LocalJobPlugin
from bliss.plugins.ec2 import EC2JobPlugin
from bliss.plugins.ssh import SSHJobPlugin

#from bliss.plugins.pbsbigjob import PBSBigJobResourcePlugin

_registry = []

_registry.append({"class"   : SSHJobPlugin,
                  "apis"    : SSHJobPlugin.supported_apis(),
                  "name"    : SSHJobPlugin.plugin_name(),
                  "schemas" : SSHJobPlugin.supported_schemas()})

_registry.append({"class"   : EC2JobPlugin,
                  "apis"    : EC2JobPlugin.supported_apis(),
                  "name"    : EC2JobPlugin.plugin_name(),
                  "schemas" : EC2JobPlugin.supported_schemas()})

_registry.append({"class"   : LocalJobPlugin,
                  "apis"    : LocalJobPlugin.supported_apis(),
                  "name"    : LocalJobPlugin.plugin_name(),
                  "schemas" : LocalJobPlugin.supported_schemas()})

_registry.append({"class"   : PBSJobAndSDPlugin,
                  "apis"    : PBSJobAndSDPlugin.supported_apis(),
                  "name"    : PBSJobAndSDPlugin.plugin_name(),
                  "schemas" : PBSJobAndSDPlugin.supported_schemas()})

#_registry.append({"class"   : PBSBigJobResourcePlugin,
#                  "apis"    : PBSBigJobResourcePlugin.supported_apis(),
#                  "name"    : PBSBigJobResourcePlugin.plugin_name(),
#                  "schemas" : PBSBigJobResourcePlugin.supported_schemas()})

_registry.append({"class"   : SFTPFilesystemPlugin,
                  "apis"    : SFTPFilesystemPlugin.supported_apis(),
                  "name"    : SFTPFilesystemPlugin.plugin_name(),
                  "schemas" : SFTPFilesystemPlugin.supported_schemas()})
