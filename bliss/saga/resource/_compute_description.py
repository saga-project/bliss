#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga._object_impl import Object
from bliss.saga._attributes_impl import AttributeInterface

class ComputeDescription(Object, AttributeInterface):
    '''Loosely defines a SAGA Resource description as defined in GWD-R.xx
    '''

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) compute resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)
        AttributeInterface.__init__(self)

        self._start          = None
        self._end            = None
        self._duration       = None

        self._machine_os     = None
        self._machine_arch   = None
        self._hostnames      = None
        self._cores          = None # total or per machine? 
        self._memory         = None # total or per machine?

        # register properties with the attribute interface
        self._register_rw_attribute     (name="Start", 
                                         accessor=self.__class__.start) 
        self._register_rw_attribute     (name="End", 
                                         accessor=self.__class__.end) 
        self._register_rw_attribute     (name="Duration", 
                                         accessor=self.__class__.duration) 

        self._register_rw_vec_attribute (name="MachineOS", 
                                         accessor=self.__class__.machine_os) 
        self._register_rw_vec_attribute (name="MachineArch", 
                                         accessor=self.__class__.machine_arch)
        self._register_rw_vec_attribute (name="Hostnames", 
                                         accessor=self.__class__.hostnames)
 
        self._register_rw_attribute     (name="Cores", 
                                         accessor=self.__class__.cores)
        self._register_rw_attribute     (name="Memory", 
                                         accessor=self.__class__.memory) 


    ######################################################################
    ## 
    def __del__(self):
        '''Delete this resource description.'''
        # nothing to do here 
        pass

    def __str__(self):
        '''String representation.'''
        result = str("{")
        for attribute in self.list_attributes():
            if self.attribute_is_vector(attribute):
                value = repr(self.get_vector_attribute(attribute))
            else:
                value = str(self.get_attribute(attribute))
            result += str("'%s' : '%s'," % (str(attribute), value))
        result += "}"
        return result
        

    ######################################################################
    ## Property 
    def start():
        doc = "Required start time for this resource reservation."
        def fget(self):
            return self._start
        def fset(self, val):
            self._start = val
        def fdel(self, val):
            self._start = None
        return locals()
    start = property(**start())
      
    ######################################################################
    ## Property 
    def end():
        doc = "Required end time for this resource reservation."
        def fget(self):
            return self._end
        def fset(self, val):
            self._end = val
        def fdel(self, val):
            self._end = None
        return locals()
    end = property(**end())

    ######################################################################
    ## Property 
    def duration():
        doc = "Required duration for this resource reservation."
        def fget(self):
            return self._duration
        def fset(self, val):
            self._duration = val
        def fdel(self, val):
            self._duration = None
        return locals()
    duration = property(**duration())

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
