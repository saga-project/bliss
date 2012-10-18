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

import sys, time, os
import bliss.saga as saga
from PIL import Image

# the dimension (in pixel) of the whole fractal
imgx = 2048 
imgy = 2048

# the number of tiles in X and Y direction
tilesx = 2
tilesy = 2

################################################################################
##
if __name__ == "__main__":

    try:
        # list that holds the jobs
        jobs = []

        # create a working directory in /scratch
        dirname = 'sftp://localhost/%s/mbrot/' % os.getenv('SCRATCH')
        workdir = saga.filesystem.Directory(dirname, saga.filesystem.Create)

        # copy the executable into our working directory
        mbexe = saga.filesystem.File('sftp://localhost/tmp/mandelbrot.py')
        mbexe.copy(workdir.get_url())

        # the saga job services connects to and provides a handle
        # to a remote machine. In this case. it's a PBS cluster:    
        jobservice = saga.job.Service('fork://localhost')

        for x in range(0, tilesx):
            for y in range(0, tilesy):

                # describe a single Mandelbrot job. we're using the 
                # directory created above as the job's working directory
                outputfile = 'tile_x%s_y%s.png' % (x,y)
                jd = saga.job.Description()
                jd.wall_time_limit   = 5
                jd.total_cpu_count   = 1    
                jd.working_directory = workdir.get_url().path
                jd.executable        = 'python'
                jd.arguments         = ['mandelbrot.py', imgx, imgy, 
                                        (imgx/tilesx*x), (imgx/tilesx*(x+1)),
                                        (imgy/tilesy*y), (imgy/tilesy*(y+1)),
                                        outputfile]
                # create the job from the description
                # above, launch it and add it to the list of jobs
                job = jobservice.create_job(jd)
                job.run()
                jobs.append(job)
                print ' * Submitted %s. Output will be written to: %s' % (job.jobid, outputfile)

        # wait for all jobs to finish
        while len(jobs) > 0:
            for job in jobs:
                jobstate = job.get_state()
                print ' * Job %s status: %s' % (job.jobid, jobstate)
                if jobstate is saga.job.Job.Done:
                    jobs.remove(job)
            time.sleep(5)

        # copy image tiles back to our 'local' directory
        for image in workdir.list('*.png'):
            print ' * Copying %s/%s back to %s' % (workdir.get_url(), image, os.getcwd())
            workdir.copy(image, 'sftp://localhost/%s/' % os.getcwd()) 

        # stitch together the final image
        fullimage = Image.new('RGB',(imgx, imgy),(255,255,255))
        for x in range(0, tilesx):
            for y in range(0, tilesy):
                partimage = Image.open('tile_x%s_y%s.png' % (x, y))
                fullimage.paste(partimage, (imgx/tilesx*x, imgy/tilesy*y, imgx/tilesx*(x+1), imgy/tilesy*(y+1)) )
        fullimage.save("mandelbrot_full.png", "PNG")
        
        sys.exit(0)

    except saga.Exception, ex:
        print 'Problem during execution: %s' % ex
        sys.exit(-1)

    except KeyboardInterrupt:
	# ctrl-c caught: try to cancel our jobs before we exit
        # the program, otherwise we'll end up with lingering jobs.
        for job in jobs:
            job.cancel()
        sys.exit(-1)
