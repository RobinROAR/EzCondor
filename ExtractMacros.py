#!/usr/bin/env python
# -*-coding:utf-8 -*-
#wrap arguments
import argparse
#regular expression
import re

#A class for extract the value of macros "
#-Robin Apirl 14,2017
#--------------------------------------------------------------------------------


class ExtractMacros:
    '''
    a class for extracting the values of target macros
    '''
    def __init__(self,filename):
        self.filename = filename


    def handle_process(self,line, queue):
        '''
        handle the queue input or out put  = in.$(Process)
        :param line:
        :param queue:
        :param prefix:
        :return:
        '''
        if line == None:
            print 'No input line'
            return 0
        if queue == 1 :
            return 0
        else:
            result = []
            m = re.match(r'(.*)([$][(]Process[)])(.*)',line)
            if m:
                for _ in range(queue):
                    result.append(line.replace('$(Process)',str(_)))
                return result
            else:
                return 0
    def extract_rm(self,line,regulation,queue):
        # Match target regulation, add all its value in a list and return
        result = []
        m1 = re.match(regulation, line)
        if m1:
            #split every element
            temp = line.split('=')[1].split(',')
            for i in temp:
                if self.handle_process(i, queue):
                    result.extend(self.handle_process(i, queue))

                else:
                    result.append(i)

            return result
        else:
            return 0


    def extract(self, *args):
        '''
        main function for extracting the content of target macros
            1. accept more than one macros
            2. the result is a dict which its keys are macros and values are the content of macros.
        :return: a dict include target macros
        '''
        if self.filename == None:
        #if args == None:
            print 'Can\'t find the target file! Please check again.'
            return 1
        #a list storing  result
        #intialize queue
        queue = 0
        with open("./"+self.filename,'rt') as file:
            list = file.readlines()
            #Get basic information
            for _ in list:
                line = _.strip().replace(' ', '')
                # omit comment
                if re.match(r'^[#]', line):
                    continue
                # handle with subfile = 'job.prepare.submit'
                # get queue value
                m3 = re.match(r'(queue)(\d+)', line)
                if m3:
                    if len(m3.groups()) == 2:
                        queue = int(m3.group(2))
                    else:
                        queue = 1
            if queue == 0:
                print "ERROR: No Queue"
            # Extract the input_sandle_box
            output = {}

            for m in args:
                flag = 0
                for _ in list:
                    line = _.strip().replace(' ','')
                    #omit comment
                    if re.match(r'^[#]',line):
                        continue
                    #check target macro
                    if self.extract_rm(line, r'(%s=)(.*)' % m, queue):
                        output[m] = self.extract_rm(line, r'(%s=)(.*)' % m, queue)
                        flag = 1
                        continue
                if flag == 0:
                    output[m] = []
                    print "%s has no marco: %s" % (self.filename,m)
                    continue


            return output



if __name__ == '__main__':

    path = './test.py'
    em = ExtractMacros(path)
    print em.extract('input','transfer_output_files')