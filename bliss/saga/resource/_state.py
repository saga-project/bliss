#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

class State:

    Pending = 1
    '''Will eventually become active or fail.'''
    Active  = 2
    '''Accepting jobs.'''
    Closed  = 3
    '''Closed by user.'''
    Expired = 4
    '''Closed by system.'''
    Failed  = 5
    '''Something went wrong.'''
