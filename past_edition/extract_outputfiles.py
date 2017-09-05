#!/usr/bin/env python
# -*-coding:utf-8 -*-
#wrap arguments
import argparse
#regular expression
import re

#This script is used to extract out file from submit file.
#-Robin Apirl 6,2017
#--------------------------------------------------------------------------------


args = None
#args= 'test.py'

def handle_process(line, queue):
    '''
    handle the Input   = in.$(Process)
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
def extract_rm(line, regulation,queue):
    # Match target regulation:
    result = []
    m1 = re.match(regulation, line)
    if m1:
        #split every element
        temp = line.split('=')[1].split(',')
        for i in temp:
            if handle_process(i, queue):
                result.extend(handle_process(i, queue))

            else:
                result.append(i)

        return result
    else:
        return 0


#def main(_):
def main(_):
    if args.filename == None:
    #if args == None:
        print 'Can\'t find the target file! Please check again.'
        return 1
    #a list storing  result
    #intialize queue
    queue = 0
    with open("./"+args.filename,'rt') as file:
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
            if m3 and m3.group(2):
                queue = int(m3.group(2))
            else:
                queue = 1
        if queue == 0:
            print "ERROR: No Queue"


        # Extract the input_sandle_box
        output = {}
        for _ in list:
            line = _.strip().replace(' ','')
            #omit comment
            if re.match(r'^[#]',line):
                continue
            if extract_rm(line, r'(transfer_output_files=)(.*)', queue):
                output['transfer_output_files'] = extract_rm(line, r'(transfer_output_files=)(.*)', queue)
                continue


        print output



if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage = './noop.py --help')
    parser.add_argument('filename', type = str, default = None, help = 'the filename of *.sub to add noop flag')
    args = parser.parse_args()
    main(None)

