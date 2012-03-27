    #v .im: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Resource Package API.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"


from bliss.saga.resource.state import State as SState
class State(SState):
    '''Resource states as defined in GFD.xx.
    '''
    pass


from bliss.saga.resource.manager_api import Manager as SManager
class Manager(SManager):
    '''A resource manager as defined in GFD.xx.

       The resource manager can translate resource requests into stateful
       resource handles. It also manages the persistence of resource
       handles and resource pools.
    '''
    pass



from bliss.saga.resource.compute_api import Compute as SCompute
class Compute(SCompute):
    '''A compute resource as defined in GFD.xx.

       TODO: Describe me.
    '''
    pass

from bliss.saga.resource.compute_description_api import ComputeDescription as SComputeDescription
class ComputeDescription(SComputeDescription):
    '''A compute resource description as defined in GFD.xx

       TODO: Describe me.
    '''
    pass



from bliss.saga.resource.storage_api import Storage as SStorage
class Storage(SStorage):
    '''A storage resource as defined in GFD.xx.

       TODO: Describe me.
    '''
    pass

from bliss.saga.resource.storage_description_api import StorageDescription as SStorageDescription
class StorageDescription(SStorageDescription):
    '''A storage resource description as defined in GFD.xx

       TODO: Describe me.
    '''
    pass



#from bliss.saga.resource.network_api import Network as SNetwork
#class Network(SNetwork):
#    '''A SAGA network resource as defined in GFD.xx.
#
#       TODO: Describe me.
#    '''
#    pass

#from bliss.saga.resource.network_description_api import NetworkDescription as SNetworkDescription
#class NetworkDescription(SNetworkDescription):
#    '''A SAGA network resource description as defined in GFD.xx
#    '''
#    pass

