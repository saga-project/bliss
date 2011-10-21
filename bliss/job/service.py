#!/usr/bin/env python

class Service:
    '''Represents a SAGA job service as defined in GFD.90'''
    def __init__(self, url=None):
        '''Construct a new job service object'''

    def create_job(self, job_description):
        '''Create a new job object from the given job description'''

    def get_job(self, job_id):
        '''Return the job object from the given job id'''

    def list(self):
        '''List all jobs known or managed by this service'''

