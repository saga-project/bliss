# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import traceback
import StringIO

def plugin_traceback(prefix="\n*** "):
    '''returns the last traceback as a string with a given prefix'''
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    if fp.getvalue() == "None\n":
        return "(No Traceback)"
    else:
        return prefix+fp.getvalue() 
