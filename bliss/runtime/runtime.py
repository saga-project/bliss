#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging
from bliss.plugins import registry

class _Runtime():
    '''Implements the Bliss runtime system'''
    def __init__(self):
        '''Constructs a runtime object'''
        logging.basicConfig(level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p',
                    	    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.info("Runtime logger started")
        
        #iterate thrugh plugin registry
        for plugin in registry._registry:
            self.logger.info("Plugin {!r} found with signature: {!s}".format(plugin["name"], str(plugin)))
            try:
                # see if the plugin can work properly on this system
                plugin["class"].sanity_check()
                self.logger.info("Plugin {!r} sanity check passed".format(plugin["name"]	))
            except Exception, ex:
                self.logger.error("Plugin {!r} sanity check failed: {!s}".format(plugin["name"], str(ex)))

