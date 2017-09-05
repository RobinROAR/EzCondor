#!/usr/bin/python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#08.11  2017
#revise 08.25
import sys
import os
import cPickle
from DAGAPI.ExtractMacros import ExtractMacros
from DAGAPI.ModifyNode import ModifyNode
import argparse

Flags = None

def main():
    # if this is the first node
    if os.path.exists('loopfile'):
        pass
    else:
        #initialize
        temp = {'currentY': 0}
        with open(r'loopfile','w+') as f:
            cPickle.dump(temp,f)
            print 'create loopfile'

    if os.path.exists(Flags.submit):
        #get the path of submitfile
        path = Flags.submit
        #jugement
        with open('loopfile','r') as f:
            temp = cPickle.load(f)
        if temp['currentY'] > 5:
            mn = ModifyNode(path)
            mn.change_to_noop()
            print "change to noop"
        else:
            print 'no change'
    else:
        print 'No target submit file!'

p = argparse.ArgumentParser()
p.add_argument('submit')
Flags = p.parse_args()
main()