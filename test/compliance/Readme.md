Compliance Test Results
=======================

Plug-In: SSH Job
----------------
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
    Git hash (git log -1): d5b9c9361f2943dcd4e95e804c812208a2c56d58 
    * 01_run_remote_exe.py: **PASS**
    * 02_run_shell_command_newline.py: **PASS**
    * 03_run_shell_command_multiline.py: **PASS**
    * 04_run_python_command_newline.py: **PASS**
    * 05_run_python_command_multiline.py: **PASS**

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


** testing on india.fg ** (AM)

* test 01:

The test run showed:

    (mypython_repo)[merzky@i136 job]$ python 01_run_remote_exe.py $P
    Job ID    : [pbs://localhost]-[None]
    Job State : saga.job.Job.New
    
    ...starting job...
    
    Job ID    : [pbs://localhost]-[389177.i136]
    Job State : saga.job.Job.Pending
    
    ...waiting for job...
    
    Job State : saga.job.Job.Done
    Exitcode  : 0

The exitcode seems to indicate success, and state as well - but the stdout file
is empty (just a newline).  qstat saya the job is done though:
queue:

    (mypython_repo)[merzky@i136 job]$ qstat
    Job id                    Name             User            Time Use S Queue
    ------------------------- ---------------- --------------- -------- - -----
    389177.i136                bliss_job        merzky          00:00:00 C batch

Debug shows:

    04/17/2012 08:05:23 AM - bliss.PBSJobAndSDPlugin(0x1a8b6248) - INFO - Generated PBS script:
    #!/bin/bash
    #PBS -N bliss_job
    #PBS -V
    #PBS -v MYOUTPUT="Hello from Bliss",
    #PBS -o bliss_job.01.stdout
    #PBS -e bliss_job.01.stderr
    
    /bin/echo $MYOUTPUT
    04/17/2012 08:05:23 AM - bliss.PBSJobAndSDPlugin(0x1a8b6248) - DEBUG - Got raw qstat output:
    04/17/2012 08:05:23 AM - bliss.PBSJobAndSDPlugin(0x1a8b6248) - DEBUG - Got raw qstat output: Job Id: 389184.i136


* test 02:
* test 03:

  Same result as for test 01


* test 04:
* test 05:

  Tests pass, and output contains the correct information


Note that Bliss should never report invalid job IDs, like
'[pbs://localhost]-[None]' -- the application ha no means to decide if this is
a valid ID or not (the native ID is opaque).  Bliss should in fact not report
any job ID before the correct and final ID is known.


Plug-In: PBS+SSH Job
----------------------

(AM)

ssh+pbs:// should be the same as pbs+ssh://

output/error files are not staged back

tests 1-3 have the same problems as the pbs tests above (not surprising).
tests 4,5 work.



Plug-In: SGE(+SSH) Job
----------------------
