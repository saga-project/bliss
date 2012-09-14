# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import traceback
import StringIO

def _get_exception_traceback():
    '''returns the last traceback as a string with a given prefix'''
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    if fp.getvalue() == "None\n":
        return "(No Traceback)"
    else:
        return fp.getvalue() 


class Exception(Exception):
    """ The Exception class encapsulates information about error conditions
        encountered in SAGA/Bliss.

        Additionally to the error message (e.message), the exception also provides
        a trace to the code location where the error condition got raised
        (e.traceback), and an error code (e.error) which identifies the type of
        error encountered.
 
        **Example**::

          try :
              file = saga.filesystem.File("sftp://alamo.futuregrid.org/tmp/data1.dat")

          except saga.Exception, e :
              if e.error == saga.Error.Timeout:
                  # maybe the network is down?
                  print "connection timed out"
              else:
                  # something else went wrong
                  print "Exception occurred: %s %s" % (str(e), e.traceback)

        """

    ######################################################################
    ##
    def __init__(self, error, message):
        """Create a new Exception object.

           :param error:   The type of error
           :type  error:   :class:`bliss.saga.Error`
           :param message: The error message
           :type  message: str
        """
        self._error = error
        self._message = message
        self._traceback = _get_exception_traceback()

    ######################################################################
    ##
    def __str__(self):
        """String representation (utf-8)."""
        return unicode(self).decode('utf-8', 'ignore')

    ######################################################################
    ##
    def __unicode__(self):
        """Unicode representation."""
        ucstring = u'SAGA Exception (%s): %s' % (unicode(self.error), unicode(self.message))
        return ucstring

    ######################################################################
    ##
    @property
    def message(self):
        """The Exception's error message."""
        return self._message

    ######################################################################
    ##
    @property
    def error(self):
        """The Exception's :class:`bliss.saga.Error` type."""
        return self._error

    ######################################################################
    ##
    @property
    def traceback(self):
        """The Exception's stack trace (if available)."""
        return self._traceback
