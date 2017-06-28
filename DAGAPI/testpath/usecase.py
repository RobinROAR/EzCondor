#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#07.18  2017
import sys
sys.path.append('../')

from DAGAPI.Dag import *
from DAGAPI.Dag import DAG


import os
    # ------ File name: diamond.dag--------
    # JOB  A  A.condor
    # JOB  B  B.condor
    # JOB  C  C.condor
    # JOB  D  D.condor
    # SCRIPT PRE  B  pre.csh $JOB .gz
    # SCRIPT POST  C  pre.csh $JOB .gz
    # PARENT A CHILD B C
    # PARENT B C CHILD D

dag = DAG('diamond.dag')
#create jobs
j1 = Job('job1','a.sh')
j1.add_commands(should_transfer_files='YES',
                 when_to_transfer_output='ON_EXIT',
                 Arguments='in1 in2 out1', Queue = 3)
s1 = Script('a.sh','j1','PRE')
s2 = Script('a.sh','j1','POST', argu = '$JOB .gz')

j2 = Job('job2','a.sh')
j2.add_commands(should_transfer_files='No',
                when_to_transfer_output='all_time',
                Arguments='usa', Queue = 0)
s3 = Script('a.sh','j2','PRE')



node1 = Node('A')
node1.job = j1
node1.scripts = [s1,s2]
node2 = Node('B')
node2.job = j1
node2.scripts = [s2]


node3 = Node('C')
node3.job = j2
node3.scripts = [s3]
node4 = Node('D')
node4.job = j2


e1 = Edge(['A','D'],['B','C'])
e2 = Edge(['A'],['B'])

for _ in [node1,node2,node3,node4]:
    dag.add_node(_)

for _ in [e1,e2]:
    dag.add_edge(_)

dag.write2file('./')

