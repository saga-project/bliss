#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit an Condor job .

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/saga-project/bliss/issues
'''

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import sys, time
import bliss.saga as saga

BASEPATH = "/home/oweidner/ExTENCI/condor/irods_bowtie/"

def main():
    
    try:
        # add extra Condor options as URL query parametersls /TG-MCB090174
        js = saga.job.Service("condor+ssh://gw68.quarry.iu.teragrid.org?WhenToTransferOutput=ON_EXIT&should_transfer_files=YES&notification=Always")

        # describe our job
        jd = saga.job.Description()

        # job executable
        jd.executable  = '%s/bowtie2-wrapper.sh' % BASEPATH

        # output options
        jd.output = "%s/irods_bowtie.stdout" % BASEPATH
        jd.error  = "%s/irods_bowtie.stdout" % BASEPATH

        # define allocation (Condor : +Project)
        jd.project = 'TG-MCB090174'
        #jd.candidate_hosts = ['UFlorida-SSERC', 'BNL_ATLAS_2', 'UFlorida-SSERC', 
        #  'BNL_ATLAS_2', 'FNAL_FERMIGRID', 'SPRACE', 'NYSGRID_CORNELL_NYS1', 
        #  'Purdue-Steele', 'MIT_CMS_CE2', 'UTA_SWT2', 'SWT2_CPB', 'AGLT2_CE_2', 
        #  'USCMS-FNAL-WC1-CE3']

        # pre-stage executables (Condor: transfer_input_files)
        jd.file_transfer = ['%s/bowtie2 > bowtie2' % BASEPATH, 
                            '%s/bowtie2-align > bowtie2-align' % BASEPATH]

        myjob = js.create_job(jd)

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...starting job...\n"
        myjob.run()

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...waiting for job...\n"
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.exitcode)

    except saga.Exception, ex:
        print "An error occured during job execution: %s" % (str(ex))
        sys.exit(-1)

if __name__ == "__main__":
    main()
