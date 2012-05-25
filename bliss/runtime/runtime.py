# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import os
import logging
import bliss.plugins.registry

class Runtime:
    '''Implements the Bliss runtime system'''

    def __init__(self):
        '''Constructs a runtime object'''

        #BLISS_VERBOSE = int(os.getenv('BLISS_VERBOSE'))
        try: 
            SAGA_VERBOSE = int(os.getenv('SAGA_VERBOSE'))
        except Exception:
            SAGA_VERBOSE = 0

        # 4 = DEBUG + INFO + WARNING + ERROR
        if SAGA_VERBOSE >= 4:
            self.loglevel = logging.DEBUG
        # 3 = INFO + WARNING + ERROR
        elif SAGA_VERBOSE == 3:
            self.loglevel = logging.INFO
        # 2 = WARNING + ERROR 
        elif SAGA_VERBOSE == 2:
            self.loglevel = logging.WARNING
        # 1 = ERROR ONLY
        elif SAGA_VERBOSE == 1:
            self.loglevel = logging.ERROR
        # 0 = No Logging
        else:
            self.loglevel = logging.CRITICAL
  
        logging.basicConfig(level=self.loglevel, datefmt='%m/%d/%Y %I:%M:%S %p',
                    	    format='%(asctime)s - bliss.%(name)s - %(levelname)s - %(message)s')
        address=str(hex(id(self)))
        self.logger = logging.getLogger(self.__class__.__name__+'('+address+')') 
        self.logger.info("BLISS runtime instance created at %s" % address)
        self.plugin_class_list = {}
        self.plugin_instance_list = {}
        
        #iterate thrugh plugin registry
        for plugin in bliss.plugins.registry._registry:
            self.logger.info("Found plugin %s supporting URL schmemas %s and API type(s) %s" \
              % (plugin["name"], plugin['schemas'], plugin['apis']))
            try:
                # see if the plugin can work properly on this system
                plugin["class"].sanity_check()
                self.logger.info("Plugin %s internal sanity check passed" \
                  % (plugin["name"]))
                # passed. add it to the list
                for schema in plugin["schemas"]:
                    self.plugin_class_list[schema] = plugin["class"]
                    self.logger.info("Registered plugin %s as handler for URL schema %s://" \
                      % (plugin["name"], schema))
            except Exception, ex:
                self.logger.error("Sanity check FAILED for plugin %s: %s. Disabled." \
                  % (plugin["name"], str(ex)))

    def __del__(self):
        '''Deletes runtime object'''
        print "runtime -- delete"


    def get_plugin_for_url(self, url, apitype):
        '''Returns a plugin instance for a given url or throws'''
        # first let's check if there's already a plugin-instance active that can handle this url scheme
        if url.scheme in self.plugin_instance_list:
            self.logger.info("Found an existing plugin instance for url scheme %s://: %s" \
              % (str(url.scheme), self.plugin_instance_list[url.scheme]))

            return self.plugin_instance_list[url.scheme]

        elif url.scheme in self.plugin_class_list:
            plugin_obj = self.plugin_class_list[url.scheme](url)
            if apitype in plugin_obj.__class__.supportedExceptions():                       
                self.logger.info("Instantiated plugin '%s' for URL scheme %s:// and API type '%s'" \
                  % (plugin_obj.name, str(url.scheme), apitype))
                self.plugin_instance_list[url.scheme] = plugin_obj
                return plugin_obj

        # Only reached if both conditions above failed
        error = ("Couldn't find a plugin for URL scheme '%s://' and API type '%s'" % (url.scheme, apitype))
        self.logger.error(error)
        raise Exception(error)


        

