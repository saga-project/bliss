#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.object_api import Object
from bliss.saga.attributes_api import AttributeInterface

class Description(Object, AttributeInterface):
    '''Loosely represents a SAGA job description as defined in GFD.90<F2>
    The following attributes are supported:

      - B{Executable:}  I{command to execute. }
         - this is the only required attribute.  
         - can be a full pathname, a pathname 
           relative to the 'WorkingDirectory' as 
           evaluated on the execution host, or
           a executable name to be searched in the
           target host's PATH environment (if 
           available).
         - B{Example:} C{d.set_attribute ("Executable", "/usr/local/bin/blast")}

      - B{Arguments:} I{list of parameters for the command. }
         - B{Example:} C{d.set_attribute ("Arguments", ["-i", "/data/input.dat", "-o", "/tmp/output.dat"])}

      - B{SPMDVariation:} I{SPMD job type and startup mechanism}
         - the SPMD JSDL extension defines the value
           to be an URI.  For simplicity, SAGA allows
           the following strings, which map into the 
           respective URIs: MPI, GridMPI, IntelMPI,
           LAM-MPI, MPICH1, MPICH2, MPICH-GM, MPICH-MX,
           MVAPICH, MVAPICH2, OpenMP, POE, PVM, None
         - the value '' (no value, default) indicates
           that the application is not a SPMD 
           application.
         - as JSDL, SAGA allows other arbitrary values.
           The implementation must clearly document
           which values are supported.
         - B{Example:} C{d.set_attribute ("SPMDVariation", "OpenMP")}

      - B{TotalCPUCount:} I{total number of cpus requested for this job}
         - B{Example:} C{d.set_attribute ("TotalCPUCount", 5)}

      - B{NumberOfProcesses:} I{total number of processes to be started}
         - B{Example:} C{d.set_attribute ("NumberOfProcesses", 10)}

      - B{Environment:} I{list of environment variables and values for the job}
         - exported into the job environment
         - format: 'key=value'
         - B{Example:} C{d.set_attribute ("Environment", ["DEBUG=1", "PRIORITY=3"])}

      - B{WorkingDirectory:} I{working directory for the job}
         - gets created if it does not exist
         - B{Example:} C{d.set_attribute ("Working Directory", "/scratch/blast/")}

      - B{Output:} I{pathname of the standard output file}
         - will not be used if 'Interactive' is 'True'
         - B{Example:} C{d.set_attribute ("Output", "stdout.log")}

      - B{Error:} I{pathname of the standard error file}
         - will not be used if 'Interactive' is 'True'
         - B{Example:} C{d.set_attribute ("Error", "stderr.log")}

      - B{FileTransfer:} I{list of file transfer directives}
         - translates into jsdl:DataStaging
         - used to specify pre- and post-staging
         - staging is part of the job's 'Running' state
         - syntax similar to LSF (SRC and TGT are URLs)::
              'SRC >  TGT' : SRC is staged in               to TGT
              'SRC >> TGT' : SRC is staged in  and appended to TGT
              'TGT <  SRC' : SRC is staged out              to TGT
              'TGT << SRC' : SRC is staged out and appended to TGT
         - B{Example:} C{d.set_attribute ("FileTransfer", ["file://localhost/data/data_1 > input.dat"])}
              

      - B{WallTimeLimit:} I{hard limit for the total job runtime.}
         - intended to provide hints to the scheduler. 
         - B{Example:} C{d.set_attribute ("WallTimeLlimit", "00:20:00")}

      - B{Queue:} I{name of a queue to place the job into}
         - While SAGA itself does not define the 
           semantics of a "queue", many backend systems
           can make use of this attribute. 
         - B{Example:} C{d.set_attribute ("Queue", "Small")}

      - B{JobProject:} I{name of a account or project name}
         - While SAGA itself does not define the 
           semantics of an "account" or "project", 
           many backend systems can make use of
           this attribute for the purpose of 
           accounting.
         - B{Example:} C{d.set_attribute ("JobPorject", "AllocationStudentXYZ")}

      - B{Contact:} I{set of endpoints describing where to report job state transitions.}
         - format: URI (e.g. fax:+123456789, sms:+123456789, mailto:joe@doe.net). 
         - named 'JobContact' in GFD.90
         - B{Example:} C{d.set_attribute ("Contact", "job_states_changes@group.intitute.edu")}
    
    '''

