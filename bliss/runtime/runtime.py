# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import os
import logging
import bliss.plugins.registry

def _dyn_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class Runtime:
    '''Implements the Bliss runtime system'''


    def __init__(self):
        '''Constructs a runtime object'''

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

        ## set up the bliss base logger
        ##
        log = logging.getLogger('bliss')
        log.setLevel(self.loglevel)
        formatter = logging.Formatter(fmt='%(asctime)s %(name)s: [%(levelname)s] %(message)s', 
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        log.addHandler(handler)

        address=str(hex(id(self)))
        self.logger = logging.getLogger('bliss.'+self.__class__.__name__)#+'('+address+')') 
        self.logger.debug("BLISS runtime instance created at %s" % address)
        self.plugin_class_list = {}
        self.plugin_instance_list = {}
        
        #iterate thrugh plugin registry
        for plugin in bliss.plugins.registry._registry:

            try:
                # first step -- make sure the plug-in has been
                # registered correctly and defines a mandatory 
                # set of attributes
                module_str = plugin['module']
                class_str  = plugin['class']
                self.logger.debug("Loading plug-in '%s.%s'" % (module_str, class_str))
            except Exception, ex:
                self.logger.error("Error inspecting plug-in registry entry '%s': %s. Skipping." % (plugin, ex))
                continue # continue with next plug-in
            try:
                _module = __import__(module_str, fromlist=[class_str])
                _plugin_class = getattr(_module, class_str)
            except Exception, ex:
                self.logger.error("Error loading plug-in class '%s.%s': %s. Skipping." % (module_str, class_str, ex))
                continue # continue with next plug-in

            # at this point, we have managed to load the plugin class 
            # successfully. however, other things can still go wrong:
            try:
                _plugin_name    = _plugin_class.plugin_name()
                _plugin_schemas = _plugin_class.supported_schemas()
                _plugin_apis    = _plugin_class.supported_apis()
                self.logger.info("Found plugin '%s' supporting URL schmemas %s and API type(s) %s" \
                  % (_plugin_name, _plugin_schemas, _plugin_apis))
            
            except Exception, ex:
                self.logger.error("Error loading plug-in information for '%s.%s': %s. Skipping." % (module_str, class_str, ex))
                continue # continue with next plug-in

            try:
                # see if the plugin can work properly on this system
                _plugin_class.sanity_check()
                self.logger.debug("Plugin %s internal sanity check passed" % (_plugin_name))

                # passed. add it to the list
                for schema in _plugin_schemas:
                    if schema in self.plugin_class_list:
                        self.plugin_class_list[schema].append(_plugin_class)
                    else:
                        self.plugin_class_list[schema] = list()
                        self.plugin_class_list[schema].append(_plugin_class)
                    self.logger.info("Registered plugin %s as handler for URL schema %s://" \
                      % (_plugin_name, schema))
            except Exception, ex:
                self.logger.error("Sanity check FAILED for plugin %s: %s. Skipping." \
                  % (_plugin_name, str(ex)))

    def __del__(self):
        '''Deletes runtime object'''
        pass
        #print "runtime -- delete"


    def get_plugin_for_url(self, url, apitype):
        '''Returns a plugin instance for a given url or throws'''
        # first let's check if there's already a plugin-instance active that can handle this url scheme
        if url.scheme in self.plugin_instance_list:
            for plugin_obj in self.plugin_instance_list[url.scheme]:
                if apitype in plugin_obj.supported_apis:                       
                    self.logger.debug("Found an existing plugin instance for url scheme %s://: %s" \
                      % (str(url.scheme), self.plugin_instance_list[url.scheme]))
                    return plugin_obj

        if url.scheme in self.plugin_class_list:
            for plugin in self.plugin_class_list[url.scheme]:
                plugin_obj = plugin(url)
                if apitype in plugin_obj.__class__.supported_apis():                       
                    self.logger.debug("Instantiated plugin '%s' for URL scheme %s:// and API type '%s'" \
                      % (plugin_obj.name, str(url.scheme), apitype))

                    if url.scheme in self.plugin_instance_list: 
                        self.plugin_instance_list[url.scheme].append(plugin_obj)
                    else:
                        self.plugin_instance_list[url.scheme] = list()
                        self.plugin_instance_list[url.scheme].append(plugin_obj)

                    return plugin_obj

        # Only reached if both conditions above failed
        error = ("Couldn't find a plugin for URL scheme '%s://' and API type '%s'" % (url.scheme, apitype))
        self.logger.error(error)
        raise Exception(error)


        

