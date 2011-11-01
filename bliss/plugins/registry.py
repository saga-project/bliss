#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.local import localjob
from bliss.plugins.job.gram import gramjob

from bliss.plugins.job import dummyjob

# Here is where the plugins are registered
_registry = []

_registry.append({"class"   : localjob.LocalJobPlugin,
                  "type"    : localjob.LocalJobPlugin.supported_api(),
                  "name"    : localjob.LocalJobPlugin.plugin_name(),
                  "schemas" : localjob.LocalJobPlugin.supported_schemas()})

_registry.append({"class"   : gramjob.GRAMJobPlugin,
                  "type"    : gramjob.GRAMJobPlugin.supported_api(),
                  "name"    : gramjob.GRAMJobPlugin.plugin_name(),
                  "schemas" : gramjob.GRAMJobPlugin.supported_schemas()})


_registry.append({"class"   : dummyjob.DummyJobPlugin,
                  "type"    : dummyjob.DummyJobPlugin.supported_api(),
                  "name"    : dummyjob.DummyJobPlugin.plugin_name(),
                  "schemas" : dummyjob.DummyJobPlugin.supported_schemas()})


