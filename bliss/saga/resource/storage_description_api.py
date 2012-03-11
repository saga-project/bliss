# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object_api import Object
from bliss.saga.attributes_api import AttributeInterface

class StorageDescription(Object, AttributeInterface):
    '''Defines a SAGA storage_description as defined in GFD.xx
    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attribute interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) storage resource description.'''
        Object.__init__(self, Object.Type.ResourceDescription, 
                        apitype=Object.Type.ResourceAPI)

        AttributeInterface.__init__(self)

        self._dynamic        = False
        self._start          = None
        self._end            = None
        self._duration       = None
        
        self._register_rw_attribute     (name="Dynamic", 
                                         accessor=self.__class__.dynamic) 
        self._register_rw_attribute     (name="Start", 
                                         accessor=self.__class__.start) 
        self._register_rw_attribute     (name="End", 
                                         accessor=self.__class__.end) 
        self._register_rw_attribute     (name="Duration", 
                                         accessor=self.__class__.duration) 
        
        self._size           = ''
        self._mountpoint     = None
        
        self._register_rw_attribute     (name="Size", 
                                         accessor=self.__class__.size) 
        self._register_rw_attribute     (name="Mountpoint",
                                         accessor=self.__class__.mountpoint) 


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
    def size():
        doc = "Required size of storage."
        def fget(self):
            return self._size
        def fset(self, val):
            self._size = val
        def fdel(self, val):
            self._size = None
        return locals()
    size = property(**size())
    
    ######################################################################
    ## Property 
    def mountpoint():
        doc = "Mountpoint of storage."
        def fget(self):
            return self._mountpoint
        def fset(self, val):
            self._mountpoint = val
        def fdel(self, val):
            self._mountpoint = None
        return locals()
    mountpoint = property(**mountpoint())

