#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#08.11  2017
import sys

class Apple(object):
    def __init__(self):
        self._name = 'abc'
        self._job =  'idle'

    @property
    def name(self):
        return self._name

    def print11(self):
        print self.name

a = Apple()
a.print11()







