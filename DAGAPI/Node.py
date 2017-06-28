#!/usr/bin/env python
# -*-coding:utf-8 -*-
##RoBinZ @ chtc.wisc.edu
#06.27 2017
#The Node class, The nodes in a DAG are usually called the 'JOB' in HTCondor DAG file.


class Node:
    #define a Node class
    def __init__(self,name, path = ''):
        self.name = name
        self.path = path

    def set_path(self,path):
        self.path = path
