import copy
import time
import subprocess
import bliss.saga
import paramiko
import os 
class SSHJobProcess(object):
    '''A wrapper around a subprocess'''

#    __slots__ = {'prochandle', 'executable', 'arguments', 
#                 'environment', 'returncode', 'pid', 'state',
#                 't_created', 't_started', 't_finished'}

    def __init__(self, jobdescription,  plugin, service_object):
        self.executable  = jobdescription.executable
        self.arguments   = jobdescription.arguments
        self.environment = jobdescription.environment
        self.so = service_object
        self.sshclient = None
        self.sshchannel = None
        #self.service_obj=service_object
        self.pid = None
        self.returncode = None
        self.state = bliss.saga.job.Job.New
        self.pi = plugin
        self._job_output=None
        self._job_error=None

    def __del__(self):
        if self._job_output is not None:
            self._job_output.close()
        if self._job_error is not None:
            self._job_error.close()
        if self.sshchannel is not None:
            self.pi.log_debug("Closing SSH channel")   
            self.sshchannel.close()
        if self.sshclient is not None:
            self.pi.log_debug("Closing SSH client")
            self.sshclient.close()


    def run(self, jd, url):
#        if jd.output is not None:
#            self._job_output = open(jd.output,"w")  
#        else:
#            self._job_output = None 

#        if jd.error is not None:
#            self._job_error = open(jd.error,"w")  
#        else:
#            self._job_error = None 

        cmdline = str(self.executable)
        args = ""
        if self.arguments is not None:
            for arg in self.arguments:
                cmdline += " %s" % arg 

        self.pi.log_info("Trying to run: %s on host %s" % (cmdline, url.host))   

 
        self.config = paramiko.SSHConfig()
        #self.config.parse(open("$HOME/.ssh/config"))
        config_file = os.path.expanduser(os.path.join("~", ".ssh", "config"))

        self.pi.log_info("Loading SSH configuration file: %s" % config_file)
        self.config.parse(open(config_file))
        #self.sshconfig = self.config.lookup(host)

        usable_ctx = None

        for ctx in self.so.session.contexts:
            if ctx.type is bliss.saga.Context.SSH:
                usable_ctx = ctx
                self.pi.log_debug("Found SSH context to use!")
                break

    
        #username = pwd.getpwuid(os.getuid()).pw_name

        username = None
        userkey = None
        if usable_ctx is not None:
            if usable_ctx.userid is not None:
                username = usable_ctx.userid
            if usable_ctx.userkey is not None:
                userkey = usable_ctx.userkey

        self.sshclient=paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))    
          
        if not userkey:
            self.pi.log_debug("Using default ssh key")    
        else:
            self.pi.log_debug("Using context-provided ssh key")

        if not username:
            self.pi.log_debug("Using default username")
        else:
            self.pi.log_debug("Using context-provided username")

        hn = url.host
        try:
            temp = self.config.lookup(hn)['hostname']
            self.pi.log_info("Translating provided hostname %s to %s" % (hn, temp))
            hn = temp
        except Exception, ex:
            self.pi.log_info("No hostname lookup for %s" % hn)

        self.pi.log_info("Connecting to host %s" % hn)

        self.sshclient.connect(hn, username=username, key_filename=userkey)
        self.sshchannel = self.sshclient.get_transport().open_session()
        self.sshchannel.exec_command("("+cmdline+")" + "> "+ jd.output + " 2> " + jd.error)
        #self.stdin = self.sshchannel.makefile('wb', bufsize)
        bufsize=-1
        self._job_output = self.sshchannel.makefile('rb', bufsize)
        self._job_error = self.sshchannel.makefile_stderr('rb', bufsize)

        #self.pid = self.prochandle.pid
        self.pid = self.sshchannel.get_id()
        self.state = bliss.saga.job.Job.Running

    def getpid(self, serviceurl):
        return "[%s]-[%s]" % (serviceurl, self.pid)

    def getstate(self):
        #self._job_output.read()
        if self.state == bliss.saga.job.Job.Running:
            # only update if still running 
            if self.sshchannel.exit_status_ready():
                # are we all done?
                self.returncode = self.sshchannel.recv_exit_status()
                if self.returncode is not None:
                    if self.returncode != 0:
                        self.state = bliss.saga.job.Job.Failed
                    else:
                        self.state = bliss.saga.job.Job.Done
               
            #self.returncode = self.prochandle.poll() 
 
        return self.state

    def terminate(self):
        self.sshchannel.close()
        self.state = bliss.saga.job.Job.Canceled


    def wait(self, timeout):
        if timeout == -1:
            self.returncode = self.sshchannel.recv_exit_status()
            self.sshchannel.close()
        else:
            t_beginning = time.time()
            seconds_passed = 0
            while True:
                self.returncode = self.prochandle.poll()
                if self.returncode is not None:
                    break
                seconds_passed = time.time() - t_beginning
                if timeout and seconds_passed > timeout:
                    break
                time.sleep(0.1)

    def get_exitcode(self):
        return self.returncode

    
