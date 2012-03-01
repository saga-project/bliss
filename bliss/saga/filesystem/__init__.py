#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package API.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.filesystem.file_api import File as SFile
class File(SFile):
    '''Loosely defines a SAGA File as defined in GFD.90.
    '''
    pass

from bliss.saga.filesystem.directory_api import Directory as SDirectory
class Directory(SDirectory):
    '''Loosely defines a SAGA Directory as defined in GFD.90.
    '''
    pass

