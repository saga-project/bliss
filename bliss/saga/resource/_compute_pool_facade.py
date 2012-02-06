
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga._object_impl import Object 

class ComputePool(Object):

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) resource pool.
        '''
        Object.__init__(self, Object.ResourceComputeResourcePool, 
                        apitype=Object.ResourceAPI, session=session)

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))
