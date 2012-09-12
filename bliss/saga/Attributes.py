# -*- coding: utf-8 -*-

__author__    = "Andre Merzky"
__copyright__ = "Copyright 2011-2012, Andre Merzky"
__license__   = "MIT"

from bliss.saga.Exception import Exception as Exception
from bliss.saga.Error     import Error     as Error


################################################################################

import datetime
import traceback
import inspect
import re

# FIXME: add a tagging 'Monitorable' interface, which enables callbacks.

################################################################################
#
# Callback (Abstract) Class
#
class Callback () :
    """
    Callback base class.

    All objects using the Attribute Interface allow to register a callback for
    any changes of its attributes, such as 'state' and 'state_detail'.  Those
    callbacks can be python call'ables, or derivates of this callback base
    class.  Instances which inherit this base class MUST implement (overload)
    the cb() method.

    The callable, or the callback's cb() method is what is invoked whenever the
    TROY implementation is notified of an change on the monitored object's
    attribute.

    The cb instance receives three parameters upon invocation:

      - obj: the watched object instance
      - key: the watched attribute (e.g. 'state' or 'state_detail')
      - val: the new value of the watched attribute

    If the callback returns 'True', it will remain registered after invocation,
    to monitor the attribute for the next subsequent state change.  On returning
    'False' (or nothing), the callback will not be called again.

    To register a callback on a object instance, use::

      class MyCallback (troy.Callback) :

        def __init__ (self, msg) :
          self.msg_ = msg

        def cb (self, obj, key, val) :
          print " %s\\n %s (%s) : %s"  %  self._msg, obj, member, value

        def main () :

          cpd = troy.compute_pilot_description ()
          cpf = troy.compute_pilot_framework ()
          cp  = cpf.submit_pilot (cpd)

          mcb = MyCallback ("Hello Pilot, how is your state?")

          cp.add_callback ('state', mcb)

    See documentation of the L{Attributes} interface for further details and
    examples.
    """

    def __init__ (self) :
        """ The callback constructor simply raises an IncorrectState exception,
            to signal that the application needs to inherit the callback class
            in a custom class in order to use notifications.
        """
        raise Exception ("Callback class must be inherited before use!", 
                         Error.IncorrectState)


    def cb (self, wu, key, val) :
        """ This is the method that needs to be implemented by the application

            Keyword arguments::

                obj:  the watched object instance
                key:  the watched attribute
                val:  the new value of the watched attribute

            Return::

                keep:   bool, signals to keep (True) or remove (False) the callback
                        after invocation

            Callback invocation MAY (and in general will) happen in a separate
            thread -- so the application need to make sure that the callback
            code is thread-safe.

            The boolean return value is used to signal if the callback should
            continue to listen for events (return True) , or if it rather should
            get unregistered after this invocation (return False).
        """
        pass



################################################################################
#
#
#
class _AttributesBase (object) :
    """ 
    This class only exists to host properties -- as object itself does *not* have
    properties!  This class is not part of the public attribute API.
    """
    def __init__ (self) :
        pass


