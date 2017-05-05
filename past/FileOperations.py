#!/usr/bin/env python
# -*-coding:utf-8 -*-
#wrap arguments
import argparse
import re

#A class for for file operations
#-Robin Apirl 17,2017
#--------------------------------------------------------------------------------


class FileOperations:
    '''
    a class for fileOperations
    '''
    def __init__(self,files):
        '''
        files: [file1,file2]
        :param files:
        '''
        self.files = files



if __name__ == '__main__':

    path = './test.py'
    em = ExtractMacros(path)
    print em.extract('input','transfer_out_files')