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
    etc.) of a :class:`bliss.saga.job.Job` to be create by a :class:`bliss.saga.job.Service`.

    **Usage example 1** shows how to run a /bin/date job::

      jd = saga.job.Description()

      jd.executable = "/bin/date"
      jd.arguments = ["-u", "-R"]

      js = saga.job.Service("fork://localhost")
      j = js.create_job(jd)

      j.run()

    **Usage example 2** shows how to run a set of shell commands as a job::

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

#      - **ProcessesPerHost:** I{number of processes to be started per host}
#
#      - **ThreadsPerProcess:** I{number of threads to start per process}
#
#      - **Interactive:** I{run the job in interactive mode}
#         - this implies that stdio streams will stay 
#           connected to the submitter after job 
#           submission, and during job execution. 
#         - if an implementation cannot handle
#           interactive jobs, and this attribute is
#           present, and 'True', the job creation MUST
#           throw an 'IncorrectParameter' error with a
#           descriptive error message.
#
#      - **Input:** I{pathname of the standard input file}
#         - will not be used if 'Interactive' is 'True'
#
#      - **Cleanup:** I{defines if output files get removed after the job finishes}
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
#      - **JobStartTime:** I{time at which a job should be scheduled}
#         - Could be viewed as a desired job start 
#           time, but that is up to the resource 
#           manager. 
#         - format: number of seconds since epoch
#
#      - **TotalCPUTime:** I{estimate total number of CPU seconds which the job will
#    require}
#         - intended to provide hints to the scheduler. 
#           scheduling policies.
#
#      - **TotalPhysicalMemory:** I{Estimated amount of memory the job requires}
#         - unit is in Mega-Byte
#         - memory usage of the job is aggregated 
#           across all processes of the job
#
#      - **CPUArchitecture:** I{compatible processor for job submission}
#         - allowed values as specified in JSDL
#
#      - **OperatingSystemType:** I{compatible operating system for job submission}
#         - allowed values as specified in JSDL
#
#      - **CandidateHosts:** I{list of host names which are to be considered by the
#    resource manager as candidate targets}


    @staticmethod
    def _deep_copy(jd):
        jd_copy = bliss.saga.job.Description()

        AttributeInterface._attributes_deep_copy (jd, jd_copy)

        return jd_copy

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new, empty job description.'''
        Object.__init__(self)
        self._apitype = 'saga.job'

        # set attribute interface properties
        self._attributes_extensible  (True)
        self._attributes_camelcasing (True)

        # register properties with the attribute interface
        self._attributes_register  ('Executable',        None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Environment',       None, self.Any,    self.Scalar, self.Writable)
        self._attributes_register  ('Arguments',         None, self.String, self.Vector, self.Writable)
        self._attributes_register  ('WorkingDirectory',  None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('FileTransfer',      None, self.String, self.Vector, self.Writable)
        self._attributes_register  ('Output',            None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Error',             None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Queue',             None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Project',           None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('WallTimeLimit',     None, self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('Contact',           None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('Name',              None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('TotalCPUCount',     None, self.Int,    self.Scalar, self.Writable)
        self._attributes_register  ('NumberOfProcesses', None, self.Int,    self.Scalar, self.Writable)
        self._attributes_register  ('SPMDVariation',     None, self.Enum,   self.Scalar, self.Writable)

      # self._attributes_set_enums ('SPMDVariation',     ['MPI', 'OpenMP', 'None'])
        self._attributes_set_enums ('SPMDVariation',     ['MPI', 'OpenMP', 'None', 'single'])

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the job description in a civilised fashion.'''
        # nothing to do here 
        pass


    ######################################################################
    ## Property: 
    Executable = property (doc = """
    Executable:
    Defines the command to execute.

      - This his is the only required attribute/property.
      - It can be a full pathname, a pathname relative to the working_directory as 
        evaluated on the execution host, or a executable name to be searched in the
        target host's PATH environment (if available).

    **Example**::
      jd = saga.job.Description()
      jd.executable = "/usr/local/bin/blast"

    """)
      
    ######################################################################
    ## Property: 
    Arguments = property (doc = """
    Arguments:
    List of arguments for the executable

      - This attribute is optional.
      - The order of arguments is, in general, significant.
      - The individual arguments are not expanded by the user environment (i.e.,
        don't use environment variables like $HOME)
      
    **Example**::
      jd = saga.job.Description()
      jd.arguments = ["--prefix", "/usr/local/bin"]

    """)

    ######################################################################
    ## Property: 
    Environment = property (doc = """
    Environment:
    The environment variables to set in the job's execution context.

      - exported into the job environment
      - format: 'key=value'
      - The individual variable values are not expanded by the user environment (i.e.,
        don't use environment variables like $HOME in values)
      
    **Example**::
      jd = saga.job.Description()
      jd.environment = ["PATH=/bin:/usr/bin", "TARGET=KingKong"]

    """)



    ######################################################################
    ## Property: 
    FileTransfer = property (doc = """
    FileTransfer:
    Defines the file staging operations.

    **Example**::
      jd = saga.job.Description()
      jd.arguments = ["--prefix", "/usr/local/bin"]

    """)

    ######################################################################
    ## Property: 
    Output = property (doc = """
    Output:
    The file in which the job\'s stdout stream will be captured.

    **Example**::
      jd = saga.job.Description()
      jd.output = "/tmp/app.log"

    """)

    ######################################################################
    ## Property: 
    Error = property (doc = """
    Error:
    The file in which the job\'s stderr stream will be captured.

    **Example**::
      jd = saga.job.Description()
      jd.error = "/tmp/app.err"

    """)

    ######################################################################
    ## Property: 
    Project = property (doc = """
    Project:
    The project / allocation name the job should be credited to.

      - This attribute is used by the scheduler backend to credit the allocated
        resources to a specific project account.

    **Example**::
      jd = saga.job.Description()
      jd.project = "project_42"

    """)

    ######################################################################
    ## Property: 
    Queue = property (doc = """
    Queue:
    The queue on the backend system to place the job in.

      - Schedulers which support different queues (with different service
        qualities) use this attribute.

    **Example**::
      jd = saga.job.Description()
      jd.queue = "Large"

    """)

    ######################################################################
    ## Property:
    WallTimeLimit = property (doc = """
    WallTimeLimit:
    The hard limit (in minutes) for the total job runtime.

      - The job is not necessarily killed when it overruns the specified time,
        but no guarantees are made.

      - The value is used by the scheduler to optimized scheduling.

    **Example**::
      jd = saga.job.Description()
      jd.wall_time_limit = "42"

    """)

    ######################################################################
    ## Property: 
    WorkingDirectory = property (doc = """
    WorkingDirectory:
    The working directory for the job.

      - If the directory does not exist, it will be created.
      - Relative path names (for output/error/file_staging) are relative to this
        working directory.

      - The backend may choose an arbitrary working directory if none is
        explicitly specified. 

    **Example**::
      jd = saga.job.Description()
      jd.working_directory = "/scratch/cpt_hook/"

    """)

    ######################################################################
    ## Property: 
    Contact = property (doc = """
    Contact:
    Endpoint describing where to report job state transitions (e.g., email).

      - This information is used to send notifications for job state changes, to
        email or other notification endpoints.

    **Example**::
      jd = saga.job.Description()
      jd.contact = "cpt_hook@piratebay.org"

    """)

    ######################################################################
    ## Property: 
    Name = property (doc = """
    Name:
    Define a name for the job.

      - Defining an explicit name can help debugging on the backend system.

    **Example**::
      jd = saga.job.Description()
      jd.name = "myblastjob_01"

    """)

    ######################################################################
    ## Property: 
    TotalCPUCount = property (doc = """
    TotalCPUCount:
    Total number of cpus requested for this job.

      - This attribute is used for jobs spanning more than one process instance,
        such as for MPI jobs etc.

      - The backend does not make any assumptions about the job distribution
        over the requested processes, nor does it give any connectivity
        guarantees (NUMA, shared memory, network interconnects etc.)

    **Example**::
      jd = saga.job.Description()
      jd.total_cpu_count = 64

    """)

    ######################################################################
    ## Property: 
    NumberOfProcesses = property (doc = """
    NumberOfProcesses:
    Number of processes to launch

      - This attribute specifies how many process instances the application is
        expected to have.  

      - Specifying this attribute does *not* automatically create those
        instances, but instead acts as a hint (boundary condition) to the
        scheduler.

    **Example**::
      jd = saga.job.Description()
      jd.number_of_processes = 8

    """)

    ######################################################################
    ## Property: 
    SPMDVariation = property (doc = """
    SPMDVariation:
    SPMD job type and startup mechanism

      - supported values: MPI, OpenMP, None
      - 'None' indicates that the application is not a SPMD application.
      - Specifying this value influences the mechanism the backend will use to
        create the application process instances (fork, mpirun, ...)

    **Example**::
      jd = saga.job.Description()
      jd.spmd_variation = "MPI"

    """)

