#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to start a simple bigjob
   service that can be used as job submission endpoint
   via the bliss bigjob plug-in.

   Adopted from: http://bit.ly/ujW3XG 

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

import SocketServer
from bigjob.bigjob_manager import bigjob

def main():
    
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

