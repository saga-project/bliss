#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to query a number of PBS 
   clusters for status information. 
    
   The information can e.g., be used to make advanced 
   scheduling decissions on application level. 
   Look in the examples/advanced direcory for inspiration.  

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.sagacompat as saga

def main():
    
    try:
        # list of resource that are potentially 
        # available 
        machines = {
          'xray'    : 'pbs+ssh://xray.futuregrid.org',
          'india'   : 'pbs+ssh://india.futuregrid.org',
          'alamo'   : 'pbs+ssh://alamo.futuregrid.org',
          'louie'   : 'pbs+ssh://louie.loni.org',
          'queenbee': 'pbs+ssh://queenbee.loni.org'
        }

        # set up the security context:
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.context()
        ctx.type = saga.context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.userkey = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'

        # get some infos about the resources in our 
        # list, like number of waiting jobs, architecture, etc... 
        for machine in machines:
            print "\nResource: %s" % (machine)
            # create a discoverer and retrieve a list
            # of available serivces 
            sdd = saga.sd.discoverer(machines[machine])
            sdd.session.contexts.append(ctx)
            services = sdd.list_services() # filter: org.ogf.saga.service.job

            for service in services:
                # for each service, get some key metrics via the
                # service data object
                data = service.get_data()

                print "  * Serivce: '%s', type: '%s', url: '%s'" \
                  % (service.name, service.type, service.url)
                print "    |- Running Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateRunningJobs"))      
                print "    |- Waiting Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateWaitingJobs"))   
                print "    |- Memory per Node      : %.2f GB" \
                  % (float(data.get_attribute("GlueHostMainMemoryRAMSize"))/1048576.0)     
                print "    |- Total CPUs           : %s" \
                  % (data.get_attribute("GlueSubClusterPhysicalCPUs"))      
                print "    |- Free CPUs            : %s" \
                  % (data.get_attribute("GlueCEStateFreeCPUs"))      
                print "    '- CPUs per Node        : %s" \
                  % (data.get_attribute("GlueHostArchitectureSMPSize"))      

    except saga.exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

