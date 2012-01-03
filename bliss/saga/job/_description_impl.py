#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga._object_impl import Object
from bliss.saga._attributes_impl import AttributeInterface

class Description(Object, AttributeInterface):
    '''Loosely represents a SAGA job description as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty job description.'''
        Object.__init__(self, Object.JobDescription, 
                        apitype=Object.JobAPI,)
        AttributeInterface.__init__(self)

        self._executable        = None
        self._arguments         = None
        self._environment       = None
        self._project           = None
        self._output            = None
        self._error             = None
        self._queue             = None
        self._wall_time_limit   = None
        self._working_directory = None
        self._contact           = None
        self._total_cpu_count   = None

        self._number_of_processes = None
        self._spmd_variation = None

        # register properties with the attribute interface
        self._register_rw_attribute     (name="Executable", 
                                         accessor=self.__class__.executable) 
        self._register_rw_attribute     (name="Output", 
                                         accessor=self.__class__.output) 
        self._register_rw_attribute     (name="Error", 
                                         accessor=self.__class__.error) 
        self._register_rw_attribute     (name="Queue", 
                                         accessor=self.__class__.queue) 
        self._register_rw_attribute     (name="WallTimeLimit", 
                                         accessor=self.__class__.wall_time_limit) 
        self._register_rw_attribute     (name="WorkingDirectory", 
                                         accessor=self.__class__.working_directory) 
        self._register_rw_attribute     (name="Contact", 
                                         accessor=self.__class__.contact) 
        self._register_rw_attribute     (name="TotalCPUCount", 
                                         accessor=self.__class__.total_cpu_count) 
        self._register_rw_attribute     (name="NumberOfProcesses", 
                                         accessor=self.__class__.number_of_processes) 
        self._register_rw_attribute     (name="SPMDVariation", 
                                         accessor=self.__class__.spmd_variation) 


        self._register_rw_vec_attribute (name="Arguments", 
                                         accessor=self.__class__.arguments) 
        self._register_rw_vec_attribute (name="Environment", 
                                         accessor=self.__class__.environment) 
        self._register_rw_vec_attribute (name="JobProject", 
                                         accessor=self.__class__.project) 

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the job description in a civilised fashion.'''
        # nothing to do here 
        pass

    ######################################################################
    ## Property: 
    def executable():
        doc = "The job executable."
        def fget(self):
            return self._executable
        def fset(self, val):
            self._executable = val
        def fdel(self, val):
            self._executable = None
        return locals()
    executable = property(**executable())
      
    ######################################################################
    ## Property: 
    def arguments():
        doc = "The arguments to pass to the job executable."
        def fget(self):
            return self._arguments
        def fset(self, val):
            self._arguments = val
        def fdel(self, val):
            self._arguments = None
        return locals()
    arguments = property(**arguments())

    ######################################################################
    ## Property: 
    def environment():
        doc = "The environment variables to set in the job's execution context."
        def fget(self):
            return self._environment
        def fset(self, val):
            self._environment = val
        def fdel(self, val):
            self._environment = None
        return locals()
    environment = property(**environment())


    ######################################################################
    ## Property: 
    def output():
        doc = "The file in which the job\'s stdout stream will be captured."
        def fget(self):
            return self._output
        def fset(self, val):
            self._output = val
        def fdel(self, val):
            self._output = None
        return locals()
    output = property(**output())

    ######################################################################
    ## Property: 
    def error():
        doc = "The file in which the job\'s stderr stream will be captured."
        def fget(self):
            return self._error
        def fset(self, val):
            self._error = val
        def fdel(self, val):
            self._error = None
        return locals()
    error = property(**error())

    ######################################################################
    ## Property: 
    def project():
        doc = "The project / allocation name the job should be credited to."
        def fget(self):
            return self._project
        def fset(self, val):
            self._project = val
        def fdel(self, val):
            self._project = None
        return locals()
    project = property(**project())

    ######################################################################
    ## Property: 
    def queue():
        doc = "The queue on the backend system to place the job in."
        def fget(self):
            return self._queue
        def fset(self, val):
            self._queue = val
        def fdel(self, val):
            self._queue = None
        return locals()
    queue = property(**queue())

    ######################################################################
    ## Property:
    def wall_time_limit():
        doc = "The hard limit for the total job runtime."
        def fget(self):
            return self._wall_time_limit
        def fset(self, val):
            self._wall_time_limit = val
        def fdel(self, val):
            self._wall_time_limit = None
        return locals()
    wall_time_limit = property(**wall_time_limit())

    ######################################################################
    ## Property: 
    def working_directory():
        doc = "The working directory for the job."
        def fget(self):
            return self._working_directory
        def fset(self, val):
            self._working_directory = val
        def fdel(self, val):
            self._working_directory = None
        return locals()
    working_directory = property(**working_directory())


    ######################################################################
    ## Property: 
    def contact():
        doc = "Endpoint describing where to report job state transitions (e.g., email)."
        def fget(self):
            return self._contact
        def fset(self, val):
            self._contact = val
        def fdel(self, val):
            self._contact = None
        return locals()
    contact = property(**contact())


    ######################################################################
    ## Property: 
    def total_cpu_count():
        doc = "Total number of cpus requested for this job."
        def fget(self):
            return self._total_cpu_count
        def fset(self, val):
            self._total_cpu_count = val
        def fdel(self, val):
            self._total_cpu_count = None
        return locals()
    total_cpu_count = property(**total_cpu_count())


    ######################################################################
    ## Property: 
    def number_of_processes():
        doc = "Number of processes to launch"
        def fget(self):
            return self._number_of_processes
        def fset(self, val):
            self._number_of_processes = val
        def fdel(self, val):
            self._number_of_processes = None
        return locals()
    number_of_processes = property(**number_of_processes())

    ######################################################################
    ## Property: 
    def spmd_variation():
        doc = "SPMD variation (MPI, None, ...)"
        def fget(self):
            return self._spmd_variation
        def fset(self, val):
            self._spmd_variation = val
        def fdel(self, val):
            self._spmd_variation = None
        return locals()
    spmd_variation = property(**spmd_variation())