#      - B{ProcessesPerHost:} I{number of processes to be started per host}
#
#      - B{ThreadsPerProcess:} I{number of threads to start per process}
#
#      - B{Interactive:} I{run the job in interactive mode}
#         - this implies that stdio streams will stay 
#           connected to the submitter after job 
#           submission, and during job execution. 
#         - if an implementation cannot handle
#           interactive jobs, and this attribute is
#           present, and 'True', the job creation MUST
#           throw an 'IncorrectParameter' error with a
#           descriptive error message.
#
#      - B{Input:} I{pathname of the standard input file}
#         - will not be used if 'Interactive' is 'True'
#
#      - B{Cleanup:} I{defines if output files get removed after the job finishes}
#         - can have the Values 'True', 'False', and 
#           'Default'
#         - On 'False', output files MUST be kept 
#           after job the finishes
#         - On 'True', output files MUST be deleted
#           after job the finishes
#         - On 'Default', the behavior is defined by
#           the implementation or the backend.
#         - translates into 'DeleteOnTermination' elements
#           in JSDL
#
#      - B{JobStartTime:} I{time at which a job should be scheduled}
#         - Could be viewed as a desired job start 
#           time, but that is up to the resource 
#           manager. 
#         - format: number of seconds since epoch
#
#      - B{TotalCPUTime:} I{estimate total number of CPU seconds which the job will
#    require}
#         - intended to provide hints to the scheduler. 
#           scheduling policies.
#
#      - B{TotalPhysicalMemory:} I{Estimated amount of memory the job requires}
#         - unit is in MegaByte
#         - memory usage of the job is aggregated 
#           across all processes of the job
#
#      - B{CPUArchitecture:} I{compatible processor for job submission}
#         - allowed values as specified in JSDL
#
#      - B{OperatingSystemType:} I{compatible operating system for job submission}
#         - allowed values as specified in JSDL
#
#      - B{CandidateHosts:} I{list of host names which are to be considered by the
#    resource manager as candidate targets}



    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty job description.'''
        Object.__init__(self, Object.Type.JobDescription, 
                        apitype=Object.Type.JobAPI,)
        AttributeInterface.__init__(self)

        self._executable        = None
        self._arguments         = None
        self._environment       = None
        self._file_transfer     = None
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
        self._register_rw_attribute     (name="Project", 
                                         accessor=self.__class__.project) 

        self._register_rw_vec_attribute (name="Arguments", 
                                         accessor=self.__class__.arguments) 
        self._register_rw_vec_attribute (name="FileTransfer", 
                                         accessor=self.__class__.file_transfer) 
        self._register_rw_vec_attribute (name="Environment", 
                                         accessor=self.__class__.environment) 

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the job description in a civilised fashion.'''
        # nothing to do here 
        pass

    def __str__(self):
        '''String representation of the job description'''
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
    ## Property: 
    def executable():
        doc = "The job executable."
        def fget(self):
            return self._executable
        def fset(self, val):
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'executable' attribute expects 'string' type.")
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
            if type(val) is not list and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'arguments' attribute expects 'list' type.")
            self._arguments = val
        def fdel(self, val):
            self._arguments = None
        return locals()
    arguments = property(**arguments())

    ######################################################################
    ## Property: 
    def file_transfer():
        doc = "The arguments to pass to the file transfer directives."
        def fget(self):
            return self._file_transfer
        def fset(self, val):
            self._file_transfer = val
        def fdel(self, val):
            self._file_transfer = None
        return locals()
    file_transfer = property(**file_transfer())

    ######################################################################
    ## Property: 
    def environment():
        doc = "The environment variables to set in the job's execution context."
        def fget(self):
            return self._environment
        def fset(self, val):
            if type(val) is not dict and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'environment' attribute expects 'dict' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'output' attribute expects 'string' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'error' attribute expects 'string' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'project' attribute expects 'string' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'queue' attribute expects 'string' type.")
            self._queue = val
        def fdel(self, val):
            self._queue = None
        return locals()
    queue = property(**queue())

    ######################################################################
    ## Property:
    def wall_time_limit():
        doc = "The hard limit (in minutes) for the total job runtime."
        def fget(self):
            return self._wall_time_limit
        def fset(self, val):
            if type(val) is not int and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'wall_time_limit' attribute expects 'int' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'working_directory' attribute expects 'string' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'contact' attribute expects 'string' type.")
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
            if type(val) is not int and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'total_cpu_count' attribute expects 'int' type.")
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
            if type(val) is not int and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'number_of_processes' attribute expects 'int' type.")
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
            if type(val) is not str and type(val) is not type(None):
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'spmd_variation' attribute expects 'string' type.")
            self._spmd_variation = val
        def fdel(self, val):
            self._spmd_variation = None
        return locals()
    spmd_variation = property(**spmd_variation())
