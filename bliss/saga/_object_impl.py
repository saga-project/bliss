#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging
import bliss.saga
import bliss.runtime

from bliss.plugins import utils


class Object(object) :
    '''Loosely resembles a SAGA object as defined in GFD.90'''

    BaseAPI              = "saga.base"
    '''Look & Feel API namespace'''
    Url                  = "saga.Url"
    '''saga.Url object type.'''
    Session              = "saga.Session"
    '''saga.Session object type.'''
    Context              = "saga.Context"
    '''saga.Context object type.'''

    JobAPI               = "saga.job"
    '''saga.job API namespace'''
    Job                  = "saga.job.Job"
    '''saga.job.Job object type.'''
    JobService           = "saga.job.Service"
    '''saga.job.Service object type.'''
    JobDescription       = "saga.job.Description"
    '''saga.job.Description object type.'''
    JobContainer         = "saga.job.Container"
    '''saga.job.Container (task container) object type.'''

    SDAPI                = "saga.sd"
    '''saga.sd API namespace'''
    SDDiscoverer         = "saga.sd.Discoverer"
    '''saga.sd.Discoverer object type.'''
    SDServiceDescription = "saga.sd.ServiceDescription"
    '''saga.sd.ServiceDescription object type.'''
    SDServiceData        = "saga.sd.ServiceData"
    '''saga.sd.ServiceData object type.'''

    FilesystemAPI        = "saga.filesystem"
    '''saga.filesystem API namespace'''
    FilesystemFile       = "saga.filesystem.File"
    '''saga.filesystem.File object type'''
    FilesystemDirectory  = "saga.filesystem.Directory"
    '''saga.filesystem.File object type'''

    ResourceAPI                 = "saga.resource"
    '''saga.resource API namespace'''
    ResourceManager             = "saga.resource.Manager"
    '''saga.resource.Manager object type'''
    ResourceComputeDescription  = "saga.resource.ComputeDescription"
    '''saga.resource.Description object type'''
    ResourceCompute             = "saga.resource.Compute"
    '''saga.resource.Compute object type'''
    ResourceComputePool         = "saga.resource.ComputePool"
    '''saga.resource.ComputePool object type'''

    __shared_state = {}
    __shared_state["runtime_initialized"] = False

    __slots__ = ("_plugin", "_type", "_logger", "_session")

    ######################################################################
    ## 
    def __init__(self, objtype, apitype, session=None):
        '''Constructor.'''
 
        if not self.__shared_state["runtime_initialized"]:
            # initialize runtime
            self._init_runtime()
            self.__shared_state["default_session"] = bliss.saga.Session()
            self.__shared_state["runtime_initialized"] = True

        self._plugin = None
        self._type = objtype
        self._apitype = apitype
        self._logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')')
 
        if session is not None:
            self._session = session
        else:
            self._session = self.__shared_state["default_session"]

    ######################################################################
    ## 
    def __del__(self):
        '''Destructor.'''
        pass

    ######################################################################
    ## PRIVATE 
    def _init_runtime(self):
        '''Registers available plugins and so on'''
        if not self.__shared_state["runtime_initialized"]: 
            self.__shared_state["runtime_instance"] = bliss.runtime.Runtime()

    ######################################################################
    ## PRIVATE
    def _get_plugin(self):
        '''Bind an object to the runtime'''
        try:
            return self.__shared_state["runtime_instance"].get_plugin_for_url(self._url, self._apitype) 
        except Exception, ex:
            error = ("%s %s" % (str(ex), utils.get_traceback()))
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, error)

    ######################################################################
    ## PRIVATE 
    def _get_runtime_info(self):
        return self._get_plugin().get_runtime_info()

    ######################################################################
    ## Property: session
    def session():
        doc = "The object's session which contains the list of security context objects."
        def fget(self):
            return self._session
        return locals()
    session = property(**session())

    ######################################################################
    ## Property: type
    def type():
        doc = "The object's type identifier."
        def fget(self):
            return self._type
        return locals()
    type = property(**type())


    ######################################################################
    ## Property: id
    def id():
        doc = "The object's unique identifier."
        def fget(self):
            return ("%s_%s") % (self.__class__.__name__, str(hex(id(self))))
        return locals()
    id = property(**id())

    ######################################################################
    ##
    def get_session(self):
        '''Legacy GFD.90 method: return the object's session.
 
           It is encouraged to use the L{session} property instead.
        '''
        if self.session is None:
            pass # return default session
        else:
           return self.session

    ######################################################################
    ##
    def get_type(self):
        '''Legacy GFD.90 method: return the object type.

           It is encouraged to use the L{type} property instead.
        '''
        return self.type

    ######################################################################
    ##
    def get_id(self):
        '''Legacy GFD.90 method: return the object identifier.

           It is encouraged to use the L{id} property instead.
        '''
        return self.id 

