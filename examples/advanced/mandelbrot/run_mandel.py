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
from mandelbrot import makemandel

# the dimension (in pixel) of the whole fractal
imgx = 2048 
imgy = 2048

# the number of tiles in X and Y direction to split-up
# the fractal into. 
tilesx = 4
tilesy = 4

################################################################################
##
if __name__ == "__main__":

    # the total time to calculate all tiles:
    t_total = 0.0

    # the 'master' image that we assemble from the individual tiles.
    # WARNING: for large images, this will consume a substantial amount
    #          of memory!
    fullimage = Image.new("RGB", (imgx, imgy))

    try:
        for x in range(0, tilesx):
            for y in range(0, tilesy):
                print "Creating Mandelbrot tile [X:%s Y:%s]" % (x+1, y+1)
                # this is where we call the Mandelbrot fractal generator
                # directly via its module function makemandel().
                t0 = time.time() 
                partimage = makemandel(imgx, imgy, (imgx/tilesx*x), (imgx/tilesx*(x+1)), 
                                                   (imgy/tilesy*y), (imgy/tilesy*(y+1)))
                dt = time.time() - t0
                t_total += dt
                print "...took %s seconds." % dt
            
                fullimage.paste(partimage, (imgx/tilesx*x, imgy/tilesy*y, imgx/tilesx*(x+1), imgy/tilesy*(y+1)) )

        print "Total execution time to generate a %sx%s Mandelbrot fractal: %s" % (imgx, imgy, t_total)
        print "Saving master image as 'mandel_full.png (this might take a while)'..."
        fullimage.save("mandel_full.png", "PNG")
        sys.exit(0)

    except KeyboardInterrupt:
	# Ctrl-C caught. Try to save what we already have and exit. 
	print "Total execution time until Ctrl-C was hit: %s" % (t_total) 
        print "Saving partial master image as 'mandel_full.png' (this might take a while)..."
        fullimage.save("mandel_full.png", "PNG") 
        sys.exit(-1)
