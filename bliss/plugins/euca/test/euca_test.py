# test script to connect to india's EC2

#!/usr/bin/env python
import bliss 
import bliss.saga as saga
import time
import os
def main():
    try:

        #connect to a resource manager with the eucalyptus plugin
        # substitute your info here
        rsc = saga.resource.Manager("euca://YOUR_ACCESS_KEY:YOUR_SECRET_KEY@149.165.146.135/YOUR_MACHINE_IMAGE_HERE")
        
        #set up context information
        ctx = saga.Context()
        ctx.type = saga.Context.X509
        ctx2 = saga.Context()
        ctx2.type = saga.Context.SSH
        
        rsc.session.contexts.append(ctx)
        rsc.session.contexts.append(ctx2)

        ctx2.userid  = 'root' 
        # substitute your info here
        ctx2.userkey = '/N/u/USER/userkey.pem'

        #create compute resource
        print "Creating compute resource"
        cd= saga.resource.ComputeDescription()
        c= rsc.create_compute(cd)

        #wait for the compute resource to be available
        print "Waiting for host", c.get_state_detail()
        while (c.get_state() !=bliss.saga.resource.State.Active) :            
            time.sleep(1)
        print

        #list all compute resources
        print "Printing list_compute_resources()"
        time.sleep(1)
        c=None
        for i in  rsc.list_compute_resources():
            print rsc.get_compute(i).get_state_detail()
            if rsc.get_compute(i).get_state()==bliss.saga.resource.State.Active:
                c=rsc.get_compute(i)

        print "Using this compute resource:"
        print c.get_state_detail()

        url = "ssh://root@" + "%s" % c.instance.public_dns_name
        ip = "%s" % c.instance.public_dns_name

        #create a job service with the ip of the virtual machine
        js = saga.job.Service(bliss.saga.Url(url))
        js.session.contexts.append(ctx2)

        ######################################################
        # COPY BOOTSTRAP SCRIPT OVER AND CACTUS
        ######################################################

        print "Copying bootstrap script and Cactus simulation files"
        
        os.system("scp -i userkey.pem ~/bootstrap.sh root@"+ip+":~/")
        os.system("scp -i userkey.pem ~/Cactus.tar root@"+ip+":/mnt")

        # environment, executable & arguments
        jd = saga.job.Description()
        jd.executable  = 'bash'
        jd.arguments   = ['~/bootstrap.sh']

        # output options
        jd.output = "bliss_cactus_job.stdout"
        jd.error  = "bliss_cactus_job.stderr"

        # create the job (state: New)
        myjob = js.create_job(jd)

        print "Running SSH job"
        myjob.run()

        print "Waiting for the job to complete"
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.exitcode)               

        #####################################################
        # COPY RESULTS BACK
        #####################################################

        print "Copying results back"
        os.system("scp -i userkey.pem root@"+ip+":~/*cactus* .")
        
        print "Terminating compute device"
        c.destroy()

        exit(0)

    except Exception, e:
        print "Test failed!",e
         
if __name__ == "__main__":
    main()
