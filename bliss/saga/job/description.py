#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object
from bliss.saga.attributes import AttributeInterface
from bliss.saga.url import Url

class Description(Object, AttributeInterface):
    '''Loosely represents a SAGA job description as defined in GFD.90'''

    __slots__ = {}
 
    def __init__(self):
        '''Constructor - create an empty job description.'''
        Object.__init__(self, Object.JobDescription)
        AttributeInterface.__init__(self)

        self._attributes['Arguments']         = {'value':[], 'type':'V', 'access':'RW'} 
        self._attributes['Environment']       = {'value':{}, 'type':'V', 'access':'RW'}
        self._attributes['Project']           = {'value':[], 'type':'V', 'access':'RW'}
        self._attributes['Executable']        = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Output']            = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Error']             = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Queue']             = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['SPMDVariation']     = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['TotalCPUCount']     = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['NumberOfProcesses'] = {'value':"", 'type':'S', 'access':'RW'}

    @property
    def executable(self):
        'The job executable.'
        return self.get_attribute('Executable')
    @executable.setter
    def executable(self, val):
        self.set_vector_attribute('Executable', val)

    @property
    def arguments(self):
        'The arguments to pass to the job executable.'
        return self.get_vector_attribute('Arguments')
    @arguments.setter
    def arguments(self, val):
        self.set_vector_attribute('Arguments', val)

    @property
    def environment(self):
        'The environment variables to set in the job execution context.'
        return self.get_vector_attribute('Environment')
    @environment.setter
    def environment(self, val):
        self.set_vector_attribute('Environment', val)

    @property
    def output(self):
        'The file in which the job\'s stdout stream will be captured.'
        return self.get_attribute('Output')
    @output.setter
    def output(self, val):
        self.set_attribute('Output', val)

    @property
    def error(self):
        'The file in which the job\'s stderr stream will be captured.'
        return self.get_attribute('Error')
    @output.setter
    def error(self, val):
        self.set_attribute('Error', val)

    @property
    def project(self):
        'The name of one or more allocations to use for service unit credits.'
        return self.get_vector_attribute('Project')
    @project.setter
    def project(self, val):
        self.set_vector_attribute('Project', val)

    @property
    def queue(self):
        'The job queue to put this job into.'
        return self.get_attribute('Queue')
    @queue.setter
    def queue(self, val):
        self.set_attribute('Queue', val)

    @property
    def spmd_variation(self):
        'The \'SPMD variation\' to use for the job (MPI or Single)'
        return self.get_attribute('SPMDVariation')
    @spmd_variation.setter
    def spmd_variation(self, val):
        self.set_attribute('SPMDVariation', val)

    @property
    def total_cpu_count(self):
        'Number of CPUs to allocate for the job.'
        return self.get_attribute('TotalCPUCount')
    @total_cpu_count.setter
    def total_cpu_count(self, val):
        self.set_attribute('TotalCPUCount', val)

    @property
    def number_of_processes(self):
        'Number of instances of the job executable to start.'
        return self.get_attribute('NumberOfProcesses')
    @number_of_processes.setter
    def number_of_processes(self, val):
        self.set_attribute('NumberOfProcesses', val)
