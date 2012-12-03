# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from logging import DEBUG

import logging

def get_logger(): 
    """Return the Bliss logging handler.
    """
    l = logging.getLogger("bliss") 
    return l 

def log_to_file(filename, level=DEBUG): 
    """Send Bliss logs to a logfile.
    """ 
    l = logging.getLogger("bliss") 
    if len(l.handlers) > 0: 
        return 
    l.setLevel(level) 
    f = open(filename, 'w') 
    lh = logging.StreamHandler(f) 
    lh.setFormatter(logging.Formatter('%(levelname)-.3s [%(asctime)s.%(msecs)03d] thr=%(_threadid)-3d %(name)s: %(message)s', 
                                      '%Y%m%d-%H:%M:%S')) 
    l.addHandler(lh) 

