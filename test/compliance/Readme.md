Compliance Test Results
=======================

Plug-In: SSH Job
----------------

  * URL: **ssh://192.168.2.112**, Info: OS X 10.7, Date: 05/01/2012, 
    Git hash (git log -1): 991b5b8670fc2702ccd5c16c794e5b6b2eac37f9
    * 01_run_remote_exe.py ssh://192.168.2.112 s1063117: **PASS**
    * 02_run_shell_command_newline.py ssh://192.168.2.112 s1063117: **PASS**
    * 03_run_shell_command_multiline.py ssh://192.168.2.112 s1063117: **PASS**
    * 04_run_python_command_newline.py ssh://192.168.2.112 s1063117: **PASS**
    * 05_run_python_command_multiline.py ssh://192.168.2.112 s1063117: **PASS**

  * URL: ssh://ranger from Lonestar
   * By default, All tests fail with:

Exception: Couldn't find a plugin for URL scheme 'ssh://' and API type 'saga.job'

This is because the locally-installed BLISS is older than the version in the virtualenv, and the
virtualenv still picks it up.

You can work around this by doing:
export PYTHONPATH=

and then running the tests.  After you do this:

  * 01_run_remote_exe.py: **PASS**
  * 02_run_shell_command_newline.py: **PASS**
  * 03_run_shell_command_multiline.py: **FAIL**
  * 04_run_python_command_newline.py: **FAIL**
  * 05_run_python_command_multiline.py: **FAIL**

The problem seems to be with this line of code in the SSH adaptor:

    args = ""
        if self.arguments is not None:
            for arg in self.arguments:
                cmdline += " %r" % arg

Which creates things like:
04/16/2012 09:56:42 AM - bliss.SSHJobPlugin(0x12122a28) - DEBUG - Sending command echo $$ && (env MYOUTPUT="Hello from Bliss"  /bin/sh -c 'python '-c' '"\nimport sys\nimport os  \nprint os.environ[\'MYOUTPUT\']\nprint sys.version\n"'')> bliss_job.stdout 2> bliss_job.stderr to remote server:

If you change it to:

    args = ""
        if self.arguments is not None:
            for arg in self.arguments:
                cmdline += " %s" % arg
                
Then we get:
04/16/2012 10:00:17 AM - bliss.SSHJobPlugin(0x130bda28) - DEBUG - Sending command echo $$ && (env MYOUTPUT="Hello from Bliss"  /bin/sh -c 'python -c "import sys 

import os 

print os.environ['MYOUTPUT'] 

print sys.version"')> bliss_job.stdout 2> bliss_job.stderr to remote server:

Which still fails.

Any ideas?  The obvious way of getting around this is creating a remote bash script that is executed by the SSH adaptor.  The problem with this approach is that then you have to worry about multiple SSH adaptor instances potentially overwriting each other's scripts.  Is there an easier way to pass multi-line commands with SSH?

Plug-In: Local (Fork) Job
-------------------------

  * URL: **fork://localhost**, Info: OS X 10.7, Date: 04/08/2012, 
    Git hash (git log -1): 81b5df0eff27ade309416afb066c4e691c8d5f70 
    * 01_run_remote_exe.py: **PASS**
    * 02_run_shell_command_newline.py: **PASS**
    * 03_run_shell_command_multiline.py: **PASS**
    * 04_run_python_command_newline.py: **PASS**
    * 05_run_python_command_multiline.py: **PASS**
    * 06_job_container_01.py **FAIL** (Containers not implemented)
    * 07_work_directory.py fork://localhost /tmp **PASS**
    * 08_absolute_output.py fork://localhost /tmp/F **PASS**

  * URL: **fork://localhost**, Info: Ubuntu Server 10.11, Date: 04/08/2012, 
    Git hash (git log -1): 823a82b1b0c797bc97063530cc17a84b35d0dc92
    * 01_run_remote_exe.py: **PASS**
    * 02_run_shell_command_newline.py: **PASS**
    * 03_run_shell_command_multiline.py: **PASS**
    * 04_run_python_command_newline.py: **PASS**
    * 05_run_python_command_multiline.py: **PASS**

AM: can confirm fork to be working, output ok, on ubuntu-10.10 python 2.6.6

Plug-In: PBS(+SSH) Job
----------------------

  * URL: **pbs+ssh://alamo.futuregrid.org**, Info: FutureGrid Alamo Cluster, PBS 2.4.8, Date: 04/21/2012, 
    Git hash (git log -1): 81b5df0eff27ade309416afb066c4e691c8d5f70 
    * 01_run_remote_exe.py: **PASS**
    * 02_run_shell_command_newline.py: **PASS**
    * 03_run_shell_command_multiline.py: **PASS**
    * 04_run_python_command_newline.py: **PASS**
    * 05_run_python_command_multiline.py: **PASS**
    * 06_
    * 07_
    * 08_absolute_output.py pbs+ssh://alamo.futuregrid.org /tmp/ **PASS**

** installation on india.fg ** (AM)

Red Hat ELS 5.8, Python 2.7

pip, easy install and virtualenv are not available, neither with the
default system python, nor with the python module loaded.
So, installation has to be done via the pystrap script linked on
https://github.com/saga-project/bliss/wiki/Installation, and then from
git (which needs module load git)

The pystrap script seems to work, but gives the following errors with
the default system python:

    ...
    Running setup.py install for furl
      File "/N/u/merzky/mypy_u10054/lib/python2.4/site-packages/furl/furl.py", line 92
        self._isabsolute = True if segments else False
                                 ^
    SyntaxError: invalid syntax
      File "/N/u/merzky/mypy_u10054/lib/python2.4/site-packages/furl/__init__.py", line 17
        from .furl import *
             ^
    SyntaxError: invalid syntax
    Running setup.py install for pycrypto-on-pypi
    ...
    src/MD2.c:31:20: error: Python.h: No such file or directory
    ...
    error: command 'gcc' failed with exit status 1
    ...


'module load python' gets pystrap running successfully (seems to have
python devel included).


** Plug-In: PBS, PBS+SSH Job**

*** hotel ***
 
results::

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_core_00.py pbs+ssh://hotel.futuregrid.org/'
  | hotel        | core    | -          | -                                                       |  ok |

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_01.sh pbs+ssh://hotel.futuregrid.org/'

  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
    SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)

  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_02.sh pbs+ssh://hotel.futuregrid.org/'
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
    SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)

  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_03.sh pbs+ssh://hotel.futuregrid.org/'
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
    SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)

  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_05.sh pbs+ssh://hotel.futuregrid.org/'
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
    SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)

  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |

  bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_04.sh pbs+ssh://hotel.futuregrid.org/'
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
    SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)

  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |


