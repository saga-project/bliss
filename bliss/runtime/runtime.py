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
        self.logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')') 
        self.logger.info("BLISS runtime instance created at {!r}".format(str(hex(id(self)))))
        self.plugin_list = {}
        
        #iterate thrugh plugin registry
        for plugin in registry._registry:
            self.logger.info("Plugin {!r} found with signature: {!s}".format(plugin["name"], str(plugin)))
            try:
                # see if the plugin can work properly on this system
                plugin["class"].sanity_check()
                self.logger.info("Plugin {!r} internal sanity check passed".format(plugin["name"]))
                # passed. add it to the list
                self.plugin_list[str(plugin["schemas"][0])] = plugin["class"]
                self.logger.info("Plugin {!r} add to list as handler for Url schema {!r}".format(plugin["name"], str(plugin["schemas"][0])))


            except Exception, ex:
                self.logger.error("Plugin {!r} sanity check failed: {!s}. Disabled.".format(plugin["name"], str(ex)))

    def find_plugin_for_url(self, url):
        '''Returns a plugin object for a given url'''
        
        # see if we can find a plugin  that works
        if url.scheme in self.plugin_list:                          
            self.logger.info("Found a plugin for url scheme {!r}: {!s}".format(str(url.scheme), self.plugin_list[url.scheme]))
            plugin_obj = self.plugin_list[url.scheme]
            return plugin_obj()
        else:
            self.logger.error("Couldn't find a plugin for url scheme {!r}".format(url.scheme))
            raise Exception("No Plugin available for Url scheme {!r}".format(url.scheme))


        

