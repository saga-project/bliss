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
        self.plugin_class_list = {}
        self.plugin_instance_list = {}
        
        #iterate thrugh plugin registry
        for plugin in registry._registry:
            self.logger.info("Plugin {!r} found with signature: {!s}".format(plugin["name"], str(plugin)))
            try:
                # see if the plugin can work properly on this system
                plugin["class"].sanity_check()
                self.logger.info("Plugin {!r} internal sanity check passed".format(plugin["name"]))
                # passed. add it to the list
                self.plugin_class_list[str(plugin["schemas"][0])] = plugin["class"]
                self.logger.info("Plugin {!r} add to list as handler for Url schema {!r}".format(plugin["name"], str(plugin["schemas"][0])))


            except Exception, ex:
                self.logger.error("Plugin {!r} sanity check failed: {!s}. Disabled.".format(plugin["name"], str(ex)))

    def get_plugin_for_url(self, url):
        '''Returns a plugin instance for a given url or throws'''
        # first let's check if there's already a plugin-instance active that can handle this url scheme
        if url.scheme in self.plugin_instance_list:
            self.logger.info("Found an existing plugin instance for url scheme {!r}: {!s}".format(str(url.scheme), self.plugin_instance_list[url.scheme]))
            return self.plugin_instance_list[url.scheme]

        elif url.scheme in self.plugin_class_list:                          
            plugin_obj = self.plugin_class_list[url.scheme](url)            
            self.logger.info("Instantiated a new plugin for url scheme {!r}: {!s}".format(str(url.scheme), repr(plugin_obj)))
            self.plugin_instance_list[url.scheme] = plugin_obj
            return plugin_obj
        else:
            error = ("Couldn't find a plugin for url scheme '{!s}://'".format(url.scheme))
            self.logger.error(error)
            raise Exception(error)


        

