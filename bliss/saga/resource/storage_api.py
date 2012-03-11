# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga                       import Url
from bliss.saga.resource.resource_api import Resource as SResource

class Storage(SResource):

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new storage resource.
        '''
        Object.__init__(self, Object.ResourceStorageResource, 
                        apitype=Object.ResourceAPI, session=session)


    ######################################################################
    ##
    #  FIXME: not sure if that should be overloaded or not...
    def __init_from_manager(self, manager_obj, storage_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._storage_description = storage_description

        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


    ######################################################################
    ##
    # FIXME: Ole, in the spec, the storage resource IS-A filesystem, so
    # get_filesystem() is not needed -- the instance can simply be casted into
    # a filesystem. I am not sure how that is rendered in Python -- I would
    # of course also simply inherit this resource type from filesystem.dir -- 
    # that seems much cleaner than re-implementing the whole filesystem
    # API/CPI...
    #
    def get_filesystem(self): 
        '''get access to the storage resource's file system.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.get_filesystem () 

