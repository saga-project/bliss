#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

class State:

    Unknown   =  0  '''wut?'''
    Pending   =  1  '''accepting workload, will eventually become active or fail.'''
    Active    =  2  '''Accepting workload, workload is executed.'''
    Draining  =  4  '''workload still executed, not accepting new work items.'''
    Running   =  Pending | Active | Draining 
    Destroyed =  8  '''Closed by user.'''
    Expired   = 16  '''Closed by system.'''
    Failed    = 32  '''Something went wrong.'''
    Final     = Destroyed | Expired | Failed 

