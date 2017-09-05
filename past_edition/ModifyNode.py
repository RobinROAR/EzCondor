#!/usr/bin/env python
# -*-coding:utf-8 -*-
import argparse
#A class for nodify node in dag
#-Robin Apirl 14,2017
#--------------------------------------------------------------------------------


class ModifyNode:
    def __init__(self,nodename):
        self.filename = nodename

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
                if 'noop_job=true' in line:
                    print 'The node is already "no op"'
                    break
                #insert noop_job  = true before queue
                if line.find("queue") != -1:
                    index = list.index(_)
            if index !=0:
                list.insert(index,str)
                print 'Change %s to noop successfully' % self.filename

        with open("./"+self.filename,'wt') as file:
            return file.writelines(list)

if __name__ == '__main__':

    mn = ModifyNode('test.py')
    mn.change_to_noop()