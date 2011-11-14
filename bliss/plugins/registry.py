#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.pbs import PBSJobAndSDPlugin
from bliss.plugins.local import LocalJobPlugin

# Here is where the plugins are registered
_registry = []

_registry.append({"class"   : LocalJobPlugin,
                  "apis"    : LocalJobPlugin.supported_apis(),
                  "name"    : LocalJobPlugin.plugin_name(),
                  "schemas" : LocalJobPlugin.supported_schemas()})

_registry.append({"class"   : PBSJobAndSDPlugin,
                  "apis"    : PBSJobAndSDPlugin.supported_apis(),
                  "name"    : PBSJobAndSDPlugin.plugin_name(),
                  "schemas" : PBSJobAndSDPlugin.supported_schemas()})

