#!/usr/bin/env python
# -*-coding:utf-8 -*-
##Robin.Z @ chtc.wisc.edu
#06.27 2017
#revised in 07.14 2017
#The Node class, The nodes in a DAG are usually called the 'JOB' in HTCondor DAG file.
from Job import Job

class Node(object):
    #define a Node class
    def __init__(self,name,job = None, scripts=[]):
        self._name = name
        self._job = job
        self._scripts = scripts

    @property
    def name(self):
        return self._name

    @property
    def job(self):
        return self._job
    @job.setter
    def job(self,job):
        self._job = job

    @property
    def scripts(self):
        return self._scripts
    @scripts.setter
    def scripts(self,scripts):
        if scripts == []:
            raise ValueError('can not set a empty script !')
        else:
            self._scripts = scripts