*** hotel ***
 
results::

  log file                  /gpfs/software/x86_64/el5/hotel/SAGA/csa//test/test.saga-1.6.gcc-4.1.2.hotel.2012-05-08.bliss.log
  hostname                  hotel
  time stamp                2012-05-08
  csa  location             /gpfs/software/x86_64/el5/hotel/SAGA
  csa  target               /gpfs/software/x86_64/el5/hotel/SAGA/saga/
  saga version              1.6
  make version              GNU Make 3.81
  compiler version          gcc-4.1.2
  using /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/x509_test.pem as X509_USER_PROXY
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | TEST SUMMARY                                                                                        |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | host         | type    | name       | info                                                    | res | 
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | running bliss tests                                                                                 |
  |                                                                                                     |
  | csa_test_bliss_core_00.py                                                                           |
  | hotel        | core    | -          | -                                                       |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_01.sh                                                                            |
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_02.sh                                                                            |
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_03.sh                                                                            |
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_04.sh                                                                            |
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_05.sh                                                                            |
  | hotel        | job     | fork       | fork://localhost/                                       |  ok |
  | hotel        | job     | ssh        | ssh://localhost/                                        |  ok |
  | hotel        | job     | pbs        | pbs://localhost/                                        |  ok |
  | hotel        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | hotel        | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | hotel        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | hotel        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | ok : 51                                                                                             |
  | nok: 5                                                                                              |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  
  
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | DETAILED ERROR LOG                                                                                  |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | hotel        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | bash -c '. /gpfs/software/x86_64/el5/hotel/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /gpfs/software/x86_64/el5/hotel/SAGA/csa///test/csa_test_bliss_job_01.sh pbs+ssh://alamo.futuregrid.org/'
  | stdout / stderr: 
  05/08/2012 01:30:09 AM - bliss.PBSJobPlugin(0x10142c68) - ERROR - Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin)
  05/08/2012 01:30:09 AM - bliss.PBSJobPlugin(0x10142c68) - ERROR - Couldn't run job because: SAGA Exception (11): [saga.plugin.job.pbssh] Couldn't find PBS command line tools on pbs+ssh://alamo.futuregrid.org/: which: no pbsnodes in (/usr/local/bin:/bin:/usr/bin) 
    *********************
    * BLISS STACK TRACE *
    *********************
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 130, in <module>
      sys.exit(main())
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 126, in main
      return run(js_url, remoteusername, queue, project)
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 48, in run
      myjob.run()
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/saga/job/Job.py", line 287, in run
      return self._plugin.job_run(self)
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/pbsshjob.py", line 253, in job_run
      jobinfo = pbs.submit_job(job)
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/cmdlinewrapper.py", line 553, in submit_job
      self._check_context()
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/cmdlinewrapper.py", line 309, in _check_context
      % (self._url, result.stderr))
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/interface/pluginbase.py", line 35, in log_error_and_raise
      msg = "[%s] %s %s" % (self.name, message, tback.get_traceback())
    File "/gpfs/software/x86_64/el5/hotel/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/utils/tback.py", line 14, in get_traceback
      traceback.print_stack(file=fp)
   
    ...
    
