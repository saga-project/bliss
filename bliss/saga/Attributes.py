# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Exception import Exception as SAGAException
from bliss.saga.Error import Error as SAGAError


class AttributeInterface(object):
    '''
    Loosely defines the SAGA attribute interface as defined in GFD.90.

    The SAGA attribute interface behaves very similar to a hash table (or
    'dictionary' in python), with the main difference that attribute names and
    types are often (depending on the specific class providing that interface)
    pre-defined.  The values are usually simple strings, integers or floats, or
    lists of strings ('vector attributes').

    Since the attribute interface matches the semantics of python dictionaries
    so well, it is often mapped to the dictionary syntax, and is rendered as
    class variables.  Sometimes, for frequently used variables, classes also
    expose an explicit accessor method (see 'JobID' example below).

    The most prominent example of the attribute interface is the
    L{job.Description} class, which is used to describe a L{job.Job} to be
    submitted to a L{job.Service}.  Other uses of the interface are
    L{resource.StorageDescription}s, and the exposure of object attributes like
    L{job.Job}.JobID.


    Example::


        jd = saga::job::Description ()
        jd.set_attribute        ("Executable", "/usr/bin/blast")
        jd.set_vector_attribute ("Arguments", ["-i", "/data/in.dat"])

        js = saga.job.Service ()
        j  = js.create_job (jd);
        j.run ()

        print "job id: %s"  % j.get_attribute ("JobID")


    This example is equivalent to::
   

        jd = saga::job::Description ()
        jd.["Executable"] = "/usr/bin/blast"
        jd.["Arguments"]  = ["-i", "/data/in.dat"]

        js = saga.job.Service ()
        j  = js.create_job (jd);
        j.run ()

        print "job id: %s"  % j.["JobID"]
        print "job id: %s"  % j.get_job_id()

    
    '''
   
    ######################################################################
    # 
    def __init__(self):
        '''Constructor'''
        self._attributes = dict()

    ######################################################################
    # PROTECTED
    def _register_ro_attribute(self, name, accessor): 
        '''Register a read only attribute'''
        self._attributes[name] = {'type':'S', 'access':'RO', 'accessor':accessor}

    ######################################################################
    # PROTECTED
    def _register_ro_vec_attribute(self, name, accessor):
        '''Register a read only vector attribute'''
        self._attributes[name] = {'type':'V', 'access':'RO', 'accessor':accessor}

    ######################################################################
    # PROTECTED
    def _register_rw_attribute(self, name, accessor):
        '''Register a read/write attribute'''
        self._attributes[name] = {'type':'S', 'access':'RW', 'accessor':accessor}

    ######################################################################
    # PROTECTED
    def _register_rw_vec_attribute(self, name, accessor):
        '''Register a read/write vector attribute'''
        self._attributes[name] = {'type':'V', 'access':'RW', 'accessor':accessor}

    ######################################################################
    #
    def _valid_attribute_key(self, key):
        '''Check if an attribute is defined as valid.
        '''
        if key in self._attributes:
            return True 
        return False

    ######################################################################
    #
    def _attribute_defined(self, name):
        if key in self._attributes:
            if self._attributes['name']['accessor'] is not None:
                return True
        else:
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' is not defined for this object." % (name))
        return False

    ######################################################################
    #
    def remove_attribute(self, key):
        '''Remove the attribute.

        Example::


          d = saga.Attribute ()
          d.set_attribute ("key", "val")
          assert ( d.has_attribute ("key") )

          # remove:
          d.remove_attribute ("key")
          assert ( not d.has_attribute ("key"))



        This is semantically equivalent to::


          d = dict ()
          d["key"] = "val"
          assert ("key" in d )

          # remove:
          d["key"] = None
          assert ("key" in d )


        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' doesn't exist." % (key))
        if self.attribute_is_readonly(key):
            raise SAGAException(SAGAError.PermissionDenied, 
                  "Attribute '%s' is a read-only attribute." % (key))
        return self._attributes[key]['accessor'].fset(self, None) 



    ######################################################################
    #
    def get_attribute(self, key):
        '''Return the value of a scalar attribute.

        Example::


          d = saga.Attribute ()
          d.set_attribute ("key", "val")

          # get
          val = d.get_attribute ("key") == "val" )
          assert ( val == "val" )



        This is semantically equivalent to::


          d = dict ()
          d["key"] = "val"

          # get
          val = d["key"]
          assert ( val == "val" )


        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' doesn't exist." % (key))
        if self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute '%s' is a vector attribute." % (key))
        return self._attributes[key]['accessor'].fget(self) 


    ######################################################################
    #    
    def set_attribute(self, key, value):
        '''Set the value of a scalar attribute.

        Example::


          d = saga.Attribute ()

          # set
          d.set_attribute ("key", "val")

          assert ( d.has_attribute ("key") )
          assert ( d.get_attribute ("key") == "val" )



        This is semantically equivalent to::


          d = dict ()

          # set
          d["key"] = "val"

          assert ( "key" in d )
          assert ( d["key" == "val" )


        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' is not defined for this object." % (key))
        if self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute '%s' is a vector attribute." % (key))
        if self.attribute_is_readonly(key):
            raise SAGAException(SAGAError.PermissionDenied, 
                  "Attribute '%s' is a read-only attribute." % (key))
        self._attributes[key]['accessor'].fset(self, value) 

    ######################################################################
    #
    def get_vector_attribute(self, key):
        '''Return the value of a vector attribute.
        '''
        if not self.attribute_exists(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' doesn't exist." % (key))
        if not self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute '%s' is a scalar attribute." % (key))
        return self._attributes[key]['accessor'].fget(self) 
 
    ######################################################################
    #
    def set_vector_attribute(self, key, value):
        '''Set the value of a vector attribute.
        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' doesn't exist." % (key))
        if not self.attribute_is_vector(key):
            raise SAGAException(SAGAError.IncorrectState, 
                  "Attribute '%s' is a scalar attribute." % (key))
        if self.attribute_is_readonly(key):
            raise SAGAException(SAGAError.PermissionDenied, 
                  "Attribute '%s' is a read-only attribute." % (key))
        self._attributes[key]['accessor'].fset(self, value) 

    ######################################################################
    #
    def attribute_exists(self, key):
        '''Check if an attribute exists.

        Example::


          d = saga.Attribute ()
          d.set_attribute ("key", "val")

          # check
          assert ( d.attribute_exists ("key") )



        This is semantically equivalent to::


          d = dict ()
          d["key"] = "val"

          # check
          assert ( "key" in d )


        '''
        if key in self._attributes:
            if self._attributes[key]['accessor'].fget(self) is not None: 
                return True 
        return False

    ######################################################################
    #
    def attribute_is_writeable(self, key):
        '''Check if an attribute is writable.

        Example::


          d = saga.Attribute ()

          # check
          if d.attribute_is_writable ("key") :
            d.set_attribute ("key", "val")
          fi



        There is no semantic equivalent in python's dicts., really -- dicts
        allow to write to any key.  The dict implementation in bliss will still
        fail though on ReadOnly keys, and will raise a 'PermissionDenied'
        exception::


          d = dict ()

          try : 
            d["key"] = "val" 
          except Exception as e :
            print "no no no!"


        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute %s doesn't exist." % (key))

        return not self.attribute_is_readonly(key)

    ######################################################################
    #
    def attribute_is_readonly(self, key):
        '''Check if an attribute is read-only.

        Example::


          d = saga.Attribute ()

          # check
          if d.attribute_is_writable ("key") :
            d.set_attribute ("key", "val")
          fi



        There is no semantic equivalent in python's dicts., really -- dicts
        allow to write to any key.  The dict implementation in bliss will still
        fail though on ReadOnly keys, and will raise a 'PermissionDenied'
        exception::


          d = dict ()

          try : 
            d["key"] = "val" 
          except Exception as e :
            print "no no no!"


        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute %s doesn't exist." % (key))

        if (self._attributes[key]['access']) == 'RW':
            return False
        else:
            return True

    ######################################################################
    #
    def attribute_is_vector(self, key):
        '''Check if an attribute is a vector.

        Python dicts don't  distinguish between vector and scalar values, but
        the SAGA attribute interface in fact cares -- this is supposed to catch
        incorrect attribute type setting as early as possible.

        Example::


          d = saga.Attribute ()

          # check
          if d.attribute_is_vector ("Arguments") :
            d.set_attribute ("Arguments", ["-i", "/data/in.dat"])
          fi



        As there is no semantic equivalent in python's dicts, the Bliss
        implementation will throw an exception on the wrong setting::


          d = dict ()

          try : 
            d["Arguments"] = "scalar_value" 
          except Exception as e :
            print "no no no!  I want lists!"


        '''
        if not self._valid_attribute_key(key):
            raise SAGAException(SAGAError.DoesNotExist, 
                  "Attribute '%s' doesn't exist." % (key))
 
        if (self._attributes[key]['type']) == 'V':
            return True
        else:
            return False

    ######################################################################
    #
    def list_attributes(self): 
        '''List all defined attributes.

        This method simply lists the names of all attributes currently defined.
        Note that this method also lists predefined attributes, even if those
        have no defined value, yet.  For example, the attribute 'JobID' is
        always known on a job -- even if the specific job instance does not yet
        have a defined job ID.

        Example::


          d = saga.Attribute ()

          # list
          print "keys: %s"  %  d.list_attributes ()



        As there is no semantic equivalent in python's dicts, the Bliss
        implementation will throw an exception on the wrong setting::


          d = dict ()

          # list
          print "keys: %s"  %  d.keys () # FIXME


        '''
        list = []
        for att in self._attributes:
            if self.attribute_exists(att):
                list.append(att)
        return list
            
