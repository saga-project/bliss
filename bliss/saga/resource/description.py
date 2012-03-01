#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object_api import Object
from bliss.saga.attributes_api import AttributeInterface

class Description(Object, AttributeInterface):
    '''Loosely defines a SAGA Resource description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)
        AttributeInterface.__init__(self)

        self._dynamic        = False
        self._start          = None
        self._end            = None
        self._duration       = None

        # register properties with the attribute interface
        self._register_rw_attribute     (name="Dynamic", 
                                         accessor=self.__class__.dynamic) 
        self._register_rw_attribute     (name="Start", 
                                         accessor=self.__class__.start) 
        self._register_rw_attribute     (name="End", 
                                         accessor=self.__class__.end) 
        self._register_rw_attribute     (name="Duration", 
                                         accessor=self.__class__.duration) 

        # FIXME: how do I signal the attrib interface that the attrib set is
        # extensible?


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

