#!/usr/bin/env python
# -*-coding:utf-8 -*-
#----------------------------------
#This script is used as a common PRE SCRIPT to every node in a workflow, in order to change a node to noop or normal status under some roles as follows:
# RULE:
#  if a OP node:
#        if all input_sandbox files exist:
#               if all output_sandbox files exist:
#                     if the all output files are created lately than all input files:
#                               turn into NOOP
#                     else:
#                               no change
#               else:
#                     no change
#        else：
#             turn into NOOP
# if a NOOP node:
#       if all input—sandbox files exist:
#              if all output files exist:
#                        if all output files created lately than all input files:
#                                   no change
#                        else:
#                                   turn into OP
#              else:
#                       turn into OP
#      else:
#            no change

#-Robin Apirl 17,2017
# updated in May 03
#--------------------------------------------------------------------------------

import os
import argparse
import sys
sys.path.append("..")
from ExtractMacros import ExtractMacros
from ModifyNode import ModifyNode



args = None

def main(_):
    filename = args.filename
    flag = 0
    if filename == None:
        print 'No target'
        return 1
    #get the input and output sandbox
    ex = ExtractMacros(filename)
    #Processing output sandbox
    output = ex.extract('transfer_output_files')['transfer_output_files']
    oflag = 0
    otimes = []
    for _ in output:
        # check all output files exist
        if os.path.exists('./' + _) != True:
            oflag = 1
        else:
            # extract modified time
            oinfo = os.stat('./' + _)
            otimes.append(oinfo.st_mtime)
    if otimes != []:
        #the oldest output file
        otime = sorted(otimes)[0]
    else:
        otime = -1
    #Processing input sandbox
    input = ex.extract('input')['input']+ex.extract('transfer_input_files')['transfer_input_files']+ex.extract('executable')['executable']
    iflag = 0
    itimes = []
    for _ in input:
        # check all output files exist
        if os.path.exists('./' + _) != True:
            print _,' not exists'
            iflag = 1
        else:
            # extract modified time
            info = os.stat('./' + _)
            itimes.append(info.st_mtime)
    #Get the newest  time
    if itimes != []:
        #the newest input file
        itime = sorted(itimes)[-1]
    else:
        itime = -1

    #Rule
    mn = ModifyNode(filename)
    if mn.detect_status("noop_job","True"):
        # Current status is OP
        if iflag == 0:
            if oflag == 0:
                if  itime <  otime:
                    mn.change_to_noop()
                else:
                    print r'No change(new input file)'
            else:
                print r'No change (lack output file)'
        else:
            mn.change_to_noop()
    else:
        # current status is NOOP
        if iflag == 0:
            if oflag == 0:
                if itime < otime:
                    print 'No change(no new inputfile)'
                else:
                    mn.reverse_noop()
            else:
                mn.reverse_noop()
        else:
            print r'No change(lack input file)'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='./dag_makefile.py --help')
    parser.add_argument('filename', type=str, default=None, help='check the filename of *.sub')
    args = parser.parse_args()
    main(None)