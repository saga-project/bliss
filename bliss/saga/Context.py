#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Attributes import AttributeInterface

class Context(AttributeInterface, object):
    '''Loosely defines a SAGA Context object as defined in GFD.90.

    A security context is a description of a security token.  It is important to
    understand that, in general, a context really just *describes* a token, but
    that a context *is not* a token (*). For example, a context may point to
    a X509 certificate -- but it will in general not hold the certificate
    contents.

    Context classes are used to inform the backends used by Bliss on what
    security tokens are expected to be used.  By default, Bliss will be able to
    pick up such tokens from their default location, but in some cases it might
    be necessary to explicitly point to them - then use a context instance to do
    so.

    The usage example for contexts is below::

        # define an ssh context
        c = saga.Context ()
        c['Type']     = 'ssh'
        c['UserCert'] = '$HOME/.ssh/special_id_rsa'
        c['UserKey']  = '$HOME/.ssh/special_id_rsa.pub'

        # add the context to a session
        s = saga.Session  ( )
        s.contexts.append (c)

        # create a job service in this session -- that job service can now
        # *only* use that ssh context. 
        j = saga.job.Service ('ssh://remote.host.net/', s)


    The 'session' argument to the job.Service constructor is fully optional --
    if left out, Bliss will use default session, which picks up some default
    contexts as described above -- that will suffice for the majority of use
    cases.

    ----

    (*) The only exception to this rule is the 'UserPass' key, which is used to
    hold plain-text passwords.  Use this key with care -- it is not good
    practice to hard-code passwords in the code base, or in config files.
    Also, be aware that the password may show up in log files, when debugging or
    analyzing your application.

    '''

    SSH      = "SSH"
    '''A security context type based on public/private keys.''' 
    EC2      = "EC2"
    '''A security context type for Eucalyptus / EC2 applications.'''

    #X509     = "X509"
    #'''A security context type based on X.509 certificates.'''
    #X509_SSH = "X509+SSH"
    #'''A security context type for X.509 via SSH.'''
    #BigJob = "BigJob"
    #'''A security context type for BigJob'''

    # FIXME: What is different between X509 and ssh+X509?
    # shouldn't the latter just a session with an ssh and an X509 context?  What
    # is this used for?
    # FIXME: What is a BigJob context??


    #__dict__ = {'_type', '_userkey', '_usercert', '_userproxy'}
  
    def __init__(self, type=None):
        '''Constructor'''
        self._type      = type
        self._userid    = None
        self._userpass  = None
        self._usercert  = None
        self._userkey   = None
        self._userproxy = None

        AttributeInterface.__init__(self)
      
        # register properties with the attribute interface 
        self._register_rw_attribute     (name="Type", 
                                         accessor=self.__class__.type) 
        self._register_rw_attribute     (name="UserID", 
                                         accessor=self.__class__.userid)  
        self._register_rw_attribute     (name="UserPass", 
                                         accessor=self.__class__.userpass)  
        self._register_rw_attribute     (name="UserCert", 
                                         accessor=self.__class__.usercert)  
        self._register_rw_attribute     (name="UserKey", 
                                         accessor=self.__class__.userkey)  
        self._register_rw_attribute     (name="UserProxy", 
                                         accessor=self.__class__.userproxy)  

    ######################################################################
    ##
    def __del__(self):
        '''Destructor.'''
        pass

    ######################################################################
    ##
    def __str__(self):
        '''String represenation.
        '''
        return "\n[\n Context Type: %s\n UserID: %s\n UserPass: %s\n UserCert: %s\n UserKey: %s\n UserProxy: %s\n]" % \
                (self.type, self.userid, self.userpass, self.usercert, self.userkey, self.userproxy)

    ######################################################################
    ## Property: type
    def type():
        doc = """Context type.
        
        This is a free-form string which describes the type of security token
        this context describes.  This type is not bound to a specific backend --
        for example, an 'SSH' context could be used by a number of backends,
        such as ssh (obviously), aws, gsissh, https, etc. (*)


        Example::


            # define an ssh context
            c = saga.Context ()
            c['Type']     = 'ssh'
            c['UserCert'] = '$HOME/.ssh/id_rsa'
            c['UserKey']  = '$HOME/.ssh/id_rsa.pub'

            # add it to a session
            s = saga.Session
            s.add_context (c)

            # create a job service in this session -- that job service can now
            # *only* use that ssh context. 
            j = saga.job.Service (s, 'ssh://remote.host.net/')


        (*) this is a list of transport protocols, not of backends, but
        hopefully make the point clear.

        """
        def fget(self):
            return self._type
        def fset(self, val):
            self._type = val
        return locals()
    type = property(**type())


    ######################################################################
    ## Property: userid
    def userid():
        doc = "User ID or user name to use."
        def fget(self):
            return self._userid
        def fset(self, val):
            self._userid = val
        return locals()
    userid = property(**userid())

    ######################################################################
    ## Property: userpass
    def userpass():
        doc = """User password to use.
        
        Please use this option with care -- it is *not* good practice to encode
        plain text passwords in source code!
        """
        def fget(self):
            return self._userpass
        def fset(self, val):
            self._userpass = val
        return locals()
    userpass = property(**userpass())

    ######################################################################
    ## Property: usercert
    def usercert():
        doc = "Location of a user certificate."
        def fget(self):
            return self._usercert
        def fset(self, val):
            self._usercert = val
        return locals()
    usercert = property(**usercert())

    ######################################################################
    ## Property: userkey
    def userkey():
        doc = "Location of a user key."
        def fget(self):
            return self._userkey
        def fset(self, val):
            self._userkey = val
        return locals()
    userkey = property(**userkey())

    ######################################################################
    ## Property: userproxy
    def userproxy():
        doc = "Location of a user proxy."
        def fget(self):
            return self._userproxy
        def fset(self, val):
            self._userproxy = val
        return locals()
    userproxy = property(**userproxy())

