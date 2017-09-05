#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#08.11  2017
import sys
import os
import cPickle
sys.path.append('../')
from ExtractMacros import ExtractMacros
from ModifyNode import ModifyNode

# if this is the first node
if os.path.exists('./loopfile'):
    pass
else:
    #initialize
    temp = {'currentY': 0}
    with open(r'./task/loopfile','w+') as f:
        cPickle.dump(temp,f)



with open('./task/loopfile','r') as f:
    temp = cPickle.load(f)

if temp['currentY'] > 5:
    mn = ModifyNode('./task/compute.sub')
    mn.change_to_noop()
    print 'change to noop'

else:
    print 'no change'
    pass
