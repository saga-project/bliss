#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Context import Context

class Session(object):
    '''Loosely defines a SAGA Session object as defined in GFD.90.

    A SAGA-Python session has the purpose of scoping the use of security
    credentials for remote operations.  In other words, a session instance acts
    as a container for security :class:`bliss.saga.Context` instances --
    SAGA-Python objects (such as :class:`bliss.saga.job.Service` or
    :class:`bliss.saga.filesystem.File`) created in that session will then use
    exactly the security contexts from that session (and no others).

    That way, the session serves two purposes:  (1) it helps SAGA-Python to decide
    which security mechanism should be used for what interaction, and (2) it
    helps SAGA-Python to find security credentials which would be difficult to pick up
    automatically.
    
    The use of a session is as follows:


    Example::


        # define an ssh context
        c = saga.Context()
        c.context_type = 'ssh'
        c.user_cert = '$HOME/.ssh/special_id_rsa'
        c.user_key = '$HOME/.ssh/special_id_rsa.pub'

        # add it to a session
        s = saga.Session
        s.add_context(c)

        # create a job service in this session -- that job service can now
        # *only* use that ssh context. 
        j = saga.job.Service('ssh://remote.host.net/', s)


    The session argument to the :class:`bliss.saga.job.Service` constructor is fully optional --
    if left out, SAGA-Python will use default session, which picks up some default
    contexts as described above -- that will suffice for the majority of use
    cases.

    '''


    #__slots__ = {'_contexts'}

    ######################################################################
    ## 
    def __init__(self):
        '''Constructor.
        '''
        self._contexts = []
        '''Authentication / security contexts registered with the Session.'''

    ######################################################################
    ## 
    def __del__(self):
        '''Destructor.
        '''
        pass

    ######################################################################
    ## 
    def __str__(self):
        '''String represenation.
        '''
        return "Registered contexts: %s" % (str(self.contexts))

    ######################################################################
    ## Property: contexts
    def contexts():
        doc = """Authentication contexts registered with the Session.
        
        This property exposes the list of context instances managed by this
        session.  
        
        As the contexts and the session are stateless, it is safe to modify this
        list as needed.  Any object created in a session will maintain a copy of
        the then-valid context list, and will not be affected by later updates
        to the session.
        """

        def fget(self):
            return self._contexts
        def fset(self, val):
            self._contexts = val
        #def fdel(self, val):
        #    self._contexts.remove(val)
        return locals()
    contexts = property(**contexts())

    ######################################################################
    ## 
    def add_context(self, context):
        '''add a security :class:`bliss.saga.Context` to the session.

           It is encouraged to use the :class:`bliss.saga.Session.contexts` property instead. 
        '''
        self._contexts.append(context)

    ######################################################################
    ## 
    def remove_context(self, context):
        '''remove a security :class:`bliss.saga.Context` from the session.

           It is encouraged to use the :class:`bliss.saga.Session.contexts` property instead.
        '''
        self._contexts.remove(context)

    ######################################################################
    ## 
    def list_contexts(self):
        '''retrieve all :class:`bliss.saga.Context` objects attached to the session.


           It is encouraged to use the :class:`bliss.saga.Session.contexts` property instead.
        '''
        return self._contexts

