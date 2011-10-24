#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.jobinterface import _JobPluginBase

class LocalJobPlugin(_JobPluginBase):
    '''Implments a job plugin that can submit jobs to the local machine'''
    
    def __init__(self):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name="saga.plugin.job.local")
    
    @classmethod
    def supported_schemas(self):
        '''Implements interface from _PluginBase'''
        return ['fork']

    @classmethod
    def plugin_name(self):
        '''Implements interface from _PluginBase'''
        return "saga.plugin.job.local"
        
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        # No requirements for this plugin
        return True
