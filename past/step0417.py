#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os
import argparse
from ExtractMacros import ExtractMacros
from ModifyNode import ModifyNode


#THis script is used as a PRE SCRIPT :
#1. Extract the value of macros "transfer_output_files"
#2. Check the existence of these files
#3. if all files exist, turn these files in to noop file
#-Robin Apirl 17,2017
#--------------------------------------------------------------------------------

args = None

def main(_):
    filename = args.filename
    flag = 0
    ex = ExtractMacros(filename)
    files = ex.extract('transfer_output_files')['transfer_output_files']
    for _ in files:
        if os.path.exists('./'+_) != True:
            flag = 1
    if flag == 0:
        mf = ModifyNode(filename)
        mf.change_to_noop()
    else:
        print 'Not all output exist, no change'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='./step0417.py --help')
    parser.add_argument('filename', type=str, default=None, help='check the filename of *.sub')
    args = parser.parse_args()
    main(None)