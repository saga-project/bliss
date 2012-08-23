# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import logging
import os.path

from bliss.saga.object import Object 

from bliss.saga.attributes import AttributeInterface
from bliss.saga.exception import Exception as SAGAException
from bliss.saga.error import Error as SAGAError

class Context(Object, AttributeInterface):
    '''Loosely defines a SAGA Context object as defined in GFD.90.

    A security context is a description of a security token.  It is important to
    understand that, in general, a context really just *describes* a token, but
    that a context *is not* a token (*). For example, a context may point to
    a X509 certificate -- but it will in general not hold the certificate
    contents.

    Context classes are used to inform the backends used by Bliss on what
    security tokens are expected to be used.  By default, Bliss will be able to
    pick up such tokens from their default location, but in some cases it might
    be necessary to explicitly point to them - then use a L{Session} with
    context instances to do so.

    The usage example for contexts is below::

        # define an ssh context
        c = saga.Context()
        c.context_type = 'ssh'
        c.user_cert = '$HOME/.ssh/special_id_rsa'
        c.user_key = '$HOME/.ssh/special_id_rsa.pub'

        # add the context to a session
        s = saga.Session()
        s.contexts.append(c)

        # create a job service in this session -- that job service can now
        # *only* use that ssh context. 
        j = saga.job.Service('ssh://remote.host.net/', s)


    The L{Session} argument to the L{job.Service} constructor is fully optional
    -- if left out, Bliss will use default session, which picks up some default
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
    X509     = "X509"
    '''A security context type based on X.509 certificates.'''
    


    ######################################################################
    ## 
    def __init__(self):
        '''Constructor'''

        Object.__init__(self, objtype=Object.ObjectType.Context,
                        apitype=Object.ObjectType.BaseAPI)

        self.__logger = logging.getLogger('bliss.'+self.__class__.__name__)

        self.attributes_extensible_  (True)
        self.attributes_camelcasing_ (True)
      
        # register properties with the attribute interface 
        self.attributes_register_ ('ContextType', None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('UserID',      None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('UserPass',    None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('UserCert',    None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('UserKey',     None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('UserProxy',   None, self.String, self.Scalar, self.Writable)

        self.attributes_register_deprecated_  ('userid'     , 'UserID'     )
        self.attributes_register_deprecated_  ('userpass'   , 'UserPass'   )
        self.attributes_register_deprecated_  ('usercert'   , 'UserCert'   )
        self.attributes_register_deprecated_  ('userkey'    , 'UserKey'    )
        self.attributes_register_deprecated_  ('userproxy'  , 'UserProxy'  )


        ##########################################
        # some attributes point to files which must exist - so we add a test for
        # those attributes
        #
        def test_file_existence_ (key, val) :
            if not val :
                return "File %s = '' doesn't exist."  %  (key)
            if not os.path.isfile (val) :
                return "File %s = '%s' doesn't exist."  %  (key, val)
            return True
        ##########################################

        self.attributes_check_add_ ('UserKey',   test_file_existence_)
        self.attributes_check_add_ ('UserCert',  test_file_existence_)
        self.attributes_check_add_ ('UserProxy', test_file_existence_)


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
                (self.context_type, self.user_id, self.user_pass, self.user_cert, self.user_key, self.user_proxy)

    ######################################################################
    ## Property: type
        """Context type.
        
        This is a free-form string which describes the type of security token
        this context describes.  This type is not bound to a specific backend --
        for example, an 'SSH' context could be used by a number of backends,
        such as ssh (obviously), aws, gsissh, https, etc. (*)


        Example::


            # define an ssh context
            c = saga.Context()
            c.context_type = 'ssh'
            c.user_cert = '$HOME/.ssh/id_rsa'
            c.user_key = '$HOME/.ssh/id_rsa.pub'

            # add it to a session
            s = saga.Session
            s.add_context(c)

            # create a job service in this session -- that job service can now
            # *only* use that ssh context. 
            j = saga.job.Service(s, 'ssh://remote.host.net/')


        (*) this is a list of transport protocols, not of backends, but
        hopefully make the point clear.

        """


    ######################################################################
    ## Property: user_id
        """
        UserID

        User ID or user name to use.
        """

    ######################################################################
    ## Property: user_pass
        """User password to use.
        
        Please use this option with care -- it is *not* good practice to encode
        plain text passwords in source code!
        """

    ######################################################################
    ## Property: user_cert
        """Location of a user certificate."""

    ######################################################################
    ## Property: user_key
        """Location of a user key."""

    ######################################################################
    ## Property: user_proxy
        """Location of a user proxy."""

