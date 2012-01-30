#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga._object_impl import Object
from bliss.saga._attributes_impl import AttributeInterface

class Description(Object, AttributeInterface):
    '''Loosely defines a SAGA Resource description as defined in GWD-R.xx
    '''

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty resource description.'''
        Object.__init__(self, Object.ResourceDescription, 
                        apitype=Object.JobAPI,)
        AttributeInterface.__init__(self)

        self._dummy        = None
  

        # register properties with the attribute interface
        self._register_rw_attribute     (name="Dummy", 
                                         accessor=self.__class__.dummy) 
    ######################################################################
    ## 
    def __del__(self):
        '''Delete the resource description in a civilised fashion.'''
        # nothing to do here 
        pass

    def __str__(self):
        '''String representation of the resource description'''
        result = str("{")
        #for attribute in self.list_attributes():
        #    if self.attribute_is_vector(attribute):
        #        value = repr(self.get_vector_attribute(attribute))
        #    else:
        #        value = str(self.get_attribute(attribute))
        #    result += str("'%s' : '%s'," % (str(attribute), value))
        #
        result += "}"
        return result
        

    ######################################################################
    ## Property: 
    def dummy():
        doc = "A dummy attribute."
        def fget(self):
            return self._dummy
        def fset(self, val):
            self._dummy = val
        def fdel(self, val):
            self._dummy = None
        return locals()
    dummy = property(**dummy())
      

