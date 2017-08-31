#!/usr/bin/env python
# -*-coding:utf-8 -*-
##Robin.Z @ chtc.wisc.edu
#07.18 2017
#The Job class.

import os

class Job(object):
    def __init__(self,exe,name='Default',argu = None,path = './'):
        self._name = name
        self._exe= exe
        self._argu = argu
        self._path = path
        self.create_file()
        self.write()

    @property
    def savepath(self):
        return self._path+str(self._name)



    @property
    def realpath(self):
        if os.path.exists(self.savepath):
            return os.path.abspath(self.savepath)
        else:
            raise ValueError('The script is not existing !')

    def create_file(self):
        #create the basic content for condor job description file
        ####################
        # Executable = foo
        # Universe = standard
        # Log = foo.log
        # Queue
        self._dict = {'Executable': self._exe, 'Universe':'vanilla','Log' :'log', 'Queue':0}
        self.write()

    def translate(self):
        #translate the dict to lines in submit file
        dict = self._dict
        lines = []
        que = 0
        for _ in dict:
            if _== 'Executable':
                lines.append('{0}  =  {1}'.format(_, dict[_])+'\n')
            elif _ == 'Universe':
                lines.append('{0}  =  {1}'.format(_, dict[_])+'\n')
            elif _ == 'Log':
                lines.append('{0}  =  {1}'.format(_, dict[_])+'\n')
            elif _ == ('Queue' or 'queue'):
                if dict[_] == 0 :
                    que  = 0
                else:
                    que = dict[_]
            else:
                lines.append('{0}  =  {1}'.format(_, dict[_]) + '\n')
        #processs command q
        if que == 0:
            lines.append('Queue  '+'\n')
        else:
            lines.append('Queue   {}'.format(que)+'\n')
        dict = None

        return lines


    def write(self):
        with open(self.savepath, "w+") as file:
            lines = self.translate()
            file.writelines(lines)
        print 'Submitfile '+self.savepath+ ' is written successfully!'


    def add_commands(self, **kwargs):
        '''This function will add commands to a Submit job vid input argument
            example : j1. add_commands(should_transfer_files = 'YES',
                                        when_to_transfer_output = 'ON_EXIT',
                                        Arguments   = 'in1 in2 out1'
            '''
        for name, value in kwargs.items():
            self._dict[name] = value
        self.write()


