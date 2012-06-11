# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.Object import Object
from bliss.saga.Attributes import AttributeInterface

class Description(Object, AttributeInterface):
    """
    Allows to define the properties and requirements for a job.
  
    The Description class allows the user to describes both the resource
    requirements (e.g. number  of CPUs, working directory etc.), as well as the
    application properties (e.g. executable path, program arguments, environment
    etc.) of a L{job.Job} to be create by a L{job.Service}.

    B{Usage example 1} shows how to run a /bin/date job::

      jd = saga.job.Description()

      jd.executable = "/bin/date"
      jd.arguments = ["-u", "-R"]

      js = saga.job.Service("fork://localhost")
      j = js.create_job(jd)

      j.run()

    B{Usage example 2} shows how to run a set of shell commands as a job::

      script = '''
       ls -la /tmp
       find  /tmp/ -name  \*.pdf -exec echo "found {}" \;
       du -a /tmp/ | egrep '\.pdf$' | wc -l
      '''

      jd = saga.job.Description()

      jd.executable = "/bin/sh"
      jd.arguments  = ["-c", script]

      js = saga.job.Service("fork://localhost")
      j  = js.create_job(jd)

      j.run()

    Note that the above example uses /bin/sh explicitly, instead of, say,
    /bin/bash -- it is good practice to use /bin/sh and sh compatible shell
    scripts, as those are guaranteed to be available on all Unix systems.

    """

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
#         - unit is in Mega-Byte
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


    @staticmethod
    def _deep_copy(jd):
        jd_copy = bliss.saga.job.Description()

        # properties
        jd_copy._executable          = jd._executable
        jd_copy._arguments           = jd._arguments
        jd_copy._environment         = jd._environment
        jd_copy._file_transfer       = jd._file_transfer
        jd_copy._project             = jd._project
        jd_copy._output              = jd._output
        jd_copy._error               = jd._error
        jd_copy._working_directory   = jd._working_directory
        jd_copy._contact             = jd._contact
        # requirements 
        jd_copy._total_cpu_count     = jd._total_cpu_count
        jd_copy._wall_time_limit     = jd._wall_time_limit
        jd_copy._number_of_processes = jd._number_of_processes
        jd_copy._spmd_variation      = jd._spmd_variation
        jd_copy._queue               = jd._queue

        return jd_copy

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty job description.'''
        Object.__init__(self, Object.Type.JobDescription, 
                        apitype=Object.Type.JobAPI,)
        AttributeInterface.__init__(self)

        # properties
        self._executable          = None
        self._arguments           = None
        self._environment         = None
        self._file_transfer       = None
        self._project             = None
        self._output              = None
        self._error               = None
        self._working_directory   = None
        self._contact             = None

        # requirements 
        self._total_cpu_count     = None
        self._wall_time_limit     = None
        self._number_of_processes = None
        self._spmd_variation      = None
        self._queue               = None


        # register properties with the attribute interface
        self._register_rw_attribute(name="Executable", 
                                    accessor=self.__class__.executable) 
        self._register_rw_attribute(name="Output", 
                                    accessor=self.__class__.output) 
        self._register_rw_attribute(name="Error", 
                                    accessor=self.__class__.error) 
        self._register_rw_attribute(name="Queue", 
                                    accessor=self.__class__.queue) 
        self._register_rw_attribute(name="WallTimeLimit", 
                                    accessor=self.__class__.wall_time_limit) 
        self._register_rw_attribute(name="WorkingDirectory", 
                                    accessor=self.__class__.working_directory) 
        self._register_rw_attribute(name="Contact", 
                                    accessor=self.__class__.contact) 
        self._register_rw_attribute(name="TotalCPUCount", 
                                    accessor=self.__class__.total_cpu_count) 
        self._register_rw_attribute(name="NumberOfProcesses", 
                                    accessor=self.__class__.number_of_processes) 
        self._register_rw_attribute(name="SPMDVariation", 
                                    accessor=self.__class__.spmd_variation) 
        self._register_rw_attribute(name="Project", 
                                    accessor=self.__class__.project) 

        self._register_rw_vec_attribute(name="Arguments", 
                                        accessor=self.__class__.arguments) 
        self._register_rw_vec_attribute(name="FileTransfer", 
                                        accessor=self.__class__.file_transfer) 
        self._register_rw_vec_attribute(name="Environment", 
                                        accessor=self.__class__.environment) 

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the job description in a civilised fashion.'''
        # nothing to do here 
        pass


    ######################################################################
    ## Property: 
    def executable():
        doc = "Defines the command to execute."
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
    """
    Defines the command to execute.
      - This his is the only required attribute/property.
      - It can be a full pathname, a pathname relative to the working_directory as 
        evaluated on the execution host, or a executable name to be searched in the
        target host's PATH environment (if available).

    B{Example}::
      jd = saga.job.Description()
      jd.executable = "/usr/local/bin/blast"

    """
      
    ######################################################################
    ## Property: 
    def arguments():
        doc = "List of arguments for the executable."
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
    """
    List of arguments for the executable
      - This attribute is optional.
      - The order of arguments is, in general, significant.
      - The individual arguments are not expanded by the user environment (i.e.,
        don't use environment variables like $HOME)
      
    B{Example}::
      jd = saga.job.Description()
      jd.arguments = ["--prefix", "/usr/local/bin"]

    """

    ######################################################################
    ## Property: 
    def environment():
        doc = "The environment variables to set in the job's execution context."
        def fget(self):
            return self._environment
        def fset(self, val):
            if type(val) is dict or type(val) is type(None):
                self._environment = val
            elif type(val) is list:
                d = dict()
                for list_item in val:
                    (key, val) = list_item.split("=")
                    d[key] = val
                self._environment = d
            else:
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'environment' attribute expects 'dict' type.")
        def fdel(self, val):
            self._environment = None
        return locals()
    environment = property(**environment())
    """
    The environment variables to set in the job's execution context.
      - exported into the job environment
      - format: 'key=value'
      - The individual variable values are not expanded by the user environment (i.e.,
        don't use environment variables like $HOME in values)
      
    B{Example}::
      jd = saga.job.Description()
      jd.environment = ["PATH=/bin:/usr/bin", "TARGET=KingKong"]

    """



    ######################################################################
    ## Property: 
    def file_transfer():
        doc = "Defines the file staging operations."
        def fget(self):
            return self._file_transfer
        def fset(self, val):
            self._file_transfer = val
        def fdel(self, val):
            self._file_transfer = None
        return locals()
    file_transfer = property(**file_transfer())
    """
    Defines the file staging operations.

    B{Example}::
      jd = saga.job.Description()
      jd.arguments = ["--prefix", "/usr/local/bin"]

    """

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
    """
    The file in which the job\'s stdout stream will be captured.

    B{Example}::
      jd = saga.job.Description()
      jd.output = "/tmp/app.log"

    """

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
    """
    The file in which the job\'s stderr stream will be captured.

    B{Example}::
      jd = saga.job.Description()
      jd.error = "/tmp/app.err"

    """

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
    """
    The project / allocation name the job should be credited to.
      - This attribute is used by the scheduler backend to credit the allocated
        resources to a specific project account.

    B{Example}::
      jd = saga.job.Description()
      jd.project = "project_42"

    """

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
    """
    The queue on the backend system to place the job in.
      - Schedulers which support different queues (with different service
        qualities) use this attribute.

    B{Example}::
      jd = saga.job.Description()
      jd.queue = "Large"

    """

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
    """
    The hard limit (in minutes) for the total job runtime.
      - The job is not necessarily killed when it overruns the specified time,
        but no guarantees are made.
      - The value is used by the scheduler to optimized scheduling.

    B{Example}::
      jd = saga.job.Description()
      jd.wall_time_limit = "42"

    """

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
    """
    The working directory for the job.
      - If the directory does not exist, it will be created.
      - Relative path names (for output/error/file_staging) are relative to this
        working directory.
      - The backend may choose an arbitrary working directory if none is
        explicitly specified. 

    B{Example}::
      jd = saga.job.Description()
      jd.working_directory = "/scratch/cpt_hook/"

    """

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

    """
    Endpoint describing where to report job state transitions (e.g., email).
      - This information is used to send notifications for job state changes, to
        email or other notification endpoints.

    B{Example}::
      jd = saga.job.Description()
      jd.contact = "cpt_hook@piratebay.org"

    """

    ######################################################################
    ## Property: 
    def total_cpu_count():
        doc = "Total number of CPUs requested for this job."
        def fget(self):
            return self._total_cpu_count
        def fset(self, val):
            if type(val) is int or type(val) is None:
                self._total_cpu_count = val
            elif type(val) is str:
                self._total_cpu_count = int(val)
            else: 
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'total_cpu_count' attribute expects 'int' or 'str' type.")
        def fdel(self, val):
            self._total_cpu_count = None
        return locals()
    total_cpu_count = property(**total_cpu_count())
    """
    Total number of cpus requested for this job.
      - This attribute is used for jobs spanning more than one process instance,
        such as for MPI jobs etc.
      - The backend does not make any assumptions about the job distribution
        over the requested processes, nor does it give any connectivity
        guarantees (NUMA, shared memory, network interconnects etc.)

    B{Example}::
      jd = saga.job.Description()
      jd.total_cpu_count = 64

    """

    ######################################################################
    ## Property: 
    def number_of_processes():
        doc = "Number of processes to launch"
        def fget(self):
            return self._number_of_processes
        def fset(self, val):
            if type(val) is int or type(val) is None:
                self._total_cpu_count = val
            elif type(val) is str:
                self._total_cpu_count = int(val)
            else:
                raise bliss.saga.Exception(bliss.saga.Error.BadParameter, "'number_of_processes' attribute expects 'int' or 'str' type.")
        def fdel(self, val):
            self._number_of_processes = None
        return locals()
    number_of_processes = property(**number_of_processes())
    """
    Number of processes to launch
      - This attribute specifies how many process instances the application is
        expected to have.  
      - Specifying this attribute does *not* automatically create those
        instances, but instead acts as a hint (boundary condition) to the
        scheduler.

    B{Example}::
      jd = saga.job.Description()
      jd.number_of_processes = 8

    """

    ######################################################################
    ## Property: 
    def spmd_variation():
        doc = "SPMD job type and startup mechanism (MPI, OpenMP, None, ...)"
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
    """
    SPMD job type and startup mechanism
      - supported values: MPI, OpenMP, None
      - 'None' indicates that the application is not a SPMD application.
      - Specifying this value influences the mechanism the backend will use to
        create the application process instances (fork, mpirun, ...)

    B{Example}::
      jd = saga.job.Description()
      jd.spmd_variation = "MPI"

    """

