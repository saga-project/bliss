#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.exception import Exception as SAGAException
from bliss.saga.exception import Error as SAGAError

class AttributeInterface(object):
    '''Loosely defines the SAGA attribute interface as defined in GFD.90.'''
   
 
    def __init__(self):
        '''Constructor'''
        self._attributes = dict()

    def _valid_attribute_key(self, key):
        '''Check if an attribute is defined as valid.
        '''
        if key in self._attributes:
            return True 
        return False

    ######################################################################
    #
    def get_attribute(self, key):
        '''Return the value of a scalar attribute.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExists, 
                  "Attribute %s doesn't exist." % (key))
        if self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute %s is a vector attribute." % (key))
        return self._attributes[key]['value']

    ######################################################################
    #    
    def set_attribute(self, key, value):
        '''Set the value of a scalar attribute.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute %s doesn't exist." % (key))
        if self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute %s is a vector attribute." % (key))
        if self.attribute_is_readonly(key):
            raise SAGAException(SAGAError.PermissionDenied, 
                  "Attribute %s is a read-only attribute." % (key))
        self._attributes[key]['value'] = value

    ######################################################################
    #
    def get_vector_attribute(self, key):
        '''Return the value of a vector attribute.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute %s doesn't exist." % (key))
        if not self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute %s is a scalar attribute." % (key))
        return self._attributes[key]['value']
 
    ######################################################################
    #
    def set_vector_attribute(self, key, value):
        '''Set the value of a vector attribute.
        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExists, 
                  "Attribute %s doesn't exist." % (key))
        if not self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute %s is a vector attribute." % (key))
        if self.attribute_is_readonly(key):
            raise SAGAException(SAGAError.PermissionDenied, 
                  "Attribute %s is a read-only attribute." % (key))
        self._attributes[key]['value'] = value

    ######################################################################
    #
    def attribute_exists(self, key):
        '''Check if an attribute exists.
        '''
        if key in self._attributes:
            #if len(self._attributes[key]['value']) > 0:
            return True 
        return False

    ######################################################################
    #
    def attribute_is_writeable(self, key):
        '''Check if an attribute is writable.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute %s doesn't exist." % (key))

        return not self.attribute_is_readonly(key)

    ######################################################################
    #
    def attribute_is_readonly(self, key):
        '''Check if an attribute is read-only.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExists, 
                  "Attribute %s doesn't exist." % (key))

        if (self._attributes[key]['access']) == 'RW':
            return False
        else:
            return True

    ######################################################################
    #
    def attribute_is_vector(self, key):
        '''Check if an attribute is a vector.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExists, 
                  "Attribute %s doesn't exist." % (key))
 
        if (self._attributes[key]['type']) == 'V':
            return True
        else:
            return False

    ######################################################################
    #
    def list_attributes(self): 
        '''List all defined attributes.
        '''
        list = []
        for att in self._attributes:
            if self.attribute_exists(att):
                list.append(att)
        return list
            