*All other pbs tests on alamo failed with the same error*


*** sierra ***

results:

  log file                  /N/soft/SAGA/csa//test/test.saga-1.6.gcc-4.1.2.sierra.2012-05-07.bliss.log
  hostname                  sierra
  time stamp                2012-05-07
  csa  location             /N/soft/SAGA
  csa  target               /N/soft/SAGA/saga/
  saga version              1.6
  make version              GNU Make 3.81
  compiler version          gcc-4.1.2
  using /N/soft/SAGA/csa///test/x509_test.pem as X509_USER_PROXY
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | TEST SUMMARY                                                                                        |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | host         | type    | name       | info                                                    | res | 
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | running bliss tests                                                                                 |
  |                                                                                                     |
  | csa_test_bliss_core_00.py                                                                           |
  | sierra       | core    | -          | -                                                       |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_01.sh                                                                            |
  | sierra       | job     | fork       | fork://localhost/                                       |  ok |
  | sierra       | job     | ssh        | ssh://localhost/                                        |  ok |
  | sierra       | job     | pbs        | pbs://localhost/                                        |  ok |
  | sierra       | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | sierra       | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_02.sh                                                                            |
  | sierra       | job     | fork       | fork://localhost/                                       |  ok |
  | sierra       | job     | ssh        | ssh://localhost/                                        |  ok |
  | sierra       | job     | pbs        | pbs://localhost/                                        |  ok |
  | sierra       | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | sierra       | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_03.sh                                                                            |
  | sierra       | job     | fork       | fork://localhost/                                       |  ok |
  | sierra       | job     | ssh        | ssh://localhost/                                        |  ok |
  | sierra       | job     | pbs        | pbs://localhost/                                        |  ok |
  | sierra       | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | sierra       | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_04.sh                                                                            |
  | sierra       | job     | fork       | fork://localhost/                                       |  ok |
  | sierra       | job     | ssh        | ssh://localhost/                                        |  ok |
  | sierra       | job     | pbs        | pbs://localhost/                                        |  ok |
  | sierra       | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | sierra       | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_05.sh                                                                            |
  | sierra       | job     | fork       | fork://localhost/                                       |  ok |
  | sierra       | job     | ssh        | ssh://localhost/                                        |  ok |
  | sierra       | job     | pbs        | pbs://localhost/                                        |  ok |
  | sierra       | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | sierra       | job     | ssh        | ssh://hotel.futuregrid.org/                             |  ok |
  | sierra       | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | sierra       | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         |  ok |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 
  | ok : 51                                                                                             |
  | nok: 5                                                                                              |
  +--------------+---------+------------+---------------------------------------------------------+-----+ 

  
*All pbs tests on alamo failed with the same error as above (hotel)*


*** alamo ***

Could not install bliss, as there is no devel version of python, thus paramiko
does not compile.  I did not investigate further...


*** india ***

