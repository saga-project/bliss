#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This is a prototype for a BigJob service using XML-RPC
   over HTTP. It encapsulates the subjob API of BigJob and
   allows to submit jobs to BigJob from a different process
   or even from a remote machine. 

   The BigJob client is implemented as a Bliss plugin for 
   the job and sd APIs. Please check out the file 
   bigjob_simple.py for example usage.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import SimpleXMLRPCServer
#from bigjob.bigjob_manager import bigjob

class BigJobService(object):
    '''Encapsulates a BigJob Service'''
    def __init__(self):
        '''Constructor'''

    def bigjob_shutdown(self):
        '''Shut down this service'''

    def bigjob_status(self):
        '''Get the current status of the BigJob service'''

    def pilot_job_start(self):
        '''Start a pilot job'''

    def pilot_job_stop(self):
        '''Stop the currently running pilot job'''

    def pilot_job_state(self):
        '''Get the state of the currently running pilot job'''

    def subjob_add(self):
        '''Add a work unit'''

    def subjob_list(self):
        '''List all subjobs'''

    def subjob_state(self, subjob_id):
        '''Get the state of a subjob'''
    


def run_bigjob_service(hostname="localhost", port="8000"):
   
    try: 
        server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
        server.register_instance(BigJobService())
        server.serve_forever()
    except Exception, ex:
        print "BigJob Service terminated: %s" % str(ex)


 
    COORDINATION_URL    = "advert://advert.cct.lsu.edu:8080/"
    lrms_url            = "fork://localhost"
    workingdirectory    = os.path.join(os.getcwd(), "agent") 
    number_of_processes = 2
    queue               = None
    
    try:
        bj = bigjob(COORDINATION_URL) 

        bj.start_pilot_job(lrms_url, 
                           None, 
                           number_of_processes, 
                           queue, 
                           project, 
                           workingdirectory, 
                           None, 
                           walltime, 
                           processes_per_node) 
    
        print "Pilot Job/BigJob URL: " + bj.pilot_url + " State: " + str(bj.get_state())

        # listen to requests and 
        sj = subjob() 
        sj.submit_job(bj.pilot_url, jd) 

        # shutdown bigjob if it is still running
        if bj.get_state() == Running:
            bj.cancel() 

    except Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

