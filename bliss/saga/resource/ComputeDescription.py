# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Object import Object
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

      js = saga.job.Service(cr)
      j  = js.create_job(jd)
      j.run()
      j.wait()


      # once the job is finished, we do not need the compute resource anymore:
      cr.destroy()

    '''

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) compute resource description.'''
        Object.__init__(self, Object.Type.ResourceComputeDescription, 
                        apitype=Object.Type.ResourceAPI,)

        AttributeInterface.__init__(self)

        self._dynamic        = False
        self._start          = None
        self._end            = None
        self._duration       = None
        self._template       = None

        self._register_rw_attribute(name="Dynamic", 
                                        accessor=self.__class__.dynamic) 
        self._register_rw_attribute(name="Start", 
                                        accessor=self.__class__.start) 
        self._register_rw_attribute(name="End", 
                                        accessor=self.__class__.end) 
        self._register_rw_attribute(name="Duration", 
                                        accessor=self.__class__.duration) 
        self._register_rw_attribute(name="Template", 
                                        accessor=self.__class__.template) 
        
        self._slots = 1
        self._memory = None
        self._hostnames = list()
        self._operating_system = 'Any'
        self._architecture = 'Any'

        self._register_rw_vec_attribute(name="OperatingSystem", 
                                        accessor=self.__class__.operating_system) 
        self._register_rw_vec_attribute(name="Architecture", 
                                        accessor=self.__class__.architecture)
        self._register_rw_vec_attribute(name="Hostnames", 
                                        accessor=self.__class__.hostnames)
        self._register_rw_attribute(name="Slots", 
                                    accessor=self.__class__.slots)
        self._register_rw_attribute(name="Memory", 
                                    accessor=self.__class__.memory) 
    
    ######################################################################
    ## 
    def __del__(self):
        '''Delete this resource description.'''
        # nothing to do here 
        pass

    ######################################################################
    ## Property 
    def start():
        doc = '''Required start time for this resource request.
        
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
    def template():
        doc = '''Required template for this resource request.

        The specified template is to be used to fill in certain elements of 
        this compute resource description.  For example, the EC2 'c1.xlarge'
        instance template implies a certain number of CPU cores and memory, 
        etc.  If the template is not known by the backend, a 'BadParameter'
        exception will be raised upon resource creation.  Specific values 
        in the compute resource description will supersede the values 
        specified by the template.
        '''
        def fget(self):
            return self._template
        def fset(self, val):
            self._template = val
        def fdel(self, val):
            self._template = None
        return locals()
    template = property(**template())

    ######################################################################
    ## Property 
    def dynamic():
        doc = '''Dynamic or not.
        
        The 'dynamic' flag signals that the resource description provides
        estimated values, but that the resource manager is allowed to choose
        different initial values, and also can change the values during the
        resource lifetime.  That flag is specifically targeting backends which
        can resize the resources in response to the actual job workload.
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
    def slots():
        doc = '''Required number of cores for this resource request.'''
        def fget(self):
            return self._slots
        def fset(self, val):
            self._slots = val
        def fdel(self, val):
            self._slots = None
        return locals()
    slots = property(**slots())

    ######################################################################
    ## Property 
    def memory():
        doc = '''Required amount of memory for this resource request.'''
        def fget(self):
            return self._memory
        def fset(self, val):
            self._memory = val
        def fdel(self, val):
            self._memory = None
        return locals()
    memory = property(**memory())

    ######################################################################
    ## Property 
    def hostnames():
        doc = '''Allowed hostnames for this resource request.
        
        With this attribute, one can specify specific and individual compute
        nodes -- for example specific cluster nodes, specific sets of virtual
        machine instances, etc.
        '''
        def fget(self):
            return self._hostnames
        def fset(self, val):
            self._hostnames = val
        def fdel(self, val):
            self._hostnames = None
        return locals()
    hostnames = property(**hostnames())

    ######################################################################
    ## Property 
    def operating_system():
        doc = '''Allowed operating system(s) for this resource request.'''
        def fget(self):
            return self._operating_system
        def fset(self, val):
            self._operating_system = val
        def fdel(self, val):
            self._operating_system = None
        return locals()
    operating_system = property(**operating_system())

    ######################################################################
    ## Property 
    def architecture():
        doc = '''Allowed systems architecture(s) for this resource request.'''
        def fget(self):
            return self._architecture
        def fset(self, val):
            self._architecture = val
        def fdel(self, val):
            self._architecture = None
        return locals()
    architecture = property(**architecture())

