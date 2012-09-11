# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import copy
import time
import bliss.saga
import os 
#from furl import furl 
import boto

class EucaCompute(object):
    '''A wrapper around a VM'''
    def __init__(self, plugin, manager_obj, url):
        self.pi = plugin
        self.mo = manager_obj
        self.url = url
        #print "url:", url
        #print "url.username:", url.username
        #print "url.password:", url.password
        #print "url.host:", url.host
        #print "url.path:", url.path
        #print "url.fragment:", url.fragment

        # TODO: Validate if the line below actually works!
        self.image = self.url.path # furl(self.url.__str__()).path.segments[-1]
        self.reservation = None

        # NOTE AM: if UserPass information are not in the URL, they need to 
        # be inferred from session/context, or environment.
        self.access_key = self.url.username
        self.private_key = self.url.password
        self.host = self.url.host

        self.pi.log_info("Euca adaptor attempting to connect to:")
        self.pi.log_info("Server: " + str(self.host))
        self.pi.log_info("Access key: " + str(self.access_key) )
        self.pi.log_info("Private key: " + str(self.private_key) )
        self.pi.log_info("SSH authentication keypair: NOT DEFINED")
        self.pi.log_info("Image: " + self.image)

        #context info:
        #userid = property(** userid()) = access key id
        #userpass = property(** userpass()) = secret access key
        #usercert = property(** usercert()) = 
        #userkey = property(** userkey()) = ssh id to use / key_name for image

        
        # NOTE AM: what does 'is_secure=False' mean?  Related to the code
        # commented out above?
        self.connection = boto.connect_euca(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.private_key,
            #                              is_secure=False,
            host=self.host,
            #         region=region,                                                                         
            port=8773
            #path="/services/Eucalyptus"                               
            )

        sgs = self.connection.get_all_security_groups()
                 
        if not 'BLISS' in [i.name for i in sgs]:
            self.pi.log_info("Creating BLISS security group")
            sg = connection.create_security_group('BLISS', 'Security group for BLISS SAGA')
            sg = connection.authorize_security_group_deprecated(sg.name, None, None, 'tcp','22' ,'22' ,'0.0.0.0/0')
        else:
            self.pi.log_info("BLISS security group already created, leaving it as-is")

    def create_instance(self):
        self.pi.log_info("Creating an instance")
        remote_image=self.connection.get_image(self.image)    
        self.reservation=remote_image.run(key_name="userkey", instance_type="m1.xlarge")
        
        return self.reservation.instances[0]
        

    def __del__(self):
        pass


    def run(self, jd, url):
        pass

    def getpid(self, serviceurl):
        return 1

    def get_state(self):
        if not self.reservation:
            return bliss.saga.resource.state.State.Unknown

        for i in self.reservation.instances:
            i.update()

        if self.reservation.instances[0].state=="pending":
            return bliss.saga.resource.state.State.Pending
        if self.reservation.instances[0].state=="running":
            return bliss.saga.resource.state.State.Active
        else:
            return bliss.saga.resource.state.State.Unknown

    def get_description(self):
        cd = bliss.saga.resource.compute_description_api.ComputeDescription()
        # print cd.list_attributes()
        cd.set_attribute("hostnames", ["192.168.1.1"])
        
        return cd

    def terminate(self):
       for i in self.reservation.instances:
            i.terminate()

    def wait(self, timeout):
        pass

    def get_exitcode(self):
        pass
