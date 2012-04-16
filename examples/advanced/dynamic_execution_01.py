#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a job to a PBS 
   jobmanager via ssh using a custom security context.

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga

def main():
    
    try:
        # list of resource that are potentially 
        # available 
        machines = {
          'xray'    : {'url':'pbs+ssh://xray.futuregrid.org',
                       'metrics':None, 'jobservice':None},
          'india'   : {'url':'pbs+ssh://india.futuregrid.org',
                       'metrics':None, 'jobservice':None},
          'alamo'   : {'url':'pbs+ssh://alamo.futuregrid.org',
                       'metrics':None, 'jobservice':None},
          'louie'   : {'url':'pbs+ssh://louie.loni.org',
                       'metrics':None, 'jobservice':None},
          'queenbee': {'url':'pbs+ssh://queenbee.loni.org',
                       'metrics':None, 'jobservice':None}
        }

        # create a bunch of jobs. at this point they are just 
        # descriptions and not bound to a resource manager
        jd = saga.job.Description()
        jd.wall_time_limit  = "0:05:00"
        jd.total_cpu_count = 1     
        jd.executable      = "/bin/sleep"
        jd.arguments       = ["10"] # 5 minutes

        jobs = []        
        for i in range(100):
            jobs.append({'jd':jd, 'jobj':None})

        # set up the security context:
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.userkey = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'

        # get some infos about the machines in our 
        # list, like number of waiting jobs, architecture, etc... 
        for key in machines:
            print "\nResource: %s" % (key)
            # create a discoverer and retrieve a list
            # of available serivces 
            sdd = saga.sd.Discoverer(machines[key]['url'])
            sdd.session.contexts.append(ctx)
            services = sdd.list_services() # filter: org.ogf.saga.service.job

            for service in services:
                # for each service, get some key metrics via the
                # service data object
                machines[key]['metrics'] = service.get_data()
                data = machines[key]['metrics'] 

                print "  * Serivce: '%s', type: '%s', url: '%s'" \
                  % (service.name, service.type, service.url)
                print "    |- Running Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateRunningJobs"))      
                print "    |- Pending Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateWaitingJobs"))    
                print "    |- Total CPUs           : %s" \
                  % (data.get_attribute("GlueSubClusterPhysicalCPUs"))      
                print "    |- Free CPUs            : %s" \
                  % (data.get_attribute("GlueCEStateFreeCPUs"))      
                print "    '- CPUs per Node        : %s" \
                  % (data.get_attribute("GlueHostArchitectureSMPSize"))      

            # create a job service for each machine.
            machines[key]['jobservice'] = \
                saga.job.Service(machines[key]['url'])
            print "  * Job service up and waiting for jobs..."

        # now that we have collected information about resources and 
        # instantiated job service endpoints, we can start to submit
        # jobs, following whatever strategy we want.
        for job in jobs:
            job['jobj'] = machines['india']['jobservice'].create_job(job['jd'])
            job['jobj'].run()

        for job in jobs:
            js = job['jobj'].get_state()
            ji = job['jobj'].get_job_id() 
            print "Job %s state: %s" % (ji, js)


             

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

