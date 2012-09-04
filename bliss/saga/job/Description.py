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

        AttributeInterface.attributes_deep_copy_ (jd, jd_copy)

        return jd_copy

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty job description.'''
        Object.__init__(self, Object.ObjectType.JobDescription, 
                        apitype=Object.ObjectType.JobAPI,)

        # set attribute interface properties
        self.attributes_extensible_  (True)
        self.attributes_camelcasing_ (True)

        # register properties with the attribute interface
        self.attributes_register_  ('Executable',        None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('Environment',       None, self.Any,    self.Scalar, self.Writable)
        self.attributes_register_  ('Arguments',         None, self.String, self.Vector, self.Writable)
        self.attributes_register_  ('WorkingDirectory',  None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('FileTransfer',      None, self.String, self.Vector, self.Writable)
        self.attributes_register_  ('Output',            None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('Error',             None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('Queue',             None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('Project',           None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('WallTimeLimit',     None, self.Time,   self.Scalar, self.Writable)
        self.attributes_register_  ('Contact',           None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('Name',              None, self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('TotalCPUCount',     None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_  ('NumberOfProcesses', None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_  ('SPMDVariation',     None, self.Enum,   self.Scalar, self.Writable)

      # self.attributes_set_enums_ ('SPMDVariation',     ['MPI', 'OpenMP', 'None'])
        self.attributes_set_enums_ ('SPMDVariation',     ['MPI', 'OpenMP', 'None', 'single'])

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the job description in a civilised fashion.'''
        # nothing to do here 
        pass


    ######################################################################
    ## Property: 
    """
    Executable:
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
    """
    Arguments:
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
    """
    Environment:
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
    """
    File Transfer:
    Defines the file staging operations.

    B{Example}::
      jd = saga.job.Description()
      jd.arguments = ["--prefix", "/usr/local/bin"]

    """

    ######################################################################
    ## Property: 
    """
    Output:
    The file in which the job\'s stdout stream will be captured.

    B{Example}::
      jd = saga.job.Description()
      jd.output = "/tmp/app.log"

    """

    ######################################################################
    ## Property: 
    """
    Error:
    The file in which the job\'s stderr stream will be captured.

    B{Example}::
      jd = saga.job.Description()
      jd.error = "/tmp/app.err"

    """

    ######################################################################
    ## Property: 
    """
    Project:
    The project / allocation name the job should be credited to.
      - This attribute is used by the scheduler backend to credit the allocated
        resources to a specific project account.

    B{Example}::
      jd = saga.job.Description()
      jd.project = "project_42"

    """

    ######################################################################
    ## Property: 
    """
    Queue:
    The queue on the backend system to place the job in.
      - Schedulers which support different queues (with different service
        qualities) use this attribute.

    B{Example}::
      jd = saga.job.Description()
      jd.queue = "Large"

    """

    ######################################################################
    ## Property:
    """
    WallTimeLimit:
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
    """
    WorkingDirectory:
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
    """
    Contact:
    Endpoint describing where to report job state transitions (e.g., email).
      - This information is used to send notifications for job state changes, to
        email or other notification endpoints.

    B{Example}::
      jd = saga.job.Description()
      jd.contact = "cpt_hook@piratebay.org"

    """

    ######################################################################
    ## Property: 
    """
    Name:
    Define a name for the job.
      - Defining an explicit name can help debugging on the backend system.
    B{Example}::
      jd = saga.job.Description()
      jd.name = "myblastjob_01"

    """

    ######################################################################
    ## Property: 
    """
    TotalCPUCount:
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
    """
    NumberOfProcesses:
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
    """
    SPMDVariation:
    SPMD job type and startup mechanism
      - supported values: MPI, OpenMP, None
      - 'None' indicates that the application is not a SPMD application.
      - Specifying this value influences the mechanism the backend will use to
        create the application process instances (fork, mpirun, ...)

    B{Example}::
      jd = saga.job.Description()
      jd.spmd_variation = "MPI"

    """

