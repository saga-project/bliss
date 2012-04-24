#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.pbs import PBSJobPlugin
from bliss.plugins.sge import SGEJobPlugin
from bliss.plugins.sftp import SFTPFilesystemPlugin
from bliss.plugins.local import LocalJobPlugin
from bliss.plugins.ssh import SSHJobPlugin

_registry = []

_registry.append({"class"   : LocalJobPlugin,
                  "apis"    : LocalJobPlugin.supportedExceptions(),
                  "name"    : LocalJobPlugin.plugin_name(),
                  "schemas" : LocalJobPlugin.supported_schemas()})

_registry.append({"class"   : PBSJobPlugin,
                  "apis"    : PBSJobPlugin.supportedExceptions(),
                  "name"    : PBSJobPlugin.plugin_name(),
                  "schemas" : PBSJobPlugin.supported_schemas()})

_registry.append({"class"   : SGEJobPlugin,
                  "apis"    : SGEJobPlugin.supportedExceptions(),
                  "name"    : SGEJobPlugin.plugin_name(),
                  "schemas" : SGEJobPlugin.supported_schemas()})

_registry.append({"class"   : SFTPFilesystemPlugin,
                  "apis"    : SFTPFilesystemPlugin.supportedExceptions(),
                  "name"    : SFTPFilesystemPlugin.plugin_name(),
                  "schemas" : SFTPFilesystemPlugin.supported_schemas()})

_registry.append({"class"   : SSHJobPlugin,
                  "apis"    : SSHJobPlugin.supportedExceptions(),
                  "name"    : SSHJobPlugin.plugin_name(),
                  "schemas" : SSHJobPlugin.supported_schemas()})
