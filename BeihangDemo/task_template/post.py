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
import htcondor

Flags = None

def main():
    #Get the path of submitfile
    path = Flags.submit
    #Get the name of output file,logfile
    em = ExtractMacros(path)

    #Get the macro value
    output = em.extract('transfer_output_files')
    if output.has_key('transfer_output_files'):
        if len(output['transfer_output_files'])!=0:
            output = em.extract('transfer_output_files')['transfer_output_files'][0]
    else:
        output= None

    log = em.extract('Log')
    if log.has_key('Log'):
        if len(log['Log'])!=0:
            log = em.extract('Log')['Log'][0]
    else:
        log= None

    if (output != None) and os.path.exists(output) :
        #读取当前的y值
        with open(output,"r") as f:
            y = int(f.readline())
        #analyse log file
        m = 0
        if log != None:
            iter = htcondor.read_events(open(log))
            #read the memory usage
            for i in iter:
                if i['MyType']=='JobImageSizeEvent':
                    m = i['MemoryUsage']

        #更新loopfile
        with open(r'loopfile','r') as f:
            temp = cPickle.load(f)
        #Update the current y
        temp['currentY'] = y
        #Update the list of histrical y
        temp['yhistory'].append(y)
        #Update the number of loops:
        temp['nloops']+=1
        #update the memory usage
        temp['mems']+=m


        with open(r'loopfile','w') as f:
           print 'currentY:  ',y
           cPickle.dump(temp, f)
    else:
        print 'before is a noop job'



p = argparse.ArgumentParser()
p.add_argument('submit')
Flags = p.parse_args()
main()

