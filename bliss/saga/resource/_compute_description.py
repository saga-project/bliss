#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.resource._description import Description as SDescription

class ComputeDescription(SDescription):
    '''Defines a SAGA compute_description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attrib interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) compute resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)

        self._type           = Type.Compute
        self._os             = 'Any'
        self._arch           = 'Any'
        self._hostnames      = None
        self._slots          = 1
        self._memory         = None
        self._access         = None

        # register properties with the attribute interface
        self._register_ro_type          (name="type", 
                                         accessor=self.__class__.res_type)
        self._register_rw_vec_attribute (name="OperatingSystem", 
                                         accessor=self.__class__.operating_system) 
        self._register_rw_vec_attribute (name="Architecture", 
                                         accessor=self.__class__.architecture)
        self._register_rw_vec_attribute (name="Hostnames", 
                                         accessor=self.__class__.hostnames)
        self._register_rw_attribute     (name="Slots", 
                                         accessor=self.__class__.slots)
        self._register_rw_attribute     (name="Memory", 
                                         accessor=self.__class__.memory) 
        self._register_ro_attribute     (name="Access", 
                                         accessor=self.__class__.access) 


    # FIXME: details do not reflect above spec, yet.

    ######################################################################
    ## Property 
    def cores():
        doc = "Required number of cores for this resource reservation."
        def fget(self):
            return self._cores
        def fset(self, val):
            self._cores = val
        def fdel(self, val):
            self._cores = None
        return locals()
    cores = property(**cores())

    ######################################################################
    ## Property 
    def memory():
        doc = "Required amount of memory for this resource reservation."
        def fget(self):
            return self._memory
        def fset(self, val):
            self._memory = val
        def fdel(self, val):
            self._memory = None
        return locals()
    memory = property(**memory())

