#!/usr/bin/python
# -*-coding:utf-8 -*-
#Robin@chtc.wisc.edu
#08.12  2017
#revise 08.25 2017
import sys
import os
import cPickle
from DAGAPI.ExtractMacros import ExtractMacros
from DAGAPI.ModifyNode import ModifyNode
import argparse

Flags = None

def main():
    #Get the path of submitfile
    path = Flags.submit
    #Get the name of output file
    em = ExtractMacros(path)
    output = em.extract('transfer_output_files')['transfer_output_files'][0]
    #Update current Y
    with open(output,"r") as f:
        y = int(f.readline())

    with open(r'loopfile','r') as f:
        temp = cPickle.load(f)

    temp['currentY'] = y

    with open(r'loopfile','w') as f:
       print 'currentY:  ',y
       cPickle.dump(temp, f)



p = argparse.ArgumentParser()
p.add_argument('submit')
Flags = p.parse_args()
main()

