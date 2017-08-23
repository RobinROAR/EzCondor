#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#08.11  2017
import sys
sys.path.append('../')
from DAGAPI.Dag import *
import shutil


def build_dag(maxnum):
    if os.path.exists('./task'):
        shutil.rmtree('./task')
        os.mkdir('./task')
    else:
        os.mkdir('./task')
    dag = DAG('buaa.dag')
    #create compute job
    job_compute = Job(name = 'task/compute',exe = './function.sh')
    job_compute.add_commands(should_transfer_files='YES', when_to_transfer_output='ON_EXIT', transfer_input_files = './data', transfer_output_files='./data' )
    #Specify Script
    s_pre = Script('pre.py', 'all', 'PRE',all = 1)
    s_post = Script('post.py', 'all', 'POST',all = 1)
    #generate nodes and edges
    names = locals()
    for i in xrange(1,maxnum+1):
        names['n'+str(i)] = Node('compute'+str(i))
        names['n' + str(i)].job = job_compute
        names['n' + str(i)].scripts = [s_pre,s_post]
        dag.add_node(names['n'+str(i)])
    for j in xrange(1,maxnum):
        names['e'+str(j)] = Edge(['compute'+str(j)],['compute'+str(j+1)])
        dag.add_edge(names['e'+str(j)])
    return dag


dag = build_dag(5)
dag.write2file('./task/')
