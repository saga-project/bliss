# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.Object     import Object
from bliss.saga.Attributes import AttributeInterface

class StorageDescription(Object, AttributeInterface):
    '''Defines a SAGA storage_description as defined in GFD.xx

    A storage description describes a storage resource (L{resource.Storage}) --
    which is, essentially, anything which can run store data.  The description
    is used to find or create instances of storage resources with specific
    properties and capabilities (see L{resource.Manager}).

    B{Usage example 1} shows how to obtain some storage of a certain size::

      # describe the resource requirements
      sd = saga.resource.StorageDescription()
      sd['Size'] = 1024 # MB

      # obtain a handle to a suitable resource
      rm = saga.resource.Manager()
      sr = rm.create_storage(sd)

      # stage some data onto the storage
      d  = sr.get_filesystem()
      d.copy("file://localhost/data/input.dat", "/data/")

      # ...

      # once the application is done, we do not need the storage resource anymore:
      sr.destroy()

    '''

    @staticmethod
    def _deep_copy(sd):
        sd_copy = bliss.saga.resource.StorageDescription()

        AttributeInterface._attributes_deep_copy (sd, sd_copy)

        return sd_copy


    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) storage resource description.'''
        Object.__init__(self)
        self._apitype = 'saga.resource'


        self._attributes_extensible  (False)
        self._attributes_camelcasing (True)
      
        # register properties with the attribute interface 
        self._attributes_register  ('Dynamic',   False, self.Bool,   self.Scalar, self.Writable)
        self._attributes_register  ('Start',     None,  self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('End',       None,  self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('Duration',  None,  self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('Template',  None,  self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Size',      None,  self.Int,    self.Scalar, self.Writable)


    ######################################################################
    ## 
    def __del__(self):
        '''Delete this resource description.'''
        # nothing to do here 
        pass
    
    ######################################################################
    ## Property 
        Start = property ( doc = '''
        Start:
        Required start time for this resource reservation.
        
        The resource is expected to be 'Running' at the specified point in time,
        and thus ready to execute job requests.  A backend which cannot make
        that promise will raise and exception.
        ''')
    
    ######################################################################
    ## Property 
        End = property ( doc = '''
        End:
        Required end time for this resource request.
        
        The resource is expected to be available until at most that given point
        in time.  A resource manager which cannot guarantee the resource to be
        available before that point (- a given duration) will fail the resource
        request.
        ''')
    
    ######################################################################
    ## Property 
        Duration = property ( doc = '''
        Duration:
        Required duration for this resource request.

        The specified time span is the time the resource is expected to be
        'Running' -- times spent in other states does not count toward this
        limit.  A backend which cannot make that promise will raise and 
        exception.
        ''')
    
    ######################################################################
    ## Property 
        Template = property ( doc = '''
        Template:
        Required template for this resource request.

        The specified template is to be used to fill in certain elements of 
        this storage resource description.  If the template is not known by 
        the backend, a 'BadParameter' exception will be raised upon resource 
        creation.  Specific values in the compute resource description will 
        supersede the values specified by the template.
        ''')

    ######################################################################
    ## Property 
        Dynamic = property ( doc = '''
        Dynamic:
        Dynamic or not.
        
        The 'dynamic' flag signals that the resource description provides
        estimated values, but that the resource manager is allowed to choose
        different initial values, and also can change the values during the
        resource lifetime.  That flag is specifically targeting backends which
        can resize the resources in response to actual storage requirements.
        ''')
    
    ######################################################################
    ## Property 
        Size = property ( doc = '''
        Size:
        Required size of storage, in MegaBytes.
        ''')
    
