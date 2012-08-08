# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Exception import Exception as MyException
from bliss.saga.Error     import Error     as MyError


################################################################################

import inspect
import re

# FIXME: add a tagging 'Monitorable' interface, which enables callbacks.
# FIXME: add a flag to mark attributes as fixed, so that app cannot change flags (type...)
#        also: __delattr__

################################################################################
#
# Callback (Abstract) Class
#
class Callback () :
    """
    Callback base class.

    All stateful objects of the pilot API allow to register a callback for any
    changes of its attributes, such as 'state' and 'state_detail'.  Those
    callbacks can be python call'ables, or derivates of this callback base
    class.  Instances which inherit this base class MUST implement (overload)
    the cb() method.

    The callable, or the callback's cb() method is what is invoked whenever the
    TROY implementation is notified of an change on the monitored object's
    attribute.

    The cb instance receives three parameters upon invocation:

      - member: the watched attribute (e.g. 'state' or 'state_detail')
      - value:  the new value of the watched attribute
      - obj:    the watched object instance

    If the callback returns 'True', it will remain registered after invocation,
    to monitor the attribute for the next subsequent state change.  On returning
    'False' (or nothing), the callback will not be called again.

    To register a callback on a object instance, use::

      class MyCallback (troy.pilot.Callback) :

        def __init__ (self, msg) :
          self.msg_ = msg

        def cb (self, obj, member, value) :
          print " %s\\n %s (%s) : %s"  %  self.msg_, obj, member, value

        def main () :

          cpd = troy.pilot.compute_pilot_description ()
          cps = troy.pilot.compute_pilot_service ()
          cp  = cps.create_pilot (cpd)

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
        raise MyException ("Callback class must be inherited before use!", 
                           MyError.IncorrectState)


    def cb (self, wu, member, value) :
        """ This is the method that needs to be implemented by the application

            Keyword arguments::

                member: the watched attribute
                value:  the new value of the watched attribute
                obj:    the watched object instance

            Return::

                keep:   bool, signals to keep (True) or remove (False) the callback
                        after invocation

            Callback invocation MAY (and in general will) happen in a separate
            thread -- so the application need to make sure that the callback
            code is thread-safe.

            The boolean return value is used to signal Troy if the callback
            should continue to listen for events (return True) , or if it rather
            should get unregistered after this invocation (return False).
        """
        pass



################################################################################
#
#
#
class AttributesBase_ (object) :
    """ 
    This class only exists to host properties -- as object itself does *not* have
    properties!  This class is not part of the public Troy API.
    """
    def __init__ (self) :
        pass


class AttributeInterface (AttributesBase_) :
    """
    This base class implements most of the semantics of the L{Attributes}
    interface.  That interface
    Attribute Interface Class

    The Attributes interface has a very simple API -- it can be used as a Python
    dictionary.  In fact, in inherits from 'dict', and can thus interchangeably
    used.  By overloading the dictionary setter and getter methods it provides,
    however, some additional semantics.

    In particular, a class which uses this interface can internally specify
    which attributes can be set, and what type they have.  Also, default values
    can be specified, and the class provides a rudimentary support for
    converting scalar attributes into vector attributes and back.

    Also, the consumer of this API can register callbacks, which get triggered
    on changes to specific attribute values.

    Example use case::


        ###########################################
        class Transliterator ( pilot.Attributes ) :
            
            def __init__ (self, *args, **kwargs) :
              # setting attribs to non-extensible will cause the cal to init below to
              # complain if attributes are specified.  Default is extensible.
              # self.attributes_extensible_ (False)
        
                # pass args to base class init (implies extensible)
                super (Transliterator, self).__init__ (*args, **kwargs)
        
                # setup class attribs
                self.attributes_register_   ('apple', 'Appel', self.Url,    self.Scalar, self.Writeable)
                self.attributes_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)
        
              # setting attribs to non-extensible at *this* point will have allowed
              # custom user attribs on __init__ time (via args), but will then forbid
              # any additional custom attributes
              # self.attributes_extensible_ (False)
        
        
        ###########################################
        if __name__ == "__main__":
        
            def cb (key, val, obj) :
                print "called: %s - %s - %s"  %  (key, val, type (obj))
                return True
        
            trans = Transliterator (cherry='Kersche')
        
            print "\\n -- apple"
            print trans.apple 
            print trans['apple']
            trans.apple = 'Abbel'
            print trans.apple 
        
            trans.add_callback ('apple', cb)
            trans.apple = ['Abbel', 'Appel']
            trans.apple = 'Apfel'
        
            trans.attributes_set_final_ ('apple')
            trans.apple = 'Abbel'
            print trans.apple 
        
            print "\\n -- plum"
            print trans.plum
          # trans.plum    = 'Pflaume'  # raises readonly exception
          # trans['plum'] = 'Pflaume'  # raises readonly exception
            print trans.plum
        
            print "\\n -- cherry"
            print trans.cherry
        
            print "\\n -- peach"
            trans['peach'] = 'Berne'
            print trans.peach
            trans.peach = 'Birne'
            print trans.peach


    This example will result in::

        -- apple
        Appel
        Appel
        Apfel
        called: apple - ['Boskop', 'Jonas'] - <class '__main__.Transliterator'>
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

    # FIXME: need an internal method to set readonly attributes from within
    # Troy.  That in turn means we have to move the checks/conversions into
    # a separate private routine, to use them consistently for public and
    # private setters.


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

    # mode enums
    Writeable   = 'writeable'  # the consumer of the interface can change
                               # the attrib value
    ReadOnly    = 'readonly'   # the consumer of the interface can not
                               # change the attrib value.  The
                               # implementation can still change it.
    Final       = 'final'      # neither consumer nor implementation can
                               # change the value anymore

    # extensible enum
    Extended    = True         # new attributes can be added on the fly
    NotExtended = False        # setting new attributes will raise an exception

    # flavor enums
    Scalar      = 'scalar'     # the attribute value is a single data element
    Vector      = 'vector'     # the attribute value is a list of data elements


    camel_case_regex_1_ = re.compile('(.)([A-Z][a-z]+)')
    camel_case_regex_2_ = re.compile('([a-z0-9])([A-Z])')


    ############################################################################
    #
    #
    #
    def __init__ (self, *args, **kwargs) :
        """
        This method is not supposed to be directly called by the consumer of
        this API -- it is called indirectly via derived object construction.

        init makes sure that the basic structures are in place on the attribute
        dictionary - this saves us ton of safety checks later on.
        """

        # self.attributes_dump_ ("init")

        # initialize state
        d = self.attributes_t_init_ ()

        # call to update and the args/kwargs handling seems to be part of the
        # dict interface conventions
        self.update (*args, **kwargs)


    ############################################################################
    #
    # Internal interface tools.
    #
    # Those tools (attributes_t_*) are only for internal use, and should never
    # be called from the outside.
    #
    # Naming: attributes_t_*_
    #
    def attributes_t_init_ (self, key=None) :
        """
        This method is not supposed to be directly called by the consumer of
        this API.

        The attributes_t_init_ method initializes the interface's internal data
        structures.  We always need the attribute dict, and the extensible flag.
        Everything else can be added on the fly.  The method will not overwrite
        any settings -- initialization occurs only once!

        If a key is given, the existence of this key is checked.  An exception
        is raised if the key does not exist.
        """

        d = {}

        try :
            d = AttributesBase_.__getattribute__ (self, 'd_')
        except :
            # need to initialize -- any exceptions in the code below should fall through
            d['attributes_']  = {}
            d['extensible_']  = True
            d['camelcasing_'] = False

            AttributesBase_.__setattr__ (self, 'd_', d)


        # check if we know about that attribute
        if key :
            if not key in d['attributes_'] :
                raise MyException (" attribute key is invalid: %s"  %  (key),
                                     MyError.DoesNotExist)
        # all is well
        return d


    ####################################
    def attributes_t_call_cb_ (self, key) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the invocation of all callbacks for a given attribute.
        Callbacks returning False (or nothing at all) will be unregistered after
        their invocation.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ (key)

        for id in range (len(d['attributes_'][key]['callbacks'])) :
            cb = d['attributes_'][key]['callbacks'][id]

            ret = False
            if inspect.isclass (cb) and \
               issubclass (cb, Callback) :
                ret = cb.cb (key, self.__get_attr__ (key), self)
            else :
                ret = cb (key, self.__getattr__ (key), self)

            # remove callbacks which return 'False'
            if not ret :
                self.attributes_unregister_cb (key, id)


    ####################################
    def attributes_t_underscore_ (self, key) :
        """ 
        This is an internal method, and should not be called outside this
        interface implementation.

        The method accepts a 'CamelCase'd word, and translates that into
        'under_score' notation -- IFF 'camelcasing_' is set

        Kudos: http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        # camel_case_regex_1_ = re.compile('(.)([A-Z][a-z]+)')
        # camel_case_regex_2_ = re.compile('([a-z0-9])([A-Z])')

        if d['camelcasing_'] :
            temp = AttributeInterface.camel_case_regex_1_.sub(r'\1_\2', key)
            return AttributeInterface.camel_case_regex_2_.sub(r'\1_\2', temp).lower()
        else :
            return key



    ####################################
    def attributes_t_conversion_ (self, key, val) :
        """
        This is an internal method, and should not be called outside this
        interface implementation.

        The method checks a given attribute value against the attribute's
        flags, and performs some simple type conversion as needed.  Also, the
        method will restore a 'None' value to the attribute's default value.
        """
        # make sure interface is ready to use
        d = self.attributes_t_init_ ()
        orig = val

        # if the key is not known
        if not key in d['attributes_'] :
            # cannot handle unknown attributes
            return val

        # check if a value is given.  If not, revert to the default value
        # (if available)
        if val == None :
            if 'default' in d['attributes_'][key] :
                val = d['attributes_'][key]['default']


        # perform flavor and type conversion
        val = self.attributes_t_conversion_flavor_ (key, val)

        # apply all value checks on the conversion result
        for check in d['attributes_'][key]['checks'] :
            ret = check (key, val)
            if ret != True :
                raise MyException (" attribute value %s is not valid: %s"  %  (key, ret),
                                     MyError.BadParameter)

        # aaaand done
        return val


    ####################################
    def attributes_t_conversion_flavor_ (self, key, val) :
        """ This method should ONLY be called by attributes_t_conversion_! """
        # FIXME: there are certainly nicer and more reversible ways to
        #        convert the flavors...
        # TODO: consider splitting strings?

        d = self.attributes_t_init_ (key)
        f = d['attributes_'][key]['flavor']

        # easiest conversion of them all... ;-)
        if val == None :
            return None


        # check if we need to serialize a list into a scalar
        if f == self.Vector :
            # we want a vector
            if not isinstance (val, list) :
                # need to create vec from scalar
                if isinstance (val, basestring) :
                    # for string values, we split on white spaces and type-convert 
                    # all elements
                    vec = val.split ()
                    ret = []
                    for element in vec :
                        ret.append (self.attributes_t_conversion_type_ (key, element))
                    return ret
                else :   
                    # all non-string types are interpreted as elements of
                    # a single-member list
                    return [self.attributes_t_conversion_type_ (key, val)]
            else :
                # val is already vec - apply type conversion on all elems
                ret = []
                for elem in val :
                    ret.append (self.attributes_t_conversion_type_ (key, elem))
                return ret


        elif f == self.Scalar :
            # we want a scalar
            if isinstance (val, list) :
                # need to create scalar from vec
                if len (val) > 1 :
                    # if the list has more than one element, we use an intermediate
                    # string representation of the list before converting to a scalar
                    tmp = ""
                    for i in val :
                        tmp += str(i) + " "
                    return self.attributes_t_conversion_type_ (key, tmp)
                elif len (val) == 1 :
                    # for single element lists, we simply use the one element as
                    # scalar value 
                    return self.attributes_t_conversion_type_ (key, val[0])
                else :
                    # no value...
                    return None
            else :
                # scalar is already scalar, just do type conversion
                return self.attributes_t_conversion_type_ (key, val)


        # we should never get here...
        raise MyException (" Cannot evaluate attribute flavor (%s) : %s"  %  (key, str(f)),
                             MyError.NoSuccess)


    ####################################
    def attributes_t_conversion_type_ (self, key, val) :
        """ This method should ONLY be called by attributes_t_conversion_! """
        d = self.attributes_t_init_ (key)
        t = d['attributes_'][key]['type']

        # oh python...
        ret = None
        
        try :
            # FIXME: add time/date conversion to/from string
            if   t == self.Any    : ret =        val  
            elif t == self.Int    : ret = int   (val) 
            elif t == self.Float  : ret = float (val) 
            elif t == self.Bool   : ret = bool  (val) 
            elif t == self.String : ret = str   (val) 
            else                  : ret =        val  
        except ValueError as e:
            raise MyException (" attribute value %s has incorrect type: %s" %  (key, val),
                                 MyError.BadParameter)

        return ret


    ###########################################################################
    #
    # internal interface
    #
    # This internal interface is used by the public interfaces (dict,
    # properties, GFD.90).  We assume that CamelCasing and under_scoring is
    # sorted out before this internal interface is called.  All other tests,
    # verifications, and conversion are done here though.
    #
    # Naming: attributes_i_*_
    #
    ####################################
    def attributes_i_get_ (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is implicitly used via the dictionary interface.

        The getattr method returns the value of the specified attribute.  If
        that attribute does not exist, an AttributeError is raised.  It is not
        an error to query an unset attribute though -- that will result in
        'None' to be returned.

        Note that this method is not performing any checks or conversions --
        those are all performed when *setting* an attribute.  So, any attribute
        flags (type, mode, flavor) are evaluated on setting, not on getting.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ (key)

        if not 'value' in d['attributes_'][key] :
            return None

        return d['attributes_'][key]['value']



    ####################################
    def attributes_i_set_ (self, key, val=None, force=False) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is implicitly used via the dictionary interface.

        The setattr method sets the value of the specified attribute.  If that
        attribute does not exist, an AttributeError is raised -- unless the
        attribute set is marked 'extensible' -- in that case, the attribute is
        created and set on the fly.  It is not an error to query unset attribute
        though -- that is done by setting it to 'None'.  If a default is
        specified for an attribute, setting 'None' will in fact restore the
        default value.

        Note that this method is performing a number of checks and conversions,
        to match the value type to the attribute flags (type, mode, flavor).
        Those conversions are not guaranteed to yield the expected result -- for
        example, the conversion from 'scalar' to 'vector' is, for complex types,
        ambiguous at best, and very likely stupid.  The consumer of the API
        SHOULD ensure correct attribute values.  The conversions are intended to
        support the most trivial and simple use cases (int to string etc).
        Failed conversions will result in an Attribute Error.

        Checks can be added dynamically, and per attribute, by calling
        attributes_check_add_ (key, callable).  'callable' needs to be a python
        callable, and will be invoked as::

            callable (key, val)

        If that call returns 'True', the value is accepted.  Otherwise, the
        value will be considered to be invalid, which usually results in an
        exception.  'callable' can in this case return a string as error
        message.


        Note::

            Conversions and checks are incomplete at this point!
            See code documentation (FIXMEs) for details.

        Attempts to set a 'final' attribute are silently ignored.  Attempts to
        set a 'readonly' attribute will result in an AttributeError being
        raised.

        The 'force' flag can be set internally if the attribute should be set
        irrespectively of its mode and permissions.

        If no value is provided, the attribute's value is set to 'None'.  Note
        that attributes_set_() will trigger callbacks, if a new value (different
        from the old value) is given.  For new attributes, the default value
        will be 'None'.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        # only perform perm and mode checks if not in 'force' mode
        if not force :
            # if the key is not known
            if not key in d['attributes_'] :
                if not d['extensible_'] :
                    # we cannot add new keys on non-extensible sets
                    raise AttributeError(" attribute set is not extensible (key %s)" %  key)
                else :
                    # if the set is extensible, we can register the new key.  It
                    # won't have any callbacks at this point.
                    self.attributes_register_ (key, None, self.Any, self.Scalar, self.Writeable, self.Extended)

            # known attribute - attempt to set if
            else:

                # check if we are allowed to change the attribute - complain if not.
                # Also, simply ignore write attempts to finalized keys.
                if 'mode' in  d['attributes_'][key] :

                    mode = d['attributes_'][key]['mode']

                    if   self.Final == mode :
                        return
                    elif self.Writeable != mode :
                        raise AttributeError(" attribute %s is not writeable" %  key)

        # permissions are confirmed, set the attribute with conversion etc.

        # apply any attribute conversion
        val = self.attributes_t_conversion_ (key, val)

        # make sure the key's value entry exists
        if not 'value' in d['attributes_'][key] :
            d['attributes_'][key]['value'] = None

        # only once an attribute is explicitely set, it 'exists' for the purpose
        # of the 'attribute_exists' call, and the key iteration
        d['attributes_'][key]['exists'] = True

        # only actually change the attribute when the new value differs --
        # and only then invoke any callbacks.

        if val != d['attributes_'][key]['value'] :
            d['attributes_'][key]['value'] = val
            self.attributes_t_call_cb_ (key)


    ####################################
    def attributes_i_add_cb_ (self, key, cb) :
        """
        For any attribute change, the API will check if any callbacks are
        registered for that attribute.  If so, those callbacks will be called
        in order of registration.  This registration function will return an
        id (cookie) identifying the callback -- that id can be used to
        unregister the callback.

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

        Note that callbacks will not be called on 'Final' attributes.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ (key)

        d['attributes_'][key]['callbacks'].append (cb)
        return len (d['attributes_'][key]['callbacks']) - 1


    ####################################
    def attributes_i_del_cb_ (self, key, id=None) :
        """
        This method allows to unregister a previously registered callback, by
        providing its id.  It is not an error to remove a non-existing cb, but
        a valid ID MUST be provided -- otherwise, an AttributeError is raised.

        If no ID is provided (id == None), all callbacks are removed for this
        attribute.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ (key)

        # id == None: remove all callbacks
        if not id :
            d['attributes_'][key]['callbacks'] = []
        else :
            if len (d['attributes_'][key]['callbacks']) < id :
                raise AttributeError(" invalid callback cookie"  %  key)
            else :
                d['attributes_'][key]['callbacks'][id] = undef


    ####################################
    def attributes_i_exists_ (self, key) :
        """
        This method will check if the given key is registered.  The call will
        also return 'True' if the value for that key is 'None'
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        # check if we know about that attribute
        if key in d['attributes_'] :
            if  d['attributes_'][key]['exists'] :
                return True

        return False


    ####################################
    def attributes_i_is_final (self, key) :
        """
        This method will query the 'final' flag for an attribute, which signals that
        the attribute will never change again.
        """

        # make sure interface is ready to use
        d = self.attributes_t_init_ (key)

        if self.Final == d['attributes_'][key]['mode'] :
             return True

        # no final flag found -- assume non-finality!
        return False


    ####################################
    # FIXME: add other inspection methods (is_writeable, is_vector, ...)


    ############################################################################
    #
    # This part of the interface is primarily for use in deriving classes, which
    # thus provide the Attributes interface
    #
    # We expect keys to be provided as CamelCase.
    #
    # Naming: attributes_*_
    #
    ####################################
    def attributes_register_ (self, key, default=None, typ=Any, flavor=Scalar, mode=Writeable, ext=False) :
        """
        Register a new attribute.

        This function ignores the extensible, final and readonly flag, and is
        supposed to be used by derived classes, not by the consumer of the API.

        Note that the given attribute will overwrite any previously existing
        attribute w/o warning (even if that one was final).
        """
                # FIXME: check for correct mode and flavor settings

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        # we expect keys to be registered as CamelCase (in those cases where
        # that matters).  But we store lookup in booth directions, and use the
        # 'under_score' version as primary key
        cc_key = key
        us_key = self.attributes_t_underscore_ (key)

        # remove any old instance of this attribute
        if us_key in  d['attributes_'] :
            self.attributes_unregister_ (us_key)

        # register the attribute and properties
        d['attributes_'][us_key]               = {}
        d['attributes_'][us_key]['value']      = default
        d['attributes_'][us_key]['default']    = default
        d['attributes_'][us_key]['type']       = typ
        d['attributes_'][us_key]['exists']     = False
        d['attributes_'][us_key]['flavor']     = flavor
        d['attributes_'][us_key]['mode']       = mode
        d['attributes_'][us_key]['extended']   = ext
        d['attributes_'][us_key]['callbacks']  = []
        d['attributes_'][us_key]['camelcase']  = key
        d['attributes_'][us_key]['underscore'] = self.attributes_t_underscore_ (key)
        d['attributes_'][us_key]['enums']      = []
        d['attributes_'][us_key]['checks']     = []

        # for enum types, we add a value checker
        if typ == self.Enum :
            def enum_check_ (key, val) :
                if not val :
                    # None is always allowed
                    return True
                
                us_key = self.attributes_t_underscore_ (key)
                d    = self.attributes_t_init_ (us_key)
                vals = d['attributes_'][us_key]['enums']

                if None == vals or \
                   0    == len(vals) :
                    # nothing to check against
                    return True

                # now value must be one of allowed enums
                for v in vals :
                    if v == val :
                        return True

                return """
                incorrect value (%s) for Enum typed attribute (%s).
                Allowed values: %s
                """  %  (str(val), key, str(vals))

            self.attributes_check_add_ (key, enum_check_)



    ####################################
    def attributes_unregister_ (self, key) :
        """
        Unregister an attribute.

        This function ignores the extensible, final and readonly flag, and is
        supposed to be used by derived classes, not by the consumer of the API.

        Note that unregistering is different from setting the value to 'None' --
        all meta information about the attribute will be removed.

        """

        # make sure interface is ready to use
        us_key = self.attributes_t_underscore_ (key)
        d = self.attributes_t_init_ (us_key)

        # if the attribute exists, purge it
        if us_key in d['attributes_'] :
            del (d['attributes_'][us_key])


    ####################################
    def attributes_set_enum_ (self, key, l=None) :
        """
        Specifies the set of allowed values for Enum typed attributes.  If not
        set, or if list is None, any values are allowed/
        """
        us_key = self.attributes_t_underscore_ (key)
        d = self.attributes_t_init_ (us_key)
        d['attributes_'][us_key]['enums'] = l

    ####################################
    def attributes_extensible_ (self, e=True) :
        """
        Allow (or forbid) the on-the-fly creation of new attributes.
        This method should only be called within derived classes.
        """

        d = self.attributes_t_init_ ()
        d['extensible_'] = e


    ####################################
    def attributes_camelcasing_ (self, c=True) :
        """
        use 'CamelCase' for dict entries, but 'under_score' for properties.
        This method should only be called within derived classes.
        """

        d = self.attributes_t_init_ ()
        d['camelcasing_'] = c


    ####################################
    def attributes_deep_copy_ (self, other) :
        
        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        other_d = {}

        other_d['extensible_']  = d['extensible_']
        other_d['camelcasing_'] = d['camelcasing_']

        # for some reason, deep copy won't work on the 'attributes_' dict
        other_d['attributes_'] = {}
        for key in d['attributes_'] :
            other_d['attributes_'][key] = {}
            other_d['attributes_'][key]['value']      = d['attributes_'][key]['value']     
            other_d['attributes_'][key]['default']    = d['attributes_'][key]['default']   
            other_d['attributes_'][key]['type']       = d['attributes_'][key]['type']      
            other_d['attributes_'][key]['flavor']     = d['attributes_'][key]['flavor']    
            other_d['attributes_'][key]['mode']       = d['attributes_'][key]['mode']      
            other_d['attributes_'][key]['extended']   = d['attributes_'][key]['extended']  
            other_d['attributes_'][key]['callbacks']  = d['attributes_'][key]['callbacks'] 
            other_d['attributes_'][key]['camelcase']  = d['attributes_'][key]['camelcase'] 
            other_d['attributes_'][key]['underscore'] = d['attributes_'][key]['underscore']

        # set the new dictionary as state
        AttributesBase_.__setattr__ (other, 'd_', other_d)


    ####################################
    def attributes_dump_ (self, msg=None) :
        """ debugging dump to stderr """

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        if msg :
            print "---------------------------------------"
            print msg

        print "---------------------------------------"
        print " %-30s : %s"  %  ("Extensible"  , d['extensible_'])
        print " %-30s : %s"  %  ("CamelCasing" , d['camelcasing_'])
        print "---------------------------------------"

        # if the key is not known
        for key in sorted(d['attributes_'].iterkeys()) :
            print " %-30s : %s"  %  (key, d['attributes_'][key]['value'])

        print "---------------------------------------"


    ####################################
    def attributes_set_final_ (self, key, val=None) :
        """
        This method will set the 'final' flag for an attribute, signalling that
        the attribute will never change again.  A final value can optionally be
        provided -- otherwise the attribute is frozen with its current value.

        Note that attributes_set_final() will trigger callbacks, if a new value
        is  given.

        This function ignores the readonly flag, and is supposed to be used by
        derived classes, not by the consumer of the API.

        """

        # make sure interface is ready to use
        us_key = self.attributes_t_underscore_ (key)
        d = self.attributes_t_init_ (us_key)

        if None == val :
            # freeze at current value unless indicated otherwise
            val = d['attributes_'][us_key]['value']

        # flag as final, and set the final value (this order to avoid races in
        # callbacks)
        d['attributes_'][us_key]['mode'] = self.Final
        self.attributes_i_set_ (us_key, val)



    ######################################
    # def attributes_config_ (self, key, option, value) :
    #     """
    #     Configure some attribute
    # 
    #     This is a private interface function, and should not be used by the
    #     application programmer.  It can be used to retroactively change and
    #     extend the attribute settings and flags.  Valid values for 'option'
    #     and 'value' should be obvious -- if not, you don't want to use this
    #     method.
    #     """
    # 
    #     # make sure interface is ready to use
    #     us_key = self.attributes_t_underscore_ (key)
    #     d = self.attributes_t_init_ (us_key)
    # 
    #     # register the attribute and properties
    #     d['attributes_'][us_key][option] = value


    ####################################
    def attributes_check_add_ (self, key, call) :
        # make sure interface is ready to use
        us_key = self.attributes_t_underscore_ (key)
        d = self.attributes_t_init_ (us_key)

        # register the attribute and properties
        d['attributes_'][us_key]['checks'].append (call)


    ###########################################################################
    #
    # the GFD.90 attribute interface
    #
    # The GFD.90 interface supports CamelCasing, and thus converts all keys to
    # underscore before using them.
    # 
    ####################################
    def set_attribute (self, key, val) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_set_ (us_key, val)

    ####################################
    def get_attribute (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_get_ (us_key)

    ####################################
    def get_vector_attribute (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_get_ (us_key)

    ####################################
    def set_vector_attribute (self, key, val) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_set_ (us_key, val)

    ####################################
    def attribute_exists (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_exists_ (us_key)

    ####################################
    def remove_attribute (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_unregister_ (us_key)

    ####################################
    def add_callback (self, key, cb) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_add_cb_ (us_key, cb)

    ####################################
    def remove_callback (self, key, id) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_del_cb_ (us_key, id)



    ############################################################################
    #
    # Python property interface
    #
    # we assume that properties are always used in under_score notation.
    #
    ####################################
    def __getattr__ (self, key) :
        return self.attributes_i_get_ (key)

    ####################################
    def __setattr__ (self, key, val) :
        return self.attributes_i_set_ (key, val)

    ####################################
    def __delattr__ (self, key) :
        return self.attributes_unregister_ (key)



    ###########################################################################
    #
    # The Python dictionary interface
    # 
    # The dict interface supports CamelCasing, and thus converts all keys to
    # underscore before using them.
    #
    ####################################
    def __getitem__ (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_get_ (us_key)
   
    ####################################
    def __setitem__ (self, key, val) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_set_ (us_key, val)
   
    ####################################
    def __delitem__ (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_unregister_ (us_key)
   
    ####################################
    def __contains__ (self, key) :
        us_key = self.attributes_t_underscore_ (key)
        return self.attributes_i_exists_ (us_key)
   
    ####################################
    def update (self, *args, **kwargs) :
        if args:
            if len (args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len (args))
            other = dict (args[0])
            for key in other:
                self.attributes_i_set_ (key, other[key])
        for key in kwargs:
            self.attributes_i_set_ (key, kwargs[key])

    ####################################
    def __str__ (self) :
        """ 
        The string representation of the attributes is, right now, somewhat
        arbitrarily defined as to make the bliss attribute unit tests happy:
        we ignore unset values and extended values.  
        """
        # FIXME: make serialization somewhat more meaningful

        # make sure interface is ready to use
        d = self.attributes_t_init_ ()

        tmp = {}

        for key in sorted(d['attributes_'].iterkeys()) :
            if not d['attributes_'][key]['extended'] and \
                   d['attributes_'][key]['exists']   and \
                   d['attributes_'][key]['value']    :
                tmp[key] = d['attributes_'][key]['value']

        return str (tmp)
            

   
   
################################################################################


