#!/usr/bin/env python
# -*-coding:utf-8 -*-
import argparse

#subfile = 'job.prepare.submit'


args = None


def main(_):
    if args.filename == None:
        print 'No target'
        return 1
    str = 'noop_job = true\n'
    with open("./"+args.filename,'rt') as file:
        list = file.readlines()
        for _ in list:
            if _.find("queue") != -1:
                index = list.index(_)
        list.insert(index,str)

    with open("./"+args.filename,'wt') as file:
        file.writelines(list)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage = './noop.py --help')
    parser.add_argument('filename', type = str, default = None, help = 'the filename of *.sub to add noop flag')
    args = parser.parse_args()
    main(None)

