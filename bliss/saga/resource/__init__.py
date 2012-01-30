#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package API.
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.resource._description_impl import Description as SDescription
class Description(SDescription):
    '''Loosely defines a SAGA Resource description as defined in GWD-R.xx
    '''
    pass

from bliss.saga.resource._manager_impl import Manager as SManager
class Manager(SManager):
    '''Loosely defines a SAGA Resource Manager object as defined in GWD-R.xx
    '''
    pass

#from bliss.saga.resource._compute_impl import Compute as SCompute
#class Compute(SCompute):
#    '''Loosely defines a SAGA Compute Resource object as defined in GWD-R.x
#    '''
#    pass

#from bliss.saga.resource._storage_impl import Storage as SStorage
#class Storage(SStorage):
#    '''Loosely defines a SAGA Storage Resource object as defined in GWD-R.x
#    '''
#    pass