class AttributeInterface (_AttributesBase) :
    """
    Attribute Interface Class

    The Attributes interface implements the attribute semantics of the SAGA Core
    API specification (http://ogf.org/documents/GFD.90.pdf).  Additionally, this
    implementation provides that semantics via two different interfaces: the
    python dictionary interface, and the python property interface.  Note that
    a *simgle* set of attributes is internally managed, no matter what interface
    is used for access.

    A class which uses this interface can internally specify which attributes
    can be set, and what type they have.  Also, default values can be specified,
    and the class provides a rudimentary support for converting scalar
    attributes into vector attributes and back.

    Also, the consumer of this API can register callbacks, which get triggered
    on changes to specific attribute values.

    Example use case::


        ###########################################
        class Transliterator ( pilot.Attributes ) :
            
            def __init__ (self, *args, **kwargs) :
                # setting attribs to non-extensible will cause the cal to init below to
                # complain if attributes are specified.  Default is extensible.
              # self._attributes_extensible (False)
        
                # pass args to base class init (requires 'extensible')
                super (Transliterator, self).__init__ (*args, **kwargs)
        
                # setup class attribs
                self._attributes_register   ('apple', 'Appel', self.Url,    self.Scalar, self.Writable)
                self._attributes_register   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)
        
                # setting attribs to non-extensible at *this* point will have allowed
                # custom user attribs on __init__ time (via args), but will then forbid
                # any additional custom attributes.
              # self._attributes_extensible (False)
        
        
        ###########################################
        if __name__ == "__main__":
        
            # define a callback method.  This callback can get registered for
            # attribute changes later.
        
            #################################
            def cb (obj, key, val) :
                # the callback gets information about what attribute was changed
                # on what object:
                print "called: %s - %s - %s"  %  (type (obj), key, str(val))

                # returning True will keep the callback registered for further
                # attribute changes.
                return True
            #################################
        
            # create a class instance and add a 'cherry' attribute/value on
            # creation.  
            trans = Transliterator (cherry='Kersche')
        
            # use the property and the dict interface to mess with the pre-defined
            # 'apple' attribute
            print "\\n -- apple"
            print trans.apple 
            print trans['apple']
            trans.apple = 'Abbel'
            print trans.apple 
        
            # add our callback to the apple attribute, and trigger some changes.
            # Note that the callback is also triggered when the attribute's
            # value changes w/o user control, e.g. by some internal state
            # changes.
            trans.add_callback ('apple', cb)
            trans.apple = ['Abbel', 'Appel']
            trans.apple = 'Apfel'
        
            # Setting an attribute final is actually an internal method, used by
            # the implementation to signal that no further changes on that
            # attribute are expected.  We use that here for demonstrating the
            # concept though.  Callback is invoked on set_final().
            trans._attributes_set_final ('apple')
            trans.apple = 'Abbel'
            print trans.apple 
        
            # mess around with the 'plum' attribute, which was marked as
            # ReadOnly on registration time.
            print "\\n -- plum"
            print trans.plum
          # trans.plum    = 'Pflaume'  # raises readonly exception
          # trans['plum'] = 'Pflaume'  # raises readonly exception
            print trans.plum
        
            # check if the 'cherry' attribute exists, which got created on
            # instantiation time.
            print "\\n -- cherry"
            print trans.cherry
        
            # as we have 'extensible' set, we can add a attribute on the fly,
            # via either the property or the dict interface, or via the GFD.90
            # API of course.
            print "\\n -- peach"
            trans['peach'] = 'Berne'
            print trans.peach
            trans.peach = 'Birne'
            print trans.peach


    This example will result in::

        -- apple
        Appel
        Appel
        Abbel
        called: apple - Abbel Appel  - <class '__main__.Transliterator'>
        called: apple - Apfel - <class '__main__.Transliterator'>
        called: apple - Apfel - <class '__main__.Transliterator'>
        Apfel
        
        -- plum
        Pruim
        Pruim
        
        -- cherry
        Kersche
        
        -- peach
        Berne
        Birne



    Note that using this interface *and* inheriting from Python's dict object
    (or any other base classes which define / overload dictionary setters and
    getters) is probably a bad idea.
    """

    ############################################################################
    #
    # define a couple of constants for the attribute API, mostly for registering
    # attributes.
    #
    # type enums
    Any         = 'any'        # any python type can be set
    Url         = 'url'        # URL type (string + URL parser checks)
    Int         = 'int'        # Integer type
    Float       = 'float'      # float type
    String      = 'string'     # string, duh!
    Bool        = 'bool'       # True or False or Maybe
    Enum        = 'enum'       # value is any one of a list of candidates
    Time        = 'time'       # seconds since epoch, or any py time thing
                               # which can be converted into such
                               # FIXME: conversion not implemented

    # mode enums
    Writable    = 'writable'   # the consumer of the interface can change
                               # the attrib value
    ReadOnly    = 'readonly'   # the consumer of the interface can not
                               # change the attrib value.  The
                               # implementation can still change it.
    Final       = 'final'      # neither consumer nor implementation can
                               # change the value anymore
    Alias       = 'alias'      # variable is deprecated, and alias'ed to
                               # a different variable.

    # extensible enum
    Extended    = True         # new attributes can be added on the fly
    NotExtended = False        # setting new attributes will raise an exception

    # flavor enums
    Scalar      = 'scalar'     # the attribute value is a single data element
    Vector      = 'vector'     # the attribute value is a list of data elements

    # two regexes for converting CamelCase into under_score_casing, as static
    # class vars to avoid frequent recompilation
    _camel_case_regex_1 = re.compile('(.)([A-Z][a-z]+)')
    _camel_case_regex_2 = re.compile('([a-z0-9])([A-Z])')


    ############################################################################
    #
    #
    #
    def __init__ (self, *args, **kwargs) :
        """
        This method is not supposed to be directly called by the consumer of
        this API -- it should be called via derived object construction.

        _attributes_t_init makes sure that the basic structures are in place on
        the attribute dictionary - this saves us ton of safety checks later on.
        """

        # initialize state
        d = self._attributes_t_init ()

        # call to update and the args/kwargs handling seems to be part of the
        # dict interface conventions *shrug*
        self.update (*args, **kwargs)


    ############################################################################
    #
    # Internal interface tools.
    #
    # These tools are only for internal use, and should never be called from 
    # outside of this module.
    #
    # Naming: _attributes_t_*
    #
    ####################################
    def _attributes_t_init (self, key=None) :
        """
        This internal function is not to be used by the consumer of this API.

        The _attributes_t_init method initializes the interface's internal data
        structures.  We always need the attribute dict, and the extensible flag.
        Everything else can be added on the fly.  The method will not overwrite
        any settings -- initialization occurs only once!

        If a key is given, the existence of this key is checked.  An exception
        is raised if the key does not exist.

        The internal data are stored as property on the _AttributesBase class.
        Storing them as property on *this* class would obviously result in
        recursion...
        """

        d = {}

        try :
            d = _AttributesBase.__getattribute__ (self, '_d')
        except :
            # need to initialize -- any exceptions in the code below should fall through
            d['attributes']  = {}
            d['extensible']  = True
            d['camelcasing'] = False
            d['setter']      = None
            d['getter']      = None
            d['lister']       = None
            d['recursion']    = False

            _AttributesBase.__setattr__ (self, '_d', d)


        # check if we know about the given attribute
        if key :
            if not key in d['attributes'] :
                raise Exception ("attribute key is invalid: %s"  %  (key),
                                 Error.DoesNotExist)

        # all is well
        return d


    ####################################
    def _attributes_t_keycheck (self, key) :
        """
        This internal function is not to be used by the consumer of this API.

        For the given key, check if the key name is valid, and/or if it is
        aliased.  
        
        If the does not yet exist, the validity check is performed, and allows
        to limit dynamically added attribute names (for 'extensible' sets).
        
        if the key does exist, the alias check triggers a deprecation warning,
        and returns the aliased key for transparent operation.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # perform name validity checks if key is new
        if not key in d['attributes'] :
            # FIXME: we actually don't have any tests, yet.  We should allow to
            # configure such via, say, _attributes_add_check (callable (key))
            pass


        # if key is known, check for aliasing
        else: 
            # check if we know about the given attribute
            if d['attributes'][key]['mode'] == self.Alias :
                alias = d['attributes'][key]['alias']
                print "attribute key / property name '%s' is deprecated - use '%s'"  %  (key, alias)
                key   = alias

        return key


    ####################################
    def _attributes_t_call_cb (self, key, val) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the invocation of all callbacks for a given attribute.
        Callbacks returning False (or nothing at all) will be unregistered after
        their invocation.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        # avoid recursion
        if d['attributes'][key]['recursion'] :
            return

        callbacks = d['attributes'][key]['callbacks']

        # iterate over a copy of the callback list, so that remove does not
        # screw up the iteration
        for cb in list (callbacks) :

            call = cb

            # support both plain callables, but also Callback derivates
            if inspect.isclass (cb) and \
               issubclass (cb, Callback) :
                # for those too lazy to parse this beautiful line below:
                # if the registered cb is an instance of our Callback class, we
                # call that class' cb method.  So, the callable (cb) is the
                # member 'cb' of the registered class (cb)
                call = cb.cb

            # got the callable - call it!
            # raise and lower recursion shield as needed
            ret = False
            try :
                d['attributes'][key]['recursion'] = True
                ret = call (self, key, val)
            finally :
                d['attributes'][key]['recursion'] = False

            # remove callbacks which return 'False', or raised and exception
            if not ret :
                callbacks.remove (cb)


    ####################################
    def _attributes_t_call_setter (self, key) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the setter callbacks, to signal that the attribute value
        has just been set and should be propagated as needed.
        """

        # make sure interface is ready to use.
        d = self._attributes_t_init (key)

        # avoid recursion
        if d['attributes'][key]['recursion'] :
            return

        try :
            # always raise and lower the recursion shield
            d['attributes'][key]['recursion'] = True
        
            setter_all = d['setter']
            setter_key = d['attributes'][key]['setter']

            if setter_all : setter_all (self, key)
            if setter_key : setter_key (self, key)

        finally :
            d['attributes'][key]['recursion'] = False


    ####################################
    def _attributes_t_call_getter (self, key) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the getter callbacks, to signal that the attribute value
        is about to be accesses and should be updated as needed.
        """

        # make sure interface is ready to use.
        d = self._attributes_t_init (key)

        # avoid recursion
        if d['attributes'][key]['recursion'] :
            return

        try :
            # always raise and lower the recursion shield
            d['attributes'][key]['recursion'] = True
        
            getter_all = d['getter']
            getter_key = d['attributes'][key]['getter']

            if getter_all : getter_all (self, key)
            if getter_key : getter_key (self, key)

        finally :
            d['attributes'][key]['recursion'] = False


    ####################################
    def _attributes_t_call_lister (self) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the lister callback, to signal that the attribute list
        is about to be accesses and should be updated as needed.
        """

        # make sure interface is ready to use.
        d = self._attributes_t_init ()

        # avoid recursion
        if d['recursion'] :
            return

            # always raise and lower the recursion shield
            try :
                d['attributes'][key]['recursion'] = True
                lister = d['lister']
                if lister : lister (self)

            finally :
                d['attributes'][key]['recursion'] = False



    ####################################
    def _attributes_t_underscore (self, key) :
        """ 
        This internal function is not to be used by the consumer of this API.

        The method accepts a CamelCased word, and translates that into
        'under_score' notation -- IFF 'camelcasing' is set

        Kudos: http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # _camel_case_regex_1 = re.compile('(.)([A-Z][a-z]+)')
        # _camel_case_regex_2 = re.compile('([a-z0-9])([A-Z])')

        if d['camelcasing'] :
            temp = AttributeInterface._camel_case_regex_1.sub(r'\1_\2', key)
            return AttributeInterface._camel_case_regex_2.sub(r'\1_\2', temp).lower()
        else :
            return key



    ####################################
    def _attributes_t_conversion (self, key, val) :
        """
        This internal function is not to be used by the consumer of this API.

        The method checks a given attribute value against the attribute's
        flags, and performs some simple type conversion as needed.  Also, the
        method will restore a 'None' value to the attribute's default value.

        A deriving class can add additional value checks for attributes by
        calling L{_attributes_add_check} (key, check).
        """

        # make sure interface is ready to use.  We do not check for keys, that
        # needs to be done in the calling method.  For example, on 'set', type
        # conversions will be performed, but the key will not exist previously.
        d = self._attributes_t_init ()

        # if the key is not known
        if not key in d['attributes'] :
            # cannot handle unknown attributes.  Attributes which have been
            # registered earlier will be fine, as they have type information.
            return val

        # check if a value is given.  If not, revert to the default value
        # (if available)
        if val == None :
            if 'default' in d['attributes'][key] :
                val = d['attributes'][key]['default']


        # perform flavor and type conversion
        val = self._attributes_t_conversion_flavor (key, val)

        # apply all value checks on the conversion result
        for check in d['attributes'][key]['checks'] :
            ret = check (key, val)
            if ret != True :
                raise Exception ("attribute value %s is not valid: %s"  %  (key, ret),
                                 Error.BadParameter)

        # aaaand done
        return val


    ####################################
    def _attributes_t_conversion_flavor (self, key, val) :
        """ 
        This internal function is not to be used by the consumer of this API.
        This method should ONLY be called by _attributes_t_conversion! 
        """
        # FIXME: there are possibly nicer and more reversible ways to
        #        convert the flavors...

        # easiest conversion of them all... ;-)
        if val == None :
            return None

        # make sure interface is ready to use.
        d = self._attributes_t_init (key)

        # check if we need to serialize a list into a scalar
        f = d['attributes'][key]['flavor']
        if f == self.Vector :
            # we want a vector
            if isinstance (val, list) :
                # val is already vec - apply type conversion on all elems
                ret = []
                for elem in val :
                    ret.append (self._attributes_t_conversion_type (key, elem))
                return ret
            else :
                # need to create vec from scalar
                if isinstance (val, basestring) :
                    # for string values, we split on white spaces and type-convert 
                    # all elements
                    vec = val.split ()
                    ret = []
                    for element in vec :
                        ret.append (self._attributes_t_conversion_type (key, element))
                    return ret
                else :   
                    # all non-string types are interpreted as only element of
                    # a single-member list
                    return [self._attributes_t_conversion_type (key, val)]


        elif f == self.Scalar :
            # we want a scalar
            if isinstance (val, list) :
                # need to create scalar from vec
                if len (val) > 1 :
                    # if the list has more than one element, we use an intermediate
                    # string representation of the list before converting to a scalar
                    # This is the weakest conversion mode, and will not very
                    # likely yield useful results.
                    tmp = ""
                    for i in val :
                        tmp += str(i) + " "
                    return self._attributes_t_conversion_type (key, tmp)
                elif len (val) == 1 :
                    # for single element lists, we simply use the one element as
                    # scalar value 
                    return self._attributes_t_conversion_type (key, val[0])
                else :
                    # no value in list
                    return None
            else :
                # scalar is already scalar, just do type conversion
                return self._attributes_t_conversion_type (key, val)


        # we should never get here...
        raise Exception ("Cannot evaluate attribute flavor (%s) : %s"  %  (key, str(f)),
                         Error.NoSuccess)


    ####################################
    def _attributes_t_conversion_type (self, key, val) :
        """ 
        This internal function is not to be used by the consumer of this API.
        This method should ONLY be called by _attributes_t_conversion!
        """

        # make sure interface is ready to use.
        d = self._attributes_t_init (key)

        # oh python, how about a decent switch statement???
        t   = d['attributes'][key]['type']
        ret = None
        try :
            # FIXME: add time/date conversion to/from string
            if   t == self.Any    : return        val  
            elif t == self.Int    : return int   (val) 
            elif t == self.Float  : return float (val) 
            elif t == self.Bool   : return bool  (val) 
            elif t == self.String : return str   (val) 
            else                  : return        val  
        except ValueError as e:
            raise Exception ("attribute value %s has incorrect type: %s" %  (key, val),
                             Error.BadParameter)

        # we should never get here...
        raise Exception ("Cannot evaluate attribute type (%s) : %s"  %  (key, str(t)),
                         Error.NoSuccess)

    ####################################
    def _attributes_t_wildcard2regex (self, pattern) :
        """ 
        This internal function is not to be used by the consumer of this API.

        This method converts a string containing POSIX shell wildcards into
        a regular expression with the same matching properties::

            *       -> .*
            ?       -> .
            {a,b,c} -> (a|b|c)
            [abc]   -> [abc]   
            [!abc]  -> [^abc]   
        """

        re = pattern

        re.replace ('*', '.*')  # set of characters
        re.replace ('?', '.' )  # single character

        # character classes
        match = re.find ('[', 0)
        while match >= 0 :
            if  re[first + 1] == '!' :
                re[first + 1] =  '^'
            match = re.find ('[', match + 1)

        # find opening { and closing }
        first = re.find ('{', 0)
        last  = re.find ('}', first + 1)

        # while match
        while first >= 0 and last  >= 0 :
            # replace with ()
            re[first] = '('
            re[last] = '('

            # also, replace all ',' with with '|' for alternatives
            comma = re.find (',', first)
            while comma >= 0 :
                re[comma] = '|'
                comma = re.find (',', comma + 1)

            # done - find next bracket pair...
            first = re.find ('{', last + 1)
            last  = re.find ('}', first + 1)


    ###########################################################################
    #
    # internal interface
    #
    # This internal interface is used by the public interfaces (dict,
    # properties, GFD.90).  We assume that CamelCasing and under_scoring is
    # sorted out before this internal interface is called.  All other tests,
    # verifications, and conversion are done here though.
    #
    # Naming: _attributes_i_*
    #
    ####################################
    def _attributes_i_set (self, key, val=None, force=False) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        See L{set_attribute} (key, val) for details.

        New value checks can be added dynamically, and per attribute, by calling
        L{_attributes_add_check} (key, callable).

        Some internal methods can set the 'force' flag, and will be able to set
        attributes even in ReadOnly mode.  That is, for example, used for getter
        hooks.  Note that the Final flag will be honored even if Force is set,
        and will result in the set request being ignored.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # if the key is not known
        if not key in d['attributes'] :
            if not d['extensible'] :
                # we cannot add new keys on non-extensible sets
                raise Exception ("attribute set is not extensible (key %s)" %  key,
                                 Error.IncorrectState)
            else :
                # if the set is extensible, we can register the new key.  It
                # won't have any callbacks at this point.
                self._attributes_register (key, None, self.Any, self.Scalar, self.Writable, self.Extended)

        # known attribute - attempt to set its value
        else:

            # check if we are allowed to change the attribute - complain if not.
            # Also, simply ignore write attempts to finalized keys.
            if 'mode' in  d['attributes'][key] :

                mode = d['attributes'][key]['mode']
                if self.Final == mode :
                    return
                elif self.ReadOnly == mode :
                    if not force :
                        raise Exception ("attribute %s is not writable" %  key, 
                                         Error.BadParameter)


        # permissions are confirmed, set the attribute with conversion etc.

        # apply any attribute conversion
        val = self._attributes_t_conversion (key, val)

        # make sure the key's value entry exists
        if not 'value' in d['attributes'][key] :
            d['attributes'][key]['value'] = None

        # only once an attribute is explicitly set, it 'exists' for the purpose
        # of the 'attribute_exists' call, and the key iteration
        d['attributes'][key]['exists'] = True

        # only actually change the attribute when the new value differs --
        # and only then invoke any callbacks and hooked setters
        if val != d['attributes'][key]['value'] :
            d['attributes'][key]['value'] = val
            self._attributes_t_call_setter (key)
            self._attributes_t_call_cb (key, val)


    ####################################
    def _attributes_i_get (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{get_attribute} (key) for details.

        Note that this method is not performing any checks or conversions --
        those are all performed when *setting* an attribute.  So, any attribute
        flags (type, mode, flavor) are evaluated on setting, not on getting.
        This implementation does not account for resulting race conditions
        (changing attribute types after setting for example) -- but the public
        API does not allow that anyway.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        self._attributes_t_call_getter (key)

        if 'value' in d['attributes'][key] :
            return d['attributes'][key]['value']

        if 'default' in d['attributes'][key] :
            return d['attributes'][key]['default']
                
        return None



    ####################################
    def _attributes_i_list (self, ext=True) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{list_attributes} () for details.

        Note that registration alone does not qualify for listing.  If 'ext' is
        True (default),extended attributes are listed, too.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # call list hooks
        self._attributes_t_call_lister ()

        ret = []

        for key in sorted(d['attributes'].iterkeys()) :
            if d['attributes'][key]['mode'] != self.Alias :
                if d['attributes'][key]['exists'] :
                    if ext or not d['attributes'][key]['extended'] :
                        ret.append (key)

        return ret


    ####################################
    def _attributes_i_find (self, pattern) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{find_attributes} (pattern) for details.
        """

        # FIXME: wildcard-to-regex

        # make sure interface is ready to use
        d = self._attributes_t_init ()


        # separate key and value pattern
        p_key  = ""    # string pattern
        p_val  = ""    # string pattern
        pc_key = None  # compiled pattern
        pc_val = None  # compiled pattern


        if pattern[0] == '=' :
            # no key pattern present, only grep on values
              p_val = self._attributes_t_wildcard2regex (pattern[1:])
        else :
          p = re.compile (r'[^\]=')
          tmp = p.split (pattern, 2)  # only split on first '='
          
          if len (tmp) >  0 : 
              # at least one elem: only key pattern present
              p_key = self._attributes_t_wildcard2regex (tmp[0])  
          
          if len (tmp) == 2 :
              # two elems: val pattern is also present
              p_val = self._attributes_t_wildcard2regex (tmp[1])

        # compile the found pattern
        if len (p_key) : pc_key = re.compile (p_key)
        if len (p_val) : pc_val = re.compile (p_val)

        # now dig out matching keys. List hooks are triggered in
        # _attributes_i_list().
        matches = []
        for key in self._attributes_i_list () :
            val = str(self._attributes_i_get (key))

            if ( (pc_key == None) or pc_key.search (key) ) and \
               ( (pc_val == None) or pc_val.search (val) )     :
                matches.append (key)

        return matches


    ####################################
    def _attributes_i_exists (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{attribute_exists} (key) for details.

        Registered keys which have never been explicitly set to a value do not
        exist for the purpose of this call.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # check if we know about that attribute
        if 'exists' in d['attributes'][key] :
            if  d['attributes'][key]['exists'] :
                return True

        return False


    ####################################
    def _attributes_i_is_extended (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        This method will check if the given key is extended, i.e. was registered
        on the fly, vs. registered explicitly.

        This method is not used by, and not exposed via the public API, yet.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        return d['attributes'][key]['extended']


    ####################################
    def _attributes_i_is_readonly (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{attribute_is_readonly} (key) for details.

        This method will check if the given key is readonly, i.e. cannot be
        'set'.  The call will also return 'True' if the attribute is final
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        # check if we know about that attribute
        if  d['attributes'][key]['mode'] == self.Final or \
            d['attributes'][key]['mode'] == self.ReadOnly :
            return True

        return False


    ####################################
    def _attributes_i_is_writable (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{attribute_is_writable} (key) for details.

        This method will check if the given key is writable - i.e. not readonly.
        """

        return not self._attributes_i_is_readonly (key)


    ####################################
    def _attributes_i_is_removable (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{attribute_is_removable} (key) for details.

        'True' if the attrib is Writable and Extended.
        """

        if self._attributes_i_is_writable (key) and \
           self._attributes_i_is_extended (key)     :
            return True

        return False

    ####################################
    def _attributes_i_is_vector (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{attribute_is_vector} (key) for details.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        # check if we know about that attribute
        if  d['attributes'][key]['flavor'] == self.Vector :
            return True

        return False


    ####################################
    def _attributes_i_is_final (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        This method will query the 'final' flag for an attribute, which signals
        that the attribute will never change again.

        This method is not used by, and not exposed via the public API, yet.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        if self.Final == d['attributes'][key]['mode'] :
             return True

        # no final flag found -- assume non-finality!
        return False


    ####################################
    def _attributes_i_add_cb (self, key, cb) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{add_callback} (key, cb) for details.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        d['attributes'][key]['callbacks'].append (cb)
        return len (d['attributes'][key]['callbacks']) - 1


    ####################################
    def _attributes_i_del_cb (self, key, id=None) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is indirectly used via the different public interfaces.

        see L{remove_callback} (key, cb) for details.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init (key)

        # id == None: remove all callbacks
        if not id :
            d['attributes'][key]['callbacks'] = []
        else :
            if len (d['attributes'][key]['callbacks']) < id :
                raise Exception ("invalid callback cookie for attribute %s"  %  key,
                                 Error.BadParameter)
            else :
                d['attributes'][key]['callbacks'][id] = undef



    ############################################################################
    #
    # This part of the interface is primarily for use in deriving classes, which
    # thus provide the Attributes interface.
    #
    # Keys should be provided as CamelCase (only relevant if camelcasing is
    # set).
    #
    # Naming: _attributes_*
    #
    ####################################
    def _attributes_register (self, key, default=None, typ=Any, flavor=Scalar, mode=Writable, ext=False) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Register a new attribute.

        This function ignores extensible, final and readonly flags.  It can also
        be used to re-register an existing attribute with new properties -- the
        old attribute value, callbacks etc. will be lost though.  Using this
        call that way may result in confusing behaviour on the public API level.
        """
        # FIXME: check for valid mode and flavor settings

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        # we expect keys to be registered as CamelCase (in those cases where
        # that matters).  But we store attributes in 'under_score' version.
        us_key = self._attributes_t_underscore (key)

        # remove any old instance of this attribute
        if us_key in  d['attributes'] :
            self._attributes_unregister (us_key)

        # register the attribute and properties
        d['attributes'][us_key]                 = {}
        d['attributes'][us_key]['value']        = default # initial value
        d['attributes'][us_key]['default']      = default # default value
        d['attributes'][us_key]['type']         = typ     # int, float, enum, ...
        d['attributes'][us_key]['exists']       = False   # no value set, yet
        d['attributes'][us_key]['flavor']       = flavor  # scalar / vector
        d['attributes'][us_key]['mode']         = mode    # readonly / writable / final
        d['attributes'][us_key]['extended']     = ext     # True if added on the fly
        d['attributes'][us_key]['camelcase']    = key     # keep original key name
        d['attributes'][us_key]['underscore']   = us_key  # keep under_scored name
        d['attributes'][us_key]['enums']        = []      # list of valid enum values
        d['attributes'][us_key]['checks']       = []      # list of custom value checks
        d['attributes'][us_key]['callbacks']    = []      # list of callbacks
        d['attributes'][us_key]['recursion']    = False   # recursion check for callbacks
        d['attributes'][us_key]['setter']       = None    # custom attribute setter
        d['attributes'][us_key]['getter']       = None    # custom attribute getter

        # for enum types, we add a value checker
        if typ == self.Enum :
            ######################################
            def _enum_check (key, val) :
                if None == val  :
                    # None is always allowed
                    return True
                
                us_key = self._attributes_t_underscore (key)
                d      = self._attributes_t_init (us_key)
                vals   = d['attributes'][us_key]['enums']

                # check if there is anything to check
                if not vals :
                    return True
                
                # value must be one of allowed enums
                if val in vals :
                        return True

                # Houston, we got a problem...
                return """
                incorrect value (%s) for Enum typed attribute (%s).
                Allowed values: %s
                """  %  (str(val), key, str(vals))
            ######################################

            self._attributes_add_check (key, _enum_check)



    ####################################
    def _attributes_register_deprecated (self, key, alias) :
        """
        Often enough, there is the need to use change attribute names.  It is
        good practice to not simply rename attributes, and thus effectively
        remove old ones, as that is likely to break existing code.  Instead, new
        names are added, and old names are kept for a certain time for backward
        compatibility.  To support migration to the new names, the old names
        should be marked as 'deprecated' though - which can be configured to
        print a warning whenever an old, deprecated attribute is used.

        This method allows to register such deprecated attribute names.  They
        can thus be used just like new ones, and in fact are implemented as
        aliases to the new ones -- but they will print a deprecated warning on
        usage.

        The first parameter is the old name of the attribute, the second
        parameter is the aliased new name.  Note that the new name needs to be
        registered before (via L{_attributes_register})::

            # old code:
            self._attributes_register ('apple', 'Appel', self.String, self.Scalar, self.Writable)

            # new code
            self._attributes_register ('fruit', 'Appel', self.String, self.Scalar, self.Writable)
            self._attributes_register_deprecated ('apple', 'fruit)

        In some cases, you may want to deprecate a variable and not replace it
        with a new one.  In order to keep this interface simple, this can be
        achieved via::

            # new code
            self._attributes_register ('deprecated_apple', 'Appel', self.String, self.Scalar, self.Writable)
            self._attributes_register_deprecated ('apple', 'deprecated_apple)

        This way, the user will either see a warning, or has to explicitly use
        'deprecated_apple' as attribute name -- which should be warning enough,
        at least for the programmer ;o)
        """

        # we expect keys to be registered as CamelCase (in those cases where
        # that matters).  But we store attributes in 'under_score' version.
        us_alias = self._attributes_t_underscore (alias)
        us_key   = self._attributes_t_underscore (key)

        # make sure interface is ready to use
        # This check will throw if 'alias' was not registered before.
        d = self._attributes_t_init (us_alias)

        # remove any old instance of this attribute
        if us_key in  d['attributes'] :
            self._attributes_unregister (us_key)

        # register the attribute and properties
        d['attributes'][us_key]               = {}
        d['attributes'][us_key]['mode']       = self.Alias # alias
        d['attributes'][us_key]['alias']      = us_alias   # aliased var
        d['attributes'][us_key]['camelcase']  = key        # keep original key name
        d['attributes'][us_key]['underscore'] = us_key     # keep under_scored name

    
    ####################################
    # @deprecated
    def _register_rw_vec_attribute (self, name, accessor) :
        """
        This deprecated alias for _attributes_register makes bigjob happy
        """

        key     = name
        default = None
        syms    = {}

        if type (accessor) == type (property()) :
            syms['fdoc'] = accessor.__doc__
            syms['fset'] = accessor.fget
            syms['fget'] = accessor.fset
            syms['fdel'] = accessor.fdel
        else :
            syms         = accessor()

        if syms['fdel'] : default = syms['fdel'] (self, None)

        self._attributes_register (key, default, self.Any, self.Vector, self.Writable)

        if syms['fget'] : self._attributes_set_getter (key, syms['fget'])
        if syms['fset'] : self._attributes_set_setter (key, syms['fset'])




    ####################################
    def _attributes_unregister (self, key) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Unregister an attribute.

        This function ignores the extensible, final and readonly flag, and is
        supposed to be used by derived classes, not by the consumer of the API.

        Note that unregistering is different from setting the value to 'None' --
        all meta information about the attribute will be removed.  Further
        attempts to access the attribute from the public API will result in an
        DoesNotExist exception.  This method should be used sparingly -- in
        fact, GFD.90 requires final attributes to stay around forever (frozen).
        """

        # make sure interface is ready to use
        us_key = self._attributes_t_underscore (key)
        d = self._attributes_t_init (us_key)

        # if the attribute exists, purge it
        if us_key in d['attributes'] :
            del (d['attributes'][us_key])


    ####################################
    def _attributes_remove (self, key) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Remove an extended an attribute.

        This function allows to safely remove any attribute which is 'extended'
        and has write permissions.
        """

        # make sure interface is ready to use
        us_key = self._attributes_t_underscore (key)
        d = self._attributes_t_init (us_key)

        if self._attributes_i_is_removable (key) :
            del (d['attributes'][us_key])


    ####################################
    def _attributes_set_enums (self, key, enums=None) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Specifies the set of allowed values for Enum typed attributes.  If not
        set, or if list is None, any values are allowed.
        """

        us_key = self._attributes_t_underscore (key)
        d      = self._attributes_t_init       (us_key)

        d['attributes'][us_key]['enums'] = enums


    ####################################
    def _attributes_extensible (self, e=True) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Allow (or forbid) the on-the-fly creation of new attributes.  Note that
        this method also allows to *remove* the extensible flag -- that leaves
        any previously created extended attributes untouched, but just prevents
        the creation of new extended attributes.
        """

        d = self._attributes_t_init ()
        d['extensible'] = e


    ####################################
    def _attributes_camelcasing (self, c=True) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Use 'CamelCase' for dict entries and the GFD.90 API, but 'under_score'
        for properties.

        Note that we do not provide an option to turn CamelCasing off - once it
        is turned on, it stays on -- otherwise we would loose attributes...
        """

        d = self._attributes_t_init ()
        d['camelcasing'] = c


    ####################################
    def _attributes_deep_copy (self, other) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        This method can be used to make sure that deep copies of derived classes
        are also deep copies of the respective attributes.  In accordance with
        GFD.90, the deep copy will ignore callbacks.  It will copy checks
        though, as the assumption is that value constraints stay valid.
        """

        
        # make sure interface is ready to use
        d = self._attributes_t_init ()

        other_d = {}

        # for some reason, deep copy won't work on the 'attributes' dict, so we
        # do it manually.  Use the list copy c'tor to copy list elements.
        other_d['extensible']  = d['extensible']
        other_d['camelcasing'] = d['camelcasing']
        other_d['attributes']  = d['attributes'] 
        other_d['extensible']  = d['extensible'] 
        other_d['camelcasing'] = d['camelcasing']
        other_d['recursion']    = d['recursion']    
        other_d['setter']       = d['setter']    
        other_d['getter']       = d['getter']    
        other_d['lister']       = d['lister']    

        other_d['attributes'] = {}

        for key in d['attributes'] :
            other_d['attributes'][key] = {}
            other_d['attributes'][key]['default']      =       d['attributes'][key]['default']   
            other_d['attributes'][key]['exists']       =       d['attributes'][key]['exists']      
            other_d['attributes'][key]['type']         =       d['attributes'][key]['type']      
            other_d['attributes'][key]['flavor']       =       d['attributes'][key]['flavor']    
            other_d['attributes'][key]['mode']         =       d['attributes'][key]['mode']      
            other_d['attributes'][key]['extended']     =       d['attributes'][key]['extended']  
            other_d['attributes'][key]['camelcase']    =       d['attributes'][key]['camelcase'] 
            other_d['attributes'][key]['underscore']   =       d['attributes'][key]['underscore']
            other_d['attributes'][key]['enums']        = list (d['attributes'][key]['enums'])
            other_d['attributes'][key]['checks']       = list (d['attributes'][key]['checks'])
            other_d['attributes'][key]['callbacks']    = list (d['attributes'][key]['callbacks'])
            other_d['attributes'][key]['recursion']    =       d['attributes'][key]['recursion']
            other_d['attributes'][key]['setter']       =       d['attributes'][key]['setter']
            other_d['attributes'][key]['getter']       =       d['attributes'][key]['getter']

            if d['attributes'][key]['flavor'] == self.Vector and \
               d['attributes'][key]['value' ] != None            :
                other_d['attributes'][key]['value']  = list (d['attributes'][key]['value'])
            else :
                other_d['attributes'][key]['value']  =       d['attributes'][key]['value']

        # set the new dictionary as state for copied class
        _AttributesBase.__setattr__ (other, '_d', other_d)


    ####################################
    def _attributes_dump (self, msg=None) :
        """ 
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Debugging dump to stdout.
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        keys_all   = sorted (d['attributes'].iterkeys ())
        keys_exist = sorted (self._attributes_i_list   ())

        print "---------------------------------------"
        print str (type (self))

        if msg :
            print "---------------------------------------"
            print msg

        print "---------------------------------------"
        print " %-30s : %s"  %  ("Extensible"  , d['extensible'])
        print " %-30s : %s"  %  ("CamelCasing" , d['camelcasing'])
        print "---------------------------------------"

        print "'Registered' attributes"
        for key in keys_all :
            if key not in keys_exist :
                if not  d['attributes'][key]['mode'] == self.Alias and \
                   not  d['attributes'][key]['extended'] :
                    print " %-30s [%-6s, %-6s, %-8s]: %s"  % \
                             (d['attributes'][key]['camelcase'],
                              d['attributes'][key]['type'],
                              d['attributes'][key]['flavor'],
                              d['attributes'][key]['mode'],
                              d['attributes'][key]['value']
                              )

        print "---------------------------------------"

        print "'Existing' attributes"
        for key in keys_exist :
            if not  d['attributes'][key]['mode'] == self.Alias :
                print " %-30s [%-6s, %-6s, %-8s]: %s"  % \
                         (d['attributes'][key]['camelcase'],
                          d['attributes'][key]['type'],
                          d['attributes'][key]['flavor'],
                          d['attributes'][key]['mode'],
                          d['attributes'][key]['value']
                          )

        print "---------------------------------------"

        print "'Extended' attributes"
        for key in keys_all :
            if key not in keys_exist :
                if not  d['attributes'][key]['mode'] == self.Alias and \
                        d['attributes'][key]['extended'] :
                    print " %-30s [%-6s, %-6s, %-8s]: %s"  % \
                             (d['attributes'][key]['camelcase'],
                              d['attributes'][key]['type'],
                              d['attributes'][key]['flavor'],
                              d['attributes'][key]['mode'],
                              d['attributes'][key]['value']
                              )

        print "---------------------------------------"

        print "'Deprecated' attributes (aliases)"
        for key in keys_all :
            if key not in keys_exist :
                if d['attributes'][key]['mode'] == self.Alias :
                    print " %-30s [%24s]:  %s"  % \
                             (d['attributes'][key]['camelcase'],
                              ' ',
                              d['attributes'][key]['alias']
                              )

        print "---------------------------------------"


    ####################################
    def _attributes_set_final (self, key, val=None) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        This method will set the 'final' flag for an attribute, signalling that
        the attribute will never change again.  The ReadOnly flag is ignored.
        A final value can optionally be provided -- otherwise the attribute is
        frozen with its current value.

        Note that attributes_set_final() will trigger callbacks, even if the
        value was not set, or did not change.
        """

        # make sure interface is ready to use
        us_key = self._attributes_t_underscore (key)
        d      = self._attributes_t_init       (us_key)

        newval = val
        oldval = d['attributes'][us_key]['value']
        if None == newval :
            # freeze at current value unless indicated otherwise
            val = oldval

        # flag as final, and set the final value (this order to avoid races in
        # callbacks)
        d['attributes'][us_key]['mode'] = self.Final
        self._attributes_i_set (us_key, val)

        # callbacks are not invoked if the value did not change -- we take care
        # of that here.
        if  None == newval or oldval == newval :
            self._attributes_t_call_cb (key, val)


    ####################################
    def _attributes_add_check (self, key, check) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        Value checks can be added dynamically, and per attribute.  'callable'
        needs to be a python callable, and will be invoked as::

            callable (key, val)

        Those checks will be invoked whenever a new attribute value is set.  If
        that call then returns 'True', the value is accepted.  Otherwise, the
        value will be considered to be invalid, which results in an exception as
        per above.  'callable' can return a string as error message.  
        """

        # make sure interface is ready to use
        us_key = self._attributes_t_underscore (key)
        d = self._attributes_t_init (us_key)

        # register the attribute and properties
        d['attributes'][us_key]['checks'].append (check)


    ####################################
    def _attributes_set_getter (self, key, getter) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        The Attribute API makes no assumptions on how attribute values are kept
        up-to-date.  In general, it expects an asynchronous thread to set
        attribute values as needed.  To keep the complexity low for backend
        developers, it also supports the registration of 'setter' and 'getter'
        hooks.  Those are very similar to callbacks, but kind of inversed: where
        frontend callbacks are invoked on backend attribute changes, backend
        hooks are invoked on frontend attribute queries.  They are expected to
        internally trigger state updates.

        For example, on::

            print c.attrib

        The attribute getter for the 'attrib' attribute will be invoked.  If for
        that attribute a getter hook is registered, that hook will first query
        the backend for value updates.  After that update has been performed,
        the getter will retrieve the (updated) value.

        Similarly, setter hooks will be invoked *after* the attribute setter
        method, to inform the implementation of the updated attribute value.

        Further, list hooks are invoked before a list or find operation is
        really internally executed, to allow the implementation to updated the
        list of available attributes.  
        
        Note that only one setter/getter method can be registered per key, and
        one listers per class instance.  Additionally, one setter and one getter
        can be registered for the key 'None', which will invoked for every
        attribute r/w access.

        Hooks have a different call signature than callbacks::
        
            setter (self, key, value)
            getter (self, key)
            lister (self)

        As with callbacks, hooks will remain registered as long as they return
        'True'. 

        Note that frequent setter, and even more list and getter calls are very
        common -- the implementation of hooks should consider to cache the
        respective values.
        """

        if key != None :
            # make sure interface is ready to use
            us_key = self._attributes_t_underscore (key)
            d      = self._attributes_t_init       (us_key)

            # register the attribute and properties
            d['attributes'][us_key]['getter'] = getter

        else :
            # make sure interface is ready to use
            d = self._attributes_t_init ()

            # register the attribute and properties
            d['getter'] = getter


    ####################################
    def _attributes_set_setter (self, key, setter) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        See documentation of L{_attributes_set_setter } for details.
        """

        if key != None :
            # make sure interface is ready to use
            us_key = self._attributes_t_underscore (key)
            d      = self._attributes_t_init       (us_key)

            # register the attribute and properties
            d['attributes'][us_key]['setter'] = setter

        else :
            # make sure interface is ready to use
            d = self._attributes_t_init ()

            # register the attribute and properties
            d['setter'] = setter


    ####################################
    def _attributes_set_lister (self, key, lister) :
        """
        This interface method is not part of the public consumer API, but can
        safely be called from within derived classes.

        See documentation of L{_attributes_set_setter } for details.
        """

        # make sure interface is ready to use
        us_key = self._attributes_t_underscore (key)
        d      = self._attributes_t_init       (us_key)

        # register the attribute and properties
        d['lister'] = lister


    ###########################################################################
    #
    # the GFD.90 attribute interface
    #
    # The GFD.90 interface supports CamelCasing, and thus converts all keys to
    # underscore before using them.
    # 
    ####################################
    def set_attribute (self, key, val) :
        """
        set_attribute(key, val)

        This method sets the value of the specified attribute.  If that
        attribute does not exist, DoesNotExist is raised -- unless the attribute
        set is marked 'extensible'.  In that case, the attribute is created and
        set on the fly (defaulting to mode=Writable, flavor=Scalar, type=Any,
        default=None).  A value of 'None' may reset the attribute to its default
        value, if such one exists (see documentation).

        Note that this method is performing a number of checks and conversions,
        to match the value type to the attribute properties (type, mode, flavor).
        Those conversions are not guaranteed to yield the expected result -- for
        example, the conversion from 'scalar' to 'vector' is, for complex types,
        ambiguous at best, and somewhat stupid.  The consumer of the API SHOULD
        ensure correct attribute values.  The conversions are intended to
        support the most trivial and simple use cases (int to string etc).
        Failed conversions will result in an BadParameter exception.

        Attempts to set a 'final' attribute are silently ignored.  Attempts to
        set a 'readonly' attribute will result in an IncorrectState exception
        being raised.

        Note that _attributes_i_set() will trigger callbacks, if a new value
        (different from the old value) is given.  
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_set        (us_key, val)


    ####################################
    def get_attribute (self, key) :
        """
        get_attribute(key)

        This method returns the value of the specified attribute.  If that
        attribute does not exist, an DoesNotExist is raised.  It is not an
        error to query an existing, but unset attribute though -- that will
        result in 'None' to be returned (or the default value, if available).
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_get        (us_key)


    ####################################
    def set_vector_attribute (self, key, val) :
        """
        set_vector_attribute (key, val)

        See also: L{set_attribute} (key, val).

        As python can handle scalar and vector types transparently, this method
        is in fact not very useful.  For that reason, it maps internally to the
        set_attribute method.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_set        (us_key, val)


    ####################################
    def get_vector_attribute (self, key) :
        """
        get_vector_attribute (key)

        See also: L{get_attribute} (key).

        As python can handle scalar and vector types transparently, this method
        is in fact not very useful.  For that reason, it maps internally to the
        get_attribute method.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_get        (us_key)


    ####################################
    def remove_attribute (self, key) :
        """
        remove_attribute (key)

        Removing an attribute is actually different from unsetting it, or from
        setting it to 'None'.  On remove, all traces of the attribute are
        purged, and the key will not be listed on L{list_attributes}() anymore.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_remove       (us_key)


    ####################################
    def list_attributes (self) :
        """
        list_attributes ()

        List all attributes which have been explicitly set. 
        """

        return self._attributes_i_list ()


    ####################################
    def find_attributes (self, pattern) :
        """
        find_attributes (pattern)

        Similar to list(), but also grep for a given attribute pattern.  That
        pattern is of the form 'key=val', where both 'key' and 'val' can contain
        POSIX shell wildcards.  For non-string typed attributes, the pattern is
        applied to a string serialization of the typed value, if that exists.
        """

        return self._attributes_i_find (pattern)


    ####################################
    def attribute_exists (self, key) :
        """
        attribute_exist (key)

        This method will check if the given key is known and was set explicitly.
        The call will also return 'True' if the value for that key is 'None'.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_exists (us_key)


    ####################################
    def attribute_is_readonly (self, key) :
        """
        attribute_is_readonly (key)

        This method will check if the given key is readonly, i.e. cannot be
        'set'.  The call will also return 'True' if the attribute is final
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_is_readonly (us_key)


    ####################################
    def attribute_is_writable (self, key) :
        """
        attribute_is_writable (key)

        This method will check if the given key is writable - i.e. not readonly.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_is_writable (us_key)


    ####################################
    def attribute_is_removable (self, key) :
        """
        attribute_is_writable (key)

        This method will check if the given key can be removed.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_is_removable (us_key)


    ####################################
    def attribute_is_vector (self, key) :
        """
        attribute_is_vector (key)

        This method will check if the given attribute has a vector value type.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_is_vector (us_key)


    ####################################
    # fold the GFD.90 monitoring API into the attributes API
    ####################################
    def add_callback (self, key, cb) :
        """
        add_callback (key, cb)

        For any attribute change, the API will check if any callbacks are
        registered for that attribute.  If so, those callbacks will be called
        in order of registration.  This registration function will return an
        id (cookie) identifying the callback -- that id can be used to
        remove the callback.

        A callback is any callable python construct, and MUST accept three
        arguments::

            - String key: the name of the attribute which changed
            - Any    val: the new value of the attribute
            - Any    obj: the object on which this attribute interface was called

        The 'obj' can be any python object type, but is guaranteed to expose
        this attribute interface.

        The callback SHOULD return 'True' or 'False' -- on 'True', the callback
        will remain registered, and will thus be called again on the next
        attribute change.  On returning 'False', the callback will be
        unregistered, and will thus not be called again.  Returning nothing is
        interpreted as 'False', other return values lead to undefined behavior.

        Note that callbacks will not be called on 'Final' attributes (they will
        be called once as that attribute enters finality).
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_add_cb (us_key, cb)


    ####################################
    def remove_callback (self, key, id) :
        """
        remove_callback (key, id)

        This method allows to unregister a previously registered callback, by
        providing its id.  It is not an error to remove a non-existing cb, but
        a valid ID MUST be provided -- otherwise, a BadParameter is raised.

        If no ID is provided (id == None), all callbacks are removed for this
        attribute.
        """

        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return self._attributes_i_del_cb (us_key, id)



    ############################################################################
    #
    # Python property interface
    #
    # we assume that properties are always used in under_score notation.
    #
    ####################################
    def __getattr__ (self, key) :
        """ see L{get_attribute} (key) for details. """
        
        key  = self._attributes_t_keycheck (key)
        return self._attributes_i_get (key)


    ####################################
    def __setattr__ (self, key, val) :
        """ see L{set_attribute} (key, val) for details. """
        
        key  = self._attributes_t_keycheck (key)
        return self._attributes_i_set (key, val)


    ####################################
    def __delattr__ (self, key) :
        """ see L{remove_attribute} (key) for details. """
        
        key  = self._attributes_t_keycheck (key)
        return self._attributes_remove (key)



    ###########################################################################
    #
    # The Python dictionary interface
    # 
    # The dict interface supports CamelCasing, and thus converts all keys to
    # underscore before using them.
    #
    ####################################
    def __getitem__ (self, key) :
        """ see L{get_attribute} (key) for details. """
        
        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_get        (us_key)
   

    ####################################
    def __setitem__ (self, key, val) :
        """ see L{set_attribute} (key, val) for details. """
        
        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_set        (us_key, val)
   

    ####################################
    def __delitem__ (self, key) :
        """ see L{remove_attribute} (key) for details. """
        
        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_remove       (us_key)
   

    ####################################
    def __contains__ (self, key) :
        """ see L{attribute_exists} (key) for details. """
        
        key    = self._attributes_t_keycheck   (key)
        us_key = self._attributes_t_underscore (key)
        return   self._attributes_i_exists     (us_key)
   

    ####################################
    def update (self, *args, **kwargs) :
        """ Initialize attributes from a dictionary or named parameters """
        
        if args:
            if len (args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len (args))
            other = dict (args[0])
            for key in other:
                self._attributes_i_set (key, other[key])
        for key in kwargs:
            self._attributes_i_set (key, kwargs[key])


    ####################################
    def iterkeys (self) :
        """ see L{list_attributes} () for details. """
        
        return self._attributes_i_list ()


    ####################################
    def __str__ (self) :
        """ 
        The string representation of the attributes is, right now, somewhat
        arbitrarily defined as to make the bliss attribute unit tests happy:
        we ignore unset values and extended values.  
        """

        # make sure interface is ready to use
        d = self._attributes_t_init ()

        tmp = {}

        for key in self._attributes_i_list (ext=False) :
            tmp[key] = d['attributes'][key]['value']

        return str (tmp)
            

   
################################################################################

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

