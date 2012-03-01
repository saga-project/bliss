#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

class Type:

    Unknown   =  0  '''wut?'''
    Compute   =  1  '''accepting compute jobs'''
    Storage   =  2  '''stores data'''
    Network   =  3  '''connects resources'''
    Pool      =  4  '''combines resources'''

