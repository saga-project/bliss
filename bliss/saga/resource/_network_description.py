#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.resource._description import Description as SDescription

class NetworkDescription(SDescription):
    '''Defines a SAGA network_description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attrib interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) network resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)

        self._type           = Type.Network
        self._size           = ''
        self._access         = None

        # register properties with the attribute interface
        self._register_ro_type          (name="type", 
                                         accessor=self.__class__.res_type)
        self._register_rw_attribute     (name="Size", 
                                         accessor=self.__class__.size) 
        self._register_ro_attribute     (name="Access", 
                                         accessor=self.__class__.access) 


    # FIXME: details do not reflect above spec, yet.

    ######################################################################
    ## Property 
    def size():
        doc = "Required size of network."
        def fget(self):
            return self._size
        def fset(self, val):
            self._size = val
        def fdel(self, val):
            self._size = None
        return locals()
    cores = property(**size())

