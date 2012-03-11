#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.pbs import PBSJobAndSDPlugin
from bliss.plugins.sftp import SFTPFilesystemPlugin
from bliss.plugins.local import LocalJobPlugin
from bliss.plugins.pbspilotjob import PBSPilotJobResourcePlugin

_registry = []

_registry.append({"class"   : LocalJobPlugin,
                  "apis"    : LocalJobPlugin.supported_apis(),
                  "name"    : LocalJobPlugin.plugin_name(),
                  "schemas" : LocalJobPlugin.supported_schemas()})

_registry.append({"class"   : PBSJobAndSDPlugin,
                  "apis"    : PBSJobAndSDPlugin.supported_apis(),
                  "name"    : PBSJobAndSDPlugin.plugin_name(),
                  "schemas" : PBSJobAndSDPlugin.supported_schemas()})

_registry.append({"class"   : PBSPilotJobResourcePlugin,
                  "apis"    : PBSPilotJobResourcePlugin.supported_apis(),
                  "name"    : PBSPilotJobResourcePlugin.plugin_name(),
                  "schemas" : PBSPilotJobResourcePlugin.supported_schemas()})

_registry.append({"class"   : SFTPFilesystemPlugin,
                  "apis"    : SFTPFilesystemPlugin.supported_apis(),
                  "name"    : SFTPFilesystemPlugin.plugin_name(),
                  "schemas" : SFTPFilesystemPlugin.supported_schemas()})
