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

  * URL: **pbs+ssh://alamo.futuregrid.org**, Info: FutureGrid Alamo Cluster, PBS 2.4.8, Date: 04/21/2012, 
    Git hash (git log -1): de149e866eae6b22be1ea2162742fec08f9927e3 
    * 01_run_remote_exe.py: **PASS**
    * 02_run_shell_command_newline.py: **PASS**
    * 03_run_shell_command_multiline.py: **PASS**
    * 04_run_python_command_newline.py: **PASS**
    * 05_run_python_command_multiline.py: **PASS**

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



Bliss ( ssh and pbs+ssh ) test results on QueenBee.
All jobs tested on queenbee from queenbee.

Job submitted from queen bee to queen bee.

(bliss-test)[pmantha@qb1 bliss]$ python test/compliance/job/01_run_remote_exe.py ssh://qb1.loni.org
Job ID    : [ssh://qb1.loni.org]-[None]
Job State : saga.job.Job.New

...starting job...

Job ID    : [ssh://qb1.loni.org]-[2907]
Job State : saga.job.Job.Running

...waiting for job...

Job State : saga.job.Job.Done
Exitcode  : 0

============================================
The job seems to have executed successfully!
============================================
                                            
NOW, SOME MANUAL CHECKING IS REQUIRED!      
                                            
(1) Login to ssh://qb1.loni.org                             
(2) Make sure the file bliss_job.stdout exists
(3) Make sure bliss_job.stdout contains the string 'Hello from Bliss'

If (1)-(3) are ok, this test can be considered as PASSED

(bliss-test)[pmantha@qb1 bliss]$ cat ~/bliss
bliss/            bliss_job.stderr  bliss_job.stdout  
(bliss-test)[pmantha@qb1 bliss]$ cat ~/bliss_job.stdout 

(bliss-test)[pmantha@qb1 bliss]$ cat ~/bliss_job.stderr 
(bliss-test)[pmantha@qb1 bliss]$ cd

--- No output is generated 

2nd test - failed.

(bliss-test)[pmantha@qb1 bliss]$ python test/compliance/job/02_run_shell_command_newline.py ssh://qb1.loni.org
Job ID    : [ssh://qb1.loni.org]-[None]
Job State : saga.job.Job.New

...starting job...

Job ID    : [ssh://qb1.loni.org]-[4981]
Job State : saga.job.Job.Running

...waiting for job...

Job State : saga.job.Job.Done
Exitcode  : 0

============================================
The job seems to have executed successfully!
============================================
                                            
NOW, SOME MANUAL CHECKING IS REQUIRED!      
                                            
(1) Login to ssh://qb1.loni.org                             
(2) Make sure the file bliss_job.stdout exists
(3) Make sure bliss_job.stdout contains:
  Hello from Bliss
  Hello from Bliss
  <The current date + time>

If (1)-(3) are ok, this test can be considered as PASSED

(bliss-test)[pmantha@qb1 bliss]$ cat ~/bliss_job.stdout 

--- No output is generated 


3rd test

(bliss-test)[pmantha@qb1 bliss]$ export SAGA_VERBOSE=5; python test/compliance/job/03_run_shell_command_multiline.py ssh://qb1.loni.org
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - BLISS runtime instance created at 0x2a9ae09c68
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.local supporting URL schmemas ['fork'] and API type(s) ['saga.job']
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.local internal sanity check passed
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.local as handler for URL schema fork://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.pbssh supporting URL schmemas ['pbs+ssh', 'pbs', 'torque', 'torque+ssh', 'xt5torque', 'xt5torque+ssh'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.pbssh internal sanity check passed
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs+ssh://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque+ssh://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque+ssh://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.sgessh supporting URL schmemas ['sge+ssh', 'sge'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.sgessh internal sanity check passed
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge+ssh://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.file.sftp supporting URL schmemas ['sftp'] and API type(s) ['saga.filesystem']
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.file.sftp internal sanity check passed
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.file.sftp as handler for URL schema sftp://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.ssh supporting URL schmemas ['ssh'] and API type(s) ['saga.job']
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.ssh internal sanity check passed
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.ssh as handler for URL schema ssh://
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Instantiated plugin 'saga.plugin.job.ssh' for URL scheme ssh:// and API type 'saga.job'
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Registered new service object <bliss.saga.job.Service.Service object at 0x2a9ae0d290>
04/16/2012 06:44:06 PM - bliss.Service(0x2a9ae0d290) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:06 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found an existing plugin instance for url scheme ssh://: <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:06 PM - bliss.Job(0x2a9ae0d3b0) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - service.create_job() called
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[None]
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.New

...starting job...

04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.run() called with ssh://qb1.loni.org
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Attempting to load SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Couldn't open SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - No hostname lookup for qb1.loni.org
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default ssh key
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default username
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Connecting to host qb1.loni.org
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - starting thread (client mode): 0x9ae0eed0L
04/16/2012 06:44:06 PM - bliss.paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_5.8p2-hpn13v11)
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - kex algos:['gss-gex-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group1-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group14-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'diffie-hellman-group-exchange-sha256', 'diffie-hellman-group-exchange-sha1', 'diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1'] server key:['ssh-rsa', 'ssh-dss'] client encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] server encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] client mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] server mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] client compress:['none', 'zlib@openssh.com'] server compress:['none', 'zlib@openssh.com'] client lang:[''] server lang:[''] kex follows?False
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - Ciphers agreed: local=aes128-ctr, remote=aes128-ctr
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - using kex diffie-hellman-group1-sha1; server key type ssh-rsa; cipher: local aes128-ctr, remote aes128-ctr; mac: local hmac-sha1, remote hmac-sha1; compression: local none, remote none
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - Switch to new keys ...
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7a9a9bac262427b7cf03004935fea648 in /home/pmantha/.ssh/id_rsa
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:44:06 PM - bliss.paramiko.transport - INFO - Authentication (publickey) failed.
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7033b17f74f888fdfdb1666a72159e51 in /home/pmantha/.ssh/id_dsa
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:44:06 PM - bliss.paramiko.transport - INFO - Authentication (publickey) successful!
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet in: 34816 bytes
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet out: 32768 bytes
04/16/2012 06:44:06 PM - bliss.paramiko.transport - INFO - Secsh channel 1 opened.
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - Sending command echo $$ && (env MYOUTPUT="Hello from Bliss"  /bin/sh -c '/bin/bash '-c' '"\necho $MYOUTPUT\necho $MYOUTPUT\ndate\n"'')> bliss_job.stdout 2> bliss_job.stderr to remote server:
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - [chan 1] Sesch channel 1 request ok
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Started process: /bin/bash ['-c', '"\necho $MYOUTPUT\necho $MYOUTPUT\ndate\n"']
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[21304]
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Running

...waiting for job...

04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.wait() called
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF received (1)
04/16/2012 06:44:06 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF sent (1)
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Failed
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_exitcode() called
Exitcode  : 127
04/16/2012 06:44:06 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called

============================================
The job seems to have FAILED!
============================================
                                            
Job returned in state 'Failed'.
Please run this test again with SAGA_VERBOSE=5 
and report the results at: 

https://github.com/saga-project/bliss/issues

(bliss-test)[pmantha@qb1 bliss]$ 
(bliss-test)[pmantha@qb1 ~]$ cat bliss_job.stderr 
necho: necho: command not found
(bliss-test)[pmantha@qb1 ~]$ 



4rth test:

(bliss-test)[pmantha@qb1 bliss]$ python test/compliance/job/04_run_python_command_newline.py ssh://qb1.loni.org
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - BLISS runtime instance created at 0x2a9ae09c68
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.local supporting URL schmemas ['fork'] and API type(s) ['saga.job']
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.local internal sanity check passed
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.local as handler for URL schema fork://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.pbssh supporting URL schmemas ['pbs+ssh', 'pbs', 'torque', 'torque+ssh', 'xt5torque', 'xt5torque+ssh'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.pbssh internal sanity check passed
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs+ssh://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque+ssh://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque+ssh://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.sgessh supporting URL schmemas ['sge+ssh', 'sge'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.sgessh internal sanity check passed
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge+ssh://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.file.sftp supporting URL schmemas ['sftp'] and API type(s) ['saga.filesystem']
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.file.sftp internal sanity check passed
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.file.sftp as handler for URL schema sftp://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.ssh supporting URL schmemas ['ssh'] and API type(s) ['saga.job']
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.ssh internal sanity check passed
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.ssh as handler for URL schema ssh://
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Instantiated plugin 'saga.plugin.job.ssh' for URL scheme ssh:// and API type 'saga.job'
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Registered new service object <bliss.saga.job.Service.Service object at 0x2a9ae0d290>
04/16/2012 06:44:56 PM - bliss.Service(0x2a9ae0d290) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:56 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found an existing plugin instance for url scheme ssh://: <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:56 PM - bliss.Job(0x2a9ae0d3b0) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - service.create_job() called
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[None]
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.New

...starting job...

04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.run() called with ssh://qb1.loni.org
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Attempting to load SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Couldn't open SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - No hostname lookup for qb1.loni.org
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default ssh key
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default username
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Connecting to host qb1.loni.org
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - starting thread (client mode): 0x9ae0ee90L
04/16/2012 06:44:56 PM - bliss.paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_5.8p2-hpn13v11)
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - kex algos:['gss-gex-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group1-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group14-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'diffie-hellman-group-exchange-sha256', 'diffie-hellman-group-exchange-sha1', 'diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1'] server key:['ssh-rsa', 'ssh-dss'] client encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] server encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] client mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] server mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] client compress:['none', 'zlib@openssh.com'] server compress:['none', 'zlib@openssh.com'] client lang:[''] server lang:[''] kex follows?False
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - Ciphers agreed: local=aes128-ctr, remote=aes128-ctr
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - using kex diffie-hellman-group1-sha1; server key type ssh-rsa; cipher: local aes128-ctr, remote aes128-ctr; mac: local hmac-sha1, remote hmac-sha1; compression: local none, remote none
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - Switch to new keys ...
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7a9a9bac262427b7cf03004935fea648 in /home/pmantha/.ssh/id_rsa
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:44:56 PM - bliss.paramiko.transport - INFO - Authentication (publickey) failed.
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7033b17f74f888fdfdb1666a72159e51 in /home/pmantha/.ssh/id_dsa
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:44:56 PM - bliss.paramiko.transport - INFO - Authentication (publickey) successful!
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet in: 34816 bytes
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet out: 32768 bytes
04/16/2012 06:44:56 PM - bliss.paramiko.transport - INFO - Secsh channel 1 opened.
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - Sending command echo $$ && (env MYOUTPUT="Hello from Bliss"  /bin/sh -c 'python '-c' '"import sys \nimport os \nprint os.environ[\'MYOUTPUT\'] \nprint sys.version"'')> bliss_job.stdout 2> bliss_job.stderr to remote server:
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - [chan 1] Sesch channel 1 request ok
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Started process: python ['-c', '"import sys \nimport os \nprint os.environ[\'MYOUTPUT\'] \nprint sys.version"']
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[21357]
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Running

...waiting for job...

04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.wait() called
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF received (1)
04/16/2012 06:44:56 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF sent (1)
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Failed
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_exitcode() called
Exitcode  : 1
04/16/2012 06:44:56 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called

============================================
The job seems to have FAILED!
============================================
                                            
Job returned in state 'Failed'.
Please run this test again with SAGA_VERBOSE=5 
and report the results at: 

https://github.com/saga-project/bliss/issues

Exception in thread Thread-1 (most likely raised during interpreter shutdown):(bliss-test)[pmantha@qb1 bliss]$ 

(bliss-test)[pmantha@qb1 ~]$ vi bliss_job.stderr 
  File "<string>", line 1
    import
         ^
SyntaxError: invalid syntax
~                                 




5th test

(bliss-test)[pmantha@qb1 bliss]$ python test/compliance/job/05_run_python_command_multiline.py ssh://qb1.loni.org
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - BLISS runtime instance created at 0x2a9ae09c68
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.local supporting URL schmemas ['fork'] and API type(s) ['saga.job']
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.local internal sanity check passed
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.local as handler for URL schema fork://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.pbssh supporting URL schmemas ['pbs+ssh', 'pbs', 'torque', 'torque+ssh', 'xt5torque', 'xt5torque+ssh'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.pbssh internal sanity check passed
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs+ssh://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema pbs://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema torque+ssh://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.pbssh as handler for URL schema xt5torque+ssh://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.sgessh supporting URL schmemas ['sge+ssh', 'sge'] and API type(s) ['saga.job', 'saga.sd']
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.sgessh internal sanity check passed
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge+ssh://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.sgessh as handler for URL schema sge://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.file.sftp supporting URL schmemas ['sftp'] and API type(s) ['saga.filesystem']
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.file.sftp internal sanity check passed
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.file.sftp as handler for URL schema sftp://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found plugin saga.plugin.job.ssh supporting URL schmemas ['ssh'] and API type(s) ['saga.job']
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Plugin saga.plugin.job.ssh internal sanity check passed
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Registered plugin saga.plugin.job.ssh as handler for URL schema ssh://
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Instantiated plugin 'saga.plugin.job.ssh' for URL scheme ssh:// and API type 'saga.job'
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Registered new service object <bliss.saga.job.Service.Service object at 0x2a9ae0d290>
04/16/2012 06:46:43 PM - bliss.Service(0x2a9ae0d290) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:46:43 PM - bliss.Runtime(0x2a9ae09c68) - INFO - Found an existing plugin instance for url scheme ssh://: <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:46:43 PM - bliss.Job(0x2a9ae0d3b0) - INFO - Bound to plugin <bliss.plugins.ssh.job.SSHJobPlugin instance at 0x2a9ae133b0>
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - service.create_job() called
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[None]
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.New

...starting job...

04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.run() called with ssh://qb1.loni.org
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Attempting to load SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Couldn't open SSH configuration file: /home/pmantha/.ssh/config
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - No hostname lookup for qb1.loni.org
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default ssh key
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Using default username
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Connecting to host qb1.loni.org
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - starting thread (client mode): 0x9ae0ee90L
04/16/2012 06:46:43 PM - bliss.paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_5.8p2-hpn13v11)
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - kex algos:['gss-gex-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group1-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'gss-group14-sha1-dZuIebMjgUqaxvbF7hDbAw==', 'diffie-hellman-group-exchange-sha256', 'diffie-hellman-group-exchange-sha1', 'diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1'] server key:['ssh-rsa', 'ssh-dss'] client encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] server encrypt:['aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'arcfour256', 'arcfour128', 'aes128-cbc', '3des-cbc', 'blowfish-cbc', 'cast128-cbc', 'aes192-cbc', 'aes256-cbc', 'arcfour', 'rijndael-cbc@lysator.liu.se'] client mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] server mac:['hmac-md5', 'hmac-sha1', 'umac-64@openssh.com', 'hmac-ripemd160', 'hmac-ripemd160@openssh.com', 'hmac-sha1-96', 'hmac-md5-96'] client compress:['none', 'zlib@openssh.com'] server compress:['none', 'zlib@openssh.com'] client lang:[''] server lang:[''] kex follows?False
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - Ciphers agreed: local=aes128-ctr, remote=aes128-ctr
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - using kex diffie-hellman-group1-sha1; server key type ssh-rsa; cipher: local aes128-ctr, remote aes128-ctr; mac: local hmac-sha1, remote hmac-sha1; compression: local none, remote none
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - Switch to new keys ...
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7a9a9bac262427b7cf03004935fea648 in /home/pmantha/.ssh/id_rsa
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:46:43 PM - bliss.paramiko.transport - INFO - Authentication (publickey) failed.
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - Trying discovered key 7033b17f74f888fdfdb1666a72159e51 in /home/pmantha/.ssh/id_dsa
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - userauth is OK
04/16/2012 06:46:43 PM - bliss.paramiko.transport - INFO - Authentication (publickey) successful!
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet in: 34816 bytes
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - [chan 1] Max packet out: 32768 bytes
04/16/2012 06:46:43 PM - bliss.paramiko.transport - INFO - Secsh channel 1 opened.
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - DEBUG - Sending command echo $$ && (env MYOUTPUT="Hello from Bliss"  /bin/sh -c 'python '-c' '"\nimport sys\nimport os  \nprint os.environ[\'MYOUTPUT\']\nprint sys.version\n"'')> bliss_job.stdout 2> bliss_job.stderr to remote server:
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - [chan 1] Sesch channel 1 request ok
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - Started process: python ['-c', '"\nimport sys\nimport os  \nprint os.environ[\'MYOUTPUT\']\nprint sys.version\n"']
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_job_id() called
Job ID    : [ssh://qb1.loni.org]-[23537]
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Running

...waiting for job...

04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.wait() called
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF received (1)
04/16/2012 06:46:43 PM - bliss.paramiko.transport - DEBUG - [chan 1] EOF sent (1)
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called
Job State : saga.job.Job.Failed
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_exitcode() called
Exitcode  : 1
04/16/2012 06:46:43 PM - bliss.SSHJobPlugin(0x2a9ae133b0) - INFO - job.get_state() called

============================================
The job seems to have FAILED!
============================================
                                            
Job returned in state 'Failed'.
Please run this test again with SAGA_VERBOSE=5 
and report the results at: 

https://github.com/saga-project/bliss/issues

(bliss-test)[pmantha@qb1 bliss]$ 


(bliss-test)[pmantha@qb1 ~]$ cat bliss_job.stderr 
Traceback (most recent call last):
  File "<string>", line 1, in ?
NameError: name 'nimport' is not defined
(bliss-test)[pmantha@qb1 ~]$ 