results::

  log file                  /N/soft/SAGA/csa//test/test.saga-1.6.gcc-4.1.2.india.2012-05-08.bliss.log
  hostname                  india
  time stamp                2012-05-08
  csa  location             /N/soft/SAGA
  csa  target               /N/soft/SAGA/saga/
  saga version              1.6
  make version              GNU Make 3.81
  compiler version          gcc-4.1.2
  using /N/soft/SAGA/csa///test/x509_test.pem as X509_USER_PROXY
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | TEST SUMMARY                                                                                        |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | host         | type    | name       | info                                                    | res |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | running bliss tests                                                                                 |
  |                                                                                                     |
  | csa_test_bliss_core_00.py                                                                           |
  | india        | core    | -          | -                                                       |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_01.sh                                                                            |
  | india        | job     | fork       | fork://localhost/                                       |  ok |
  | india        | job     | ssh        | ssh://localhost/                                        |  ok |
  | india        | job     | pbs        | pbs://localhost/                                        |  ok |
  | india        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | india        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | india        | job     | ssh        | ssh://hotel.futuregrid.org/                             | nok |
  | india        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | india        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         | nok |
  |                                                                                                     |
  | csa_test_bliss_job_02.sh                                                                            |
  | india        | job     | fork       | fork://localhost/                                       |  ok |
  | india        | job     | ssh        | ssh://localhost/                                        |  ok |
  | india        | job     | pbs        | pbs://localhost/                                        |  ok |
  | india        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | india        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | india        | job     | ssh        | ssh://hotel.futuregrid.org/                             | nok |
  | india        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | india        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         | nok |
  |                                                                                                     |
  | csa_test_bliss_job_03.sh                                                                            |
  | india        | job     | fork       | fork://localhost/                                       |  ok |
  | india        | job     | ssh        | ssh://localhost/                                        |  ok |
  | india        | job     | pbs        | pbs://localhost/                                        |  ok |
  | india        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | india        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | india        | job     | ssh        | ssh://hotel.futuregrid.org/                             | nok |
  | india        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | india        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         | nok |
  |                                                                                                     |
  | csa_test_bliss_job_04.sh                                                                            |
  | india        | job     | fork       | fork://localhost/                                       |  ok |
  | india        | job     | ssh        | ssh://localhost/                                        |  ok |
  | india        | job     | pbs        | pbs://localhost/                                        |  ok |
  | india        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | india        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | india        | job     | ssh        | ssh://hotel.futuregrid.org/                             | nok |
  | india        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | india        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         | nok |
  |                                                                                                     |
  | csa_test_bliss_job_05.sh                                                                            |
  | india        | job     | fork       | fork://localhost/                                       |  ok |
  | india        | job     | ssh        | ssh://localhost/                                        |  ok |
  | india        | job     | pbs        | pbs://localhost/                                        |  ok |
  | india        | job     | ssh        | ssh://india.futuregrid.org/                             |  ok |
  | india        | job     | ssh        | ssh://sierra.futuregrid.org/                            |  ok |
  | india        | job     | ssh        | ssh://hotel.futuregrid.org/                             | nok |
  | india        | job     | ssh        | ssh://alamo.futuregrid.org/                             |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://india.futuregrid.org/                         |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://sierra.futuregrid.org/                        |  ok |
  | india        | job     | pbs+ssh    | pbs+ssh://alamo.futuregrid.org/                         | nok |
  | india        | job     | pbs+ssh    | pbs+ssh://hotel.futuregrid.org/                         | nok |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | ok : 41                                                                                             |
  | nok: 15                                                                                             |
  +--------------+---------+------------+---------------------------------------------------------+-----+


For some reason, the home FS on hotel is mounted RO right now, and thus I could
not setup ssh propely - thus ssh from india to hotel failed.


*All pbs tests on alamo failed with the same error as above (hotel)*



*** kraken ***

results::

  log file                  /lustre/scratch/proj/saga/csa//test/test.saga-1.6.gcc-4.3.2.kraken.2012-05-08.bliss.log
  hostname                  kraken
  time stamp                2012-05-08
  csa  location             /lustre/scratch/proj/saga
  csa  target               /lustre/scratch/proj/saga/saga/
  saga version              1.6
  make version              GNU Make 3.81
  compiler version          gcc-4.3.2
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | TEST SUMMARY                                                                                        |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | host         | type    | name       | info                                                    | res |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | running bliss tests                                                                                 |
  |                                                                                                     |
  | csa_test_bliss_core_00.py                                                                           |
  | kraken       | core    | -          | -                                                       |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_01.sh                                                                            |
  | kraken       | job     | fork       | fork://localhost/                                       |  ok |
  | kraken       | job     | pbs        | pbs://localhost/                                        |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_02.sh                                                                            |
  | kraken       | job     | fork       | fork://localhost/                                       |  ok |
  | kraken       | job     | pbs        | pbs://localhost/                                        |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_03.sh                                                                            |
  | kraken       | job     | fork       | fork://localhost/                                       |  ok |
  | kraken       | job     | pbs        | pbs://localhost/                                        |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_04.sh                                                                            |
  | kraken       | job     | fork       | fork://localhost/                                       |  ok |
  | kraken       | job     | pbs        | pbs://localhost/                                        |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_05.sh                                                                            |
  | kraken       | job     | fork       | fork://localhost/                                       |  ok |
  | kraken       | job     | pbs        | pbs://localhost/                                        |  ok |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | ok : 11                                                                                             |
  | nok: 0                                                                                              |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  
  
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | DETAILED ERROR LOG                                                                                  |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | ok : 11                                                                                             |
  | nok: 0                                                                                              |
  +--------------+---------+------------+---------------------------------------------------------+-----+


