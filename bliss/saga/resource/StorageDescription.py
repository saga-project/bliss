# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Object import Object
from bliss.saga.Attributes import AttributeInterface

class StorageDescription(Object, AttributeInterface):
    '''Defines a SAGA storage_description as defined in GFD.xx

    A storage description describes a storage resource (L{resource.Storage}) --
    which is, essentially, anything which can run store data.  The description
    is used to find or create instances of storage resources with specific
    properties and capabilities (see L{resource.Manager}).

    B{Usage example 1} shows how to obtain some storage of a certain size::

      # describe the resource requirements
      sd = saga.resource.StorageDescription ()
      sd['Size'] = 1024 # MB

      # obtain a handle to a suitable resource
      rm = saga.resource.Manager ()
      sr = rm.create_storage (sd)

      # stage some data onto the storage
      d  = sr.get_filesystem ()
      d.copy ("file://localhost/data/input.dat", "/data/")

      # ...

      # once the application is done, we do not need the storage resource anymore:
      sr.destroy ()

    '''

    ######################################################################
    ## 
    # FIXME: not sure if inheritance for the attribute interface is supposed 
    # to work this way...
    def __init__(self):
        '''Create a new (empty) storage resource description.'''
        Object.__init__(self, Object.Type.ResourceStorageDescription, 
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
        doc = '''Required start time for this resource reservation.
        
        The resource is expected to be 'Running' at the specified point in time,
        and thus ready to execute job requests.  A backend which cannot make
        that promise will raise and exception.
        '''
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
        doc = '''Required end time for this resource request.
        
        The resource is expected to be available until at most that given point
        in time.  A resource manager which cannot guarantee the resource to be
        available before that point (- a given duration) will fail the resource
        request.
        '''
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
        doc = '''Required duration for this resource request.

        The specified time span is the time the resource is expected to be
        'Running' -- times spent in other states does not count toward this
        limit.  A backend which cannot make that promise will raise and 
        exception.
        '''
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
        doc = '''Dynamic or not.
        
        The 'dynamic' flag signals that the resource description provides
        estimated values, but that the resource manager is allowed to choose
        different initial values, and also can change the values during the
        resource lifetime.  That flag is specifically targeting backends which
        can resize the resources in response to actual storage requirements.
        '''
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
        doc = "Required size of storage, in MegaBytes."
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
        # FIXME: as storages cannot be bound to compute resources in Bliss, this
        # property does not make sense anymore. 
        doc = "Mountpoint of storage."
        def fget(self):
            return self._mountpoint
        def fset(self, val):
            self._mountpoint = val
        def fdel(self, val):
            self._mountpoint = None
        return locals()
    mountpoint = property(**mountpoint())

