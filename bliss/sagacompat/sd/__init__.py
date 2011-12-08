#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Service Discovery Package (compatibility) API. 
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.sd.discoverer import Discoverer as SDiscoverer
class discoverer(SDiscoverer):
    '''Loosely defines a SAGA Service Discoverer as defined in GFD.90.
    '''
    pass

from bliss.saga.sd.service_description import ServiceDescription as SServiceDescription
class service_description(SServiceDescription):
    '''Loosely defines a SAGA Service Description as defined in GFD.90.
    '''
    pass

from bliss.saga.sd.service_data import ServiceData as SServiceData
class service_data(SServiceData):
    '''Loosely defines a SAGA Service Data as defined in GFD.90.
    '''
    pass
