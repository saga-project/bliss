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

Plug-In: PBS(+SSH) Job
----------------------


Plug-In: SGE(+SSH) Job
----------------------
