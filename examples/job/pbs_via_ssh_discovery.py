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
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga

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
        
        # set up the security contet:
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.usercert = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'

        sdd = saga.sd.Discoverer("pbs+ssh://xray.futuregrid.org")
        sdd.session.contexts.append(ctx)
        services = sdd.list_services()

        for service in services:
            print "Serivce name: '%s', type: '%s', url: '%s'" \
              % (service.name, service.type, service.url) 

        # create a job service for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        #js = saga.job.Service("pbs+ssh://louie.loni.org")

        

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

# INFO: The PBS script generated behind the scenes by the  
#       plugin looks like this (SAGA_VERBOSE=6 shows it):
#       
#         #!/bin/bash 
#         #PBS -N bliss_job 
#         #PBS -V     
#         #PBS -o bliss_pbssh_job.stdout 
#         #PBS -e bliss_pbssh_job.stderr 
#         #PBS -l walltime=0:05:00 
#         #PBS -v SLEEP_TIME=10, 
#       
#         /bin/sleep $SLEEP_TIME 

