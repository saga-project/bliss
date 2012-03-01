# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object_api import Object
from bliss.saga.attributes_api import AttributeInterface

class ComputeDescription(Object, AttributeInterface):
    '''Defines a SAGA compute_description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attrib interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) compute resource description.'''
        Object.__init__(self, Object.ResourceComputeDescription, 
                        apitype=Object.ResourceAPI,)

        self._type           = Type.Compute
        self._dynamic        = False
        self._start          = None
        self._end            = None
        self._duration       = None

        self._register_ro_type          (name="Type", 
                                             accessor=self.__class__.res_type)
        self._register_rw_attribute     (name="Dynamic", 
                                             accessor=self.__class__.dynamic) 
        self._register_rw_attribute     (name="Start", 
                                             accessor=self.__class__.start) 
        self._register_rw_attribute     (name="End", 
                                             accessor=self.__class__.end) 
        self._register_rw_attribute     (name="Duration", 
                                             accessor=self.__class__.duration) 
        
        self._slots          = 1
        self._memory         = None
        self._hostnames      = None
        self._os             = 'Any'
        self._arch           = 'Any'

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
    
    ######################################################################
    ## 
    def __del__(self):
        '''Delete this resource description.'''
        # nothing to do here 
        pass

    ######################################################################
    ## 
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
    def type():
        doc = "Type..."
        def fget(self):
            return self._type
        return locals()
    type = property(**type())
    
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
    def dynamic():
        doc = "Dynamic or not."
        def fget(self):
            return self._dynamic
        def fset(self, val):
            self._dynamic = val
        def fdel(self, val):
            self._dynamic = None
        return locals()
    dynamic = property(**dynamic())
    
    ######################################################################
    ## Property 
    def slots():
        doc = "Required number of cores for this resource reservation."
        def fget(self):
            return self._slots
        def fset(self, val):
            self._slots = val
        def fdel(self, val):
            self._slots = None
        return locals()
    slots = property(**slots())

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

    ######################################################################
    ## Property 
    def hostnames():
        doc = "Allowed hostnames for this resource reservation (i.e., cluster nodes)."
        def fget(self):
            return self._hostnames
        def fset(self, val):
            self._hostnames = val
        def fdel(self, val):
            self._hostnames = None
        return locals()
    hostnames = property(**hostnames())

    ######################################################################
    ## Property 
    def os():
        doc = "Allowed operating systems for this resource reservation."
        def fget(self):
            return self._os
        def fset(self, val):
            self._os = val
        def fdel(self, val):
            self._os = None
        return locals()
    os = property(**os())

    ######################################################################
    ## Property 
    def arch():
        doc = "Allowed operating systems for this resource reservation."
        def fget(self):
            return self._arch
        def fset(self, val):
            self._arch = val
        def fdel(self, val):
            self._arch = None
        return locals()
    arch = property(**arch())
