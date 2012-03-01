# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.resource.description import Description as SDescription

class PoolDescription(SDescription):
    '''Defines a SAGA pool_description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attrib interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) pool resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)

        self._type           = Type.Pool
        self._policy         = 'Default'
        self._access         = None

        # register properties with the attribute interface
        self._register_ro_type          (name="type", 
                                         accessor=self.__class__.res_type)
        self._register_rw_attribute     (name="Policy", 
                                         accessor=self.__class__.policy) 
        self._register_ro_attribute     (name="Access", 
                                         accessor=self.__class__.access) 


    # FIXME: details do not reflect above spec, yet.

    ######################################################################
    ## Property 
    def policy():
        doc = "."
        def fget(self):
            return self._policy
        def fset(self, val):
            self._policy = val
        def fdel(self, val):
            self._policy = None
        return locals()
    cores = property(**policy())

