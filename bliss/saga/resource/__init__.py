# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package API.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.resource.state import State as SState
class State(SState):
    '''SAGA resource states as defined in GFD.xx.
    '''
    pass


from bliss.saga.resource.manager_api import Manager as SManager
class Manager(SManager):
    '''A SAGA resource manager as defined in GFD.xx.

       The resource manager can translate resource requests into stateful
       resource handles. It also manages the persistence of resource
       handles and resource pools.
    '''
    pass



from bliss.saga.resource.compute_api import Compute as SCompute
class Compute(SCompute):
    '''A SAGA compute resource as defined in GFD.xx.

       A compute resource represents a stateful handle to a physical
       compute resource. Jobs can be submitted to it.  
    '''
    pass

from bliss.saga.resource.compute_description_api import ComputeDescription as SComputeDescription
class ComputeDescription(SComputeDescription):
    '''A SAGA compute resource description as defined in GFD.xx
    '''
    pass



from bliss.saga.resource.storage_api import Storage as SStorage
class Storage(SStorage):
    '''A SAGA storage resource as defined in GFD.xx.

       TODO: Describe me.
    '''
    pass

from bliss.saga.resource.storage_description_api import StorageDescription as SStorageDescription
class StorageDescription(SStorageDescription):
    '''A SAGA storage resource description as defined in GFD.xx
    '''
    pass



from bliss.saga.resource.network_api import Network as SNetwork
class Network(SNetwork):
    '''A SAGA network resource as defined in GFD.xx.

       TODO: Describe me.
    '''
    pass

from bliss.saga.resource.network_description_api import NetworkDescription as SNetworkDescription
class NetworkDescription(SNetworkDescription):
    '''A SAGA network resource description as defined in GFD.xx
    '''
    pass



from bliss.saga.resource.pool_api import Pool as SPool
class Pool(SPool):
    '''A SAGA compute pool as defined in GFD.xx.

       A compute resource pool is a container for that holds
       resource objects. Custom policies for scheduling etc.
       can be selected for a resource pool. 
    '''
    pass


