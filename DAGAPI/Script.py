#!/usr/bin/env python
# -*-coding:utf-8 -*-
##Robin.Z @ chtc.wisc.edu
#06.27 2017
#revised in July 14, 2017
#The Script class.
import os

class Script(object):
    #define a Script class,a Script is belonging to a job
    def __init__(self,name,job,position,argu = '',all = 0):
        self._job = job
        self._position = position
        self._name = name
        self._argu = argu
        self._all = all

    @property
    def job(self):
        return self._job
    @job.setter
    def job(self,job):
        if job == None:
            raise ValueError('a script must have a job to belong !')
        else:
            self._job = job


    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if position == None or position not in ('PRE','pre','Pre','post','Post' 'POST'):
            raise ValueError('The position must be ’PRE‘ or ’POST‘ !')
        else:
            self._position = position

    @property
    # def path(self):
    #     if os.path.exists(self._name):
    #         return os.path.abspath(self._name)
    #     else:
    #         raise ValueError('The script is not existing !')
    def path(self):
        return self._name


    @property
    def argu(self):
        return self._argu
    @argu.setter
    def argu(self,argu):
        self._argu = argu