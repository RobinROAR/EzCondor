#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os
import argparse
import re
from ExtractMacros import ExtractMacros
from ModifyNode import ModifyNode


#THis script is used as a read a dag description file to dataflow model:
# dag file example:
# File name: diamond.dag
    # JOB  A  A.condor
    # JOB  B  B.condor
    # JOB  C  C.condor
    # JOB  D  D.condor
    # PARENT A CHILD B C
    # PARENT B C CHILD D
# a dataflow model:
#   [{input: ..., transform: name.  output: ....}...]
#--------------------------------------------------------------------------------

args = None

def read_jobs(filename):
    '''
    read the dag file
    :param filename:
    :return:
    '''
    filename = filename
    with open("./" + filename, 'rt') as file:
        list = file.readlines()
        # Get basic information
        jobs = []
        for _ in list:
            #remove blank in top and tail
            line = _.strip()
            # extract the job: JOB  A  A.condor
            m = re.match(r'(JOB)(\s+)(\S+)(\s+)(\S+)', line)
            # group(3) is job name, group(5) is job file
            if m:
                if len(m.groups()) == 5 :
                    temp = {}
                    temp[m.group(3)]=m.group(5)
                    jobs.append(temp)
                else:
                    continue
        return jobs

def convert_dataflow(jobs):
    dataflow = []
    for j in jobs:
        temp = {'Input':[],'Output':[]}
        #get filepath
        name = j.items()[0][0]
        path = j.items()[0][1]
        em = ExtractMacros(path)
        result = em.extract('input','transfer_input_files','executable','transfer_output_files')
        # make input
        if result.has_key('input'):
            temp['Input'] += result['input']
        if result.has_key('transfer_input_files'):
            temp['Input'] += result['transfer_input_files']
        if result.has_key('executable'):
            temp['Input'] += result['executable']
        temp['T'] = name
        if result.has_key('transfer_output_files'):
            temp['Output'] = result['transfer_output_files']
        dataflow.append(temp)
    return dataflow



# def main(_):
#     read_jobs(args.filename)

if __name__ == '__main__':

    print convert_dataflow(read_jobs('demofiles/t.py'))

    # parser = argparse.ArgumentParser(usage='./step0418.py --help')
    # parser.add_argument('filename', type=str, default=None, help='check the filename of *.sub')
    # args = parser.parse_args()
    # main(None)