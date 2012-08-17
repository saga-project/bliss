# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.Object     import Object
from bliss.saga.Attributes import AttributeInterface

class ComputeDescription(Object, AttributeInterface):
    '''Defines a SAGA compute_description as defined in GFD.xx

    A compute description describes a L{resource.Compute} -- which is, essentially,
    anything which can run compute jobs.  The description is used to find or
    create instances of compute resources with specific properties and
    capabilities (see L{resource.Manager}).

    B{Usage example 1} shows how to obtain a handle to a cluster of a certain size::

      # describe the resource requirements
      cd = saga.resource.ComputeDescription()
      cd['Slots'] = 128

      # obtain a handle to a suitable resource
      rm = saga.resource.Manager()
      cr = rm.create_compute(cd)

      # submit a large job
      jd = saga.job.Description()
      jd['Executable'] = 'blast'
      jd['NumberOfProcesses'] = 128
      jd['SPMDVariation'] = MPI

      js = cr.get_job_service()
      j  = js.create_job(jd)
      j.run()
      j.wait()


      # once the job is finished, we do not need the compute resource anymore:
      cr.destroy()

    '''

    @staticmethod
    def _deep_copy(cd):
        cd_copy = bliss.saga.resource.ComputeDescription()

        AttributeInterface.attributes_deep_copy_ (cd, cd_copy)

        return cd_copy

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) compute resource description.'''
        Object.__init__(self, Object.ObjectType.ResourceComputeDescription, 
                        apitype=Object.ObjectType.ResourceAPI,)

        # set attribute interface properties
        self.attributes_extensible_  (False)
        self.attributes_camelcasing_ (True)

        # register properties with the attribute interface 
        self.attributes_register_  ('Dynamic',         False, self.Bool,   self.Scalar, self.Writable)
        self.attributes_register_  ('Start',           None,  self.Time,   self.Scalar, self.Writable)
        self.attributes_register_  ('End',             None,  self.Time,   self.Scalar, self.Writable)
        self.attributes_register_  ('Duration',        None,  self.Time,   self.Scalar, self.Writable)
        self.attributes_register_  ('Template',        None,  self.String, self.Scalar, self.Writable)

        self.attributes_register_  ('Slots',           1,     self.Int,    self.Scalar, self.Writable)
        self.attributes_register_  ('OperatingSystem', 'Any', self.Enum,   self.Scalar, self.Writable)
        self.attributes_register_  ('Architecture',    'Any', self.Enum,   self.Scalar, self.Writable)
        self.attributes_register_  ('Hostnames',       [],    self.String, self.Vector, self.Writable)
        self.attributes_register_  ('Memory',          None,  self.Int,    self.Scalar, self.Writable)

    ######################################################################
    ## 
    def __del__(self):
        '''Delete this resource description.'''
        # nothing to do here 
        pass

    ######################################################################
    ## Property 
        '''
        start:
        Required start time for this resource request.
        
        The resource is expected to be 'Running' at the specified point in time,
        and thus ready to execute job requests.  A backend which cannot make
        that promise will raise and exception.
        '''
    
    ######################################################################
    ## Property 
        '''
        end:
        Required end time for this resource request.
        
        The resource is expected to be available until at most that given point
        in time.  A resource manager which cannot guarantee the resource to be
        available before that point (- a given duration) will fail the resource
        request.
        '''
    
    ######################################################################
    ## Property 
        '''
        duration:
        Required duration for this resource request.

        The specified time span is the time the resource is expected to be
        'Running' -- times spent in other states does not count toward this
        limit.  A backend which cannot make that promise will raise and 
        exception.
        '''

    ######################################################################
    ## Property 
        '''
        template:
        Required template for this resource request.

        The specified template is to be used to fill in certain elements of 
        this compute resource description.  For example, the EC2 'c1.xlarge'
        instance template implies a certain number of CPU cores and memory, 
        etc.  If the template is not known by the backend, a 'BadParameter'
        exception will be raised upon resource creation.  Specific values 
        in the compute resource description will supersede the values 
        specified by the template.
        '''

    ######################################################################
    ## Property 
        '''
        dynamic:
        Dynamic or not.
        
        The 'dynamic' flag signals that the resource description provides
        estimated values, but that the resource manager is allowed to choose
        different initial values, and also can change the values during the
        resource lifetime.  That flag is specifically targeting backends which
        can resize the resources in response to the actual job workload.
        '''
    
    ######################################################################
    ## Property 
        '''
        slots:
        Required number of cores for this resource request.
        '''

    ######################################################################
    ## Property 
        '''
        memory:
        Required amount of memory for this resource request.
        '''

    ######################################################################
    ## Property 
        '''
        hostnames:
        Allowed hostnames for this resource request.
        
        With this attribute, one can specify specific and individual compute
        nodes -- for example specific cluster nodes, specific sets of virtual
        machine instances, etc.
        '''

    ######################################################################
    ## Property 
        '''
        operating_system:
        Allowed operating system(s) for this resource request.
        '''

    ######################################################################
    ## Property 
        '''
        architecture:
        Allowed systems architecture(s) for this resource request.
        '''

