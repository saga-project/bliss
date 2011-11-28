#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import FilesystemPluginInterface

from bliss.plugins import utils

import time
import bliss.saga

################################################################################
################################################################################

class SSHFilesystemPlugin(FilesystemPluginInterface):
    '''Implements a filesystem plugin that does things via SSH
    '''
    ## Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.file.ssh'

    ## Define supported url schemas
    ## 
    _schemas = ['ssh']

    ## Define apis supported by this adaptor
    ##
    _apis = ['saga.filesystem']


    ######################################################################
    ##
    def __init__(self, url):
        '''Class constructor'''
        FilesystemPluginInterface.__init__(self, name=self._name, schemas=self._schemas)

    ######################################################################
    ##
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        pass

