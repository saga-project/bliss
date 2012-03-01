#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package (compatibility) API.
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.filesystem._file_api import File as SFile
class file(SFile):
    '''Loosely defines a SAGA File as defined in GFD.90.
    '''
    pass

from bliss.saga.filesystem._directory_api import Directory as SDirectory
class directory(SDirectory):
    '''Loosely defines a SAGA Directory as defined in GFD.90.
    '''
    pass

