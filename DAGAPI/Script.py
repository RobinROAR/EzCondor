#!/usr/bin/env python
# -*-coding:utf-8 -*-
##RoBinZ @ chtc.wisc.edu
#06.27 2017
#The Script class.
#Processing done before a job is submitted to HTCondor or Stork is called a PRE script. Processing done after a job completes its execution under HTCondor or Stork is called a POST script. A node in the DAG is comprised of the job together with PRE and/or POST scripts.


class Script:
    #define a Script class
    def __init__(self,script, pre = [], post = [], argu= ''):
        '''

        :param scritps:  the executable script
        :param pre:  a list of the names of parents nodes,[A,B]
        :param post: a list of the names of parents nodes,[A,B]
        :param arg:  the argument of scripts
        '''

        self.script = script
        self.pre = pre
        self.post = post
        self.argu = argu
    def set_pre(self,pre):
        self.pre.extend(pre)

    def set_post(self,post):
        self.post.extend(post)

    def set_argu(self,argu):
        self.argu = argu
