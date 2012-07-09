#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

""" 
This example script runs the Mandelbrot fractal generator sequentially.

In this example, we run the Mandelbrot generator for a 2048x2048 pixel
Mandelbrot fractal. We split it up in 4x4 tiles which we run sequentially, one
after another on the local machine, simply by calling the 'makemandel()'
function directly.

Try to change the values for the dimension (imgx, imgy) and the number of
tiles (tilesx, tilesy). You will see that the bigger the image is, the longer
it will take to compute. Changing the number of tiles doesn't change the total
compute time for the whole set, because compute time per tile will increase
with more tiles and decrease with fewer tiles.

   A 2048x2048 Mandelbrot fractal takes about one minute to generate on a
   3.0GHz CPU. A 32768x32768 fractal takes more than two hours to finish!

Different tiles seem to need different amounts of time to generate. 
Do you know why?  
"""

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import sys, time, Image
import logging
import bliss.utils
import bliss.saga as saga
from mandelbrot import makemandel

# the dimension (in pixel) of the whole fractal
imgx = 2048 
imgy = 2048

# the number of tiles in X and Y direction to split-up
# the fractal into. 
tilesx = 1
tilesy = 1

################################################################################
##
if __name__ == "__main__":

    try:
        jobs = []
 
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
 
        # the saga job services connects to and provides a handle
        # to a remote machine. In this case. it's a PBS cluster:    
        jobservice = saga.job.Service("pbs+ssh://oweidner@india.futuregrid.org")
        jobservice.session.contexts.append(ctx)


        for x in range(0, tilesx):
            for y in range(0, tilesy):
                # the saga job description is used to describe the parameters 
                # and requirements of a compute job. Here, we describe how we
                # want to run the Mandelbrot generator:
                outputfile = 'tile_x%s_y%s.png' % (x,y)
                jd = saga.job.Description()
                jd.wall_time_limit   = 5
                jd.total_cpu_count   = 1     
                jd.executable        = 'python'
                jd.arguments         = ['mandelbrot.py', imgx, imgy, 
                                        (imgx/tilesx*x), (imgx/tilesx*(x+1)),
                                        (imgy/tilesy*y), (imgy/tilesy*(y+1)),
                                        outputfile]

                job = jobservice.create_job(jd)
                job.run()
                jobs.append(job)

                print " * Submitted 'tile-job' with ID %s. Output will be written to: %s" % (job.jobid, outputfile)

        while len(jobs) > 0:
            for job in jobs:
                jobstate = job.get_state()
                print " * Job %s status: %s" % (job.jobid, jobstate)
                if jobstate is saga.job.Job.Done:
                    jobs.remove(job)
                
            time.sleep(5)

        #print "Saving master image as 'mandel_full.png (this might take a while)'..."
        #fullimage.save("mandel_full.png", "PNG")
        sys.exit(0)

    except saga.Exception, ex:
        print ex
        sys.exit(-1)

    except KeyboardInterrupt:
	# Ctrl-C caught. Try to save what we already have and exit. 
        #print "Saving partial master image as 'mandel_full.png' (this might take a while)..."
        #fullimage.save("mandel_full.png", "PNG")
        for job in jobs:
            job.cancel()
        sys.exit(-1)
