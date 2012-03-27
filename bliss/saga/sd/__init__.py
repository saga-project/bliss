#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Service Discovery Package API. 
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.sd.discoverer_api import Discoverer as SDiscoverer
class Discoverer(SDiscoverer):
    '''Loosely defines a SAGA Service Discoverer as defined in GFD.90.
    '''
    pass

from bliss.saga.sd.service_description_api import ServiceDescription as SServiceDescription
class ServiceDescription(SServiceDescription):
    '''Loosely defines a SAGA Service Description as defined in GFD.90.
    '''
    pass

from bliss.saga.sd.service_data_api import ServiceData as SServiceData
class ServiceData(SServiceData):
    '''Loosely defines a SAGA Service Data as defined in GFD.90.
    '''
    pass
