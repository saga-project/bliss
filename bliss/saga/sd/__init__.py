#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Service Discovery Package API. 
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.sd._discoverer_impl import Discoverer as SDiscoverer
class Discoverer(SDiscoverer):
    '''Loosely defines a SAGA Service Discoverer as defined in GFD.90.
    '''
    pass

from bliss.saga.sd._service_description_impl import ServiceDescription as SServiceDescription
class ServiceDescription(SServiceDescription):
    '''Loosely defines a SAGA Service Description as defined in GFD.90.
    '''
    pass

from bliss.saga.sd._service_data_impl import ServiceData as SServiceData
class ServiceData(SServiceData):
    '''Loosely defines a SAGA Service Data as defined in GFD.90.
    '''
    pass
