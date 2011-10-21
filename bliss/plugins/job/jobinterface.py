#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.pluginbase import _PluginBase
from bliss.plugins.pluginbase import _api_type_saga_job

class _JobPluginBase(_PluginBase):
    '''Abstract base class for all job plugins'''
    
    def __init__(self, name):
        '''Class constructor'''
        _PluginBase.__init__(name=name)
    
    @classmethod
    def supported_api(self):
        '''Implements interface from _PluginBase'''
        return _api_type_saga_job