#!/usr/bin/env python
# -*-coding:utf-8 -*-
import argparse
import re
from ExtractMacros import ExtractMacros

#-----------------------------------------------------------------------------------
#This class is used for changing a node's status by modifying its description file.
#Functions:
#  1. detect_status(macro, status): check whether a macro's value matches the giving status.
#  2. change_to_noop(): change a normal node to noop status
#  3. reverse_noop():   reverse a noop node to normal status
#Robin Apirl 14,2017
#-----------------------------------------------------------------------------------


class ModifyNode:
    def __init__(self,nodename):
        self.filename = nodename

    def detect_status(self,macro,status):
        # check whether a macro's value matches the giving status.
        if self.filename == None:
            print 'No target'
            return 1
        em = ExtractMacros(self.filename)
        temp = em.extract(macro)
        #every value is warp by a list
        if temp.has_key(macro):
            if [status] == temp[macro]:
                return 0
            else:
                return 1
        else:
            return 1

    def change_to_noop(self):
        '''
        change a Dag node to noop
        :return:
        '''
        if self.filename == None:
            print 'No target'
            return 1
        str = 'noop_job=True\n'
        with open("./"+self.filename,'rt') as file:
            list = file.readlines()
            index = 0
            for _ in list:
                line = _.strip().replace(' ', '')
                if 'noop_job=True' in line:
                    print 'The node is already "no op"'
                    break
                #insert noop_job  = true before carco “queue“
                if line.find("ueue") != -1:
                    index = list.index(_)
            if index !=0:
                list.insert(index,str)
                print 'Change %s to noop successfully' % self.filename
            else:
                print 'No queue'

        with open("./"+self.filename,'wt') as file:
            return file.writelines(list)

    def reverse_noop(self):
        '''
            reverse a noop nodes to  a Dag node to normal status.
            :retun 0
            '''
        if self.filename == None:
            print 'No target'
            return 1
        str = 'noop_job=True\n'
        with open("./" + self.filename, 'rt') as file:
            list = file.readlines()
            index = 0
            for _ in list:
                line = _.strip().replace(' ', '')
                if 'noop_job=True' in line:
                    list.remove(_)
                    index+=1
                else:
                    continue
            print 'Change to normal, del noop: ',index


        with open("./" + self.filename, 'wt') as file:
            return file.writelines(list)


if __name__ == '__main__':

    mn = ModifyNode('./demofiles/test.py')
    #print mn.detect_status('universe','vanilla')
    #mn.change_to_noop()
    mn.reverse_noop()