*** lonestar ***

results::

  log file                  /share1/projects/xsede/SAGA/csa//test/test.saga-1.6.gcc-4.1.2.lonestar.2012-05-08.bliss.log
  hostname                  lonestar
  time stamp                2012-05-08
  csa  location             /share1/projects/xsede/SAGA
  csa  target               /share1/projects/xsede/SAGA/saga/
  saga version              1.6
  make version              GNU Make 3.81
  compiler version          gcc-4.1.2
  using /share1/projects/xsede/SAGA/csa///test/x509_test.pem as X509_USER_PROXY
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | TEST SUMMARY                                                                                        |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | host         | type    | name       | info                                                    | res |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | running bliss tests                                                                                 |
  |                                                                                                     |
  | csa_test_bliss_core_00.py                                                                           |
  | lonestar     | core    | -          | -                                                       |  ok |
  |                                                                                                     |
  | csa_test_bliss_job_01.sh                                                                            |
  | lonestar     | job     | fork       | fork://localhost/                                       |  ok |
  | lonestar     | job     | ssh        | ssh://localhost/                                        |  ok |
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  |                                                                                                     |
  | csa_test_bliss_job_02.sh                                                                            |
  | lonestar     | job     | fork       | fork://localhost/                                       |  ok |
  | lonestar     | job     | ssh        | ssh://localhost/                                        |  ok |
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  |                                                                                                     |
  | csa_test_bliss_job_03.sh                                                                            |
  | lonestar     | job     | fork       | fork://localhost/                                       |  ok |
  | lonestar     | job     | ssh        | ssh://localhost/                                        |  ok |
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  |                                                                                                     |
  | csa_test_bliss_job_04.sh                                                                            |
  | lonestar     | job     | fork       | fork://localhost/                                       |  ok |
  | lonestar     | job     | ssh        | ssh://localhost/                                        |  ok |
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  |                                                                                                     |
  | csa_test_bliss_job_05.sh                                                                            |
  | lonestar     | job     | fork       | fork://localhost/                                       |  ok |
  | lonestar     | job     | ssh        | ssh://localhost/                                        |  ok |
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | ok : 11                                                                                             |
  | nok: 10                                                                                             |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  
  
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | DETAILED ERROR LOG                                                                                  |
  +--------------+---------+------------+---------------------------------------------------------+-----+
  | lonestar     | job     | pbs        | pbs://localhost/                                        | nok |
  | bash -c '. /share1/projects/xsede/SAGA/csa///../saga/bliss/pyvirt/bin/activate ; bash /share1/projects/xsede/SAGA/csa///test/csa_test_bliss_job_01.sh pbs://localhost/'
  | stdout / stderr:
  05/08/2012 12:33:22 PM - bliss.PBSJobPlugin(0x1d16d248) - ERROR - Couldn't find PBS tools on pbs://localhost/
  05/08/2012 12:33:22 PM - bliss.PBSJobPlugin(0x1d16d248) - ERROR - Couldn't run job because: SAGA Exception (NoSuccess): [saga.plugin.job.pbssh] Couldn't find PBS tools on pbs://localhost/
    *********************
    * BLISS STACK TRACE *
    *********************
    File "/share1/projects/xsede/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 130, in <module>
      sys.exit(main())
    File "/share1/projects/xsede/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 126, in main
      return run(js_url, remoteusername, queue, project)
    File "/share1/projects/xsede/SAGA/saga//bliss//bliss/test/compliance/job/01_run_remote_exe.py", line 48, in run
      myjob.run()
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/saga/job/Job.py", line 287, in run
      return self._plugin.job_run(self)
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/pbsshjob.py", line 253, in job_run
      jobinfo = pbs.submit_job(job)
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/cmdlinewrapper.py", line 553, in submit_job
      self._check_context()
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/plugins/pbs/cmdlinewrapper.py", line 257, in _check_context
      "Couldn't find PBS tools on %s" % (self._url))
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/interface/pluginbase.py", line 35, in log_error_and_raise
      msg = "[%s] %s %s" % (self.name, message, tback.get_traceback())
    File "/share1/projects/xsede/SAGA/saga/bliss/pyvirt/lib/python2.7/site-packages/bliss-0.1.21-py2.7.egg/bliss/utils/tback.py", line 14, in get_traceback
      traceback.print_stack(file=fp)
  
    ...

*All other pbs tests failed with the same error*
  



Plug-In: SGE(+SSH) Job
----------------------



