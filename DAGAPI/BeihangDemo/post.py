#!/usr/bin/env python
# -*-coding:utf-8 -*-
#Robin@chtc.wisc.edu
#08.12  2017
import sys
import cPickle
sys.path.append('../')


with open('./task/data',"r") as f:
    y = int(f.readline())

with open(r'./task/loopfile','r') as f:
    temp = cPickle.load(f)

temp['currentY'] = y

with open(r'./task/loopfile','w') as f:
    print 'currentY ： ',y
    cPickle.dump(temp, f)


