#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package API.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.resource._compute_description import ComputeDescription as SComputeDescription
class ComputeDescription(SComputeDescription):
    '''A SAGA compute resource description as defined in GWD-R.xx
    '''
    pass


from bliss.saga.resource._state import State as SState
class State(SState):
    '''SAGA resource states as defined in GWD-R.xx.
    '''
    pass


from bliss.saga.resource._manager_facade import Manager as SManager
class Manager(SManager):
    '''A SAGA resource manager as defined in GWD-R.xx.

       The resource manager can translate resource requests into stateful
       resource handles. It also manages the persistency of resource
       handles and resource pools.
    '''
    pass


from bliss.saga.resource._compute_facade import Compute as SCompute
class Compute(SCompute):
    '''A SAGA compute resource as defined in GWD-R.xx.

       A compute resource represents a stateful handle to a physical
       compute resource. Jobs can be submitted to it.  
    '''
    pass


from bliss.saga.resource._compute_pool_facade import ComputePool as SComputePool
class ComputePool(SComputePool):
    '''A SAGA compute pool as defined in GWD-R.xx.

       A compute resource pool is a container for that holds
       compute resource objects. A custom job scheduling 
       algorithm can be selected for a compute resource pool. 
    '''
    pass


