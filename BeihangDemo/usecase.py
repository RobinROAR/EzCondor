#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#08.11  2017
import sys
from DAGAPI.Dag import *
import shutil


def build_dag(maxnum):
    if os.path.exists('./task'):
        shutil.rmtree('./task')
        os.mkdir('./task')
        os.mkdir('./task/log')
    else:
        os.mkdir('./task')

    os.system('cp ./task_template/* ./task')
    os.system('cp -r DAGAPI task/')
    dag = DAG('buaa.dag')

    #generate the name of nodes,submitfiles, inputs, outputs, and out,error
    nodes = []
    submitfiles = []
    inputs = []
    #outputs = []
    stdouts = []
    errors = []
    for i in xrange(1,maxnum+1):
        nodes.append('node_'+str(i))
        submitfiles.append('node_'+str(i)+'.sub')
        inputs.append('input_data_'+str(i))
        #outputs.append('output_data_'+str(i))
        stdouts.append('node_'+str(i)+'.out')
        errors.append('node_' + str(i) + '.error')
    #final result
    inputs.append('final_output')

    #create compute nodes
    job_dict = {}
    for i in xrange(maxnum):
    #for node,sub,input,output,stdout,error in zip(nodes,submitfiles,inputs,outputs,stdouts,errors):
        job_dict[nodes[i]] = Job(name = submitfiles[i],exe = './function.sh',path = './task/')
        job_dict[nodes[i]].add_commands(should_transfer_files='YES', when_to_transfer_output='ON_EXIT',
                                     transfer_input_files = inputs[i], transfer_output_files=inputs[i+1], output ='log/'+stdouts[i],
                                    error = 'log/'+errors[i],Log = 'log/'+nodes[i]+'.log', Arguments = inputs[i]+' '+inputs[i+1])


    #Generate Nodes
    names = locals()
    for i in xrange(1,maxnum+1):
        names['n'+str(i)] = Node(nodes[i-1])
        names['n'+str(i)].job = job_dict[nodes[i-1]]
        # Specify Script
        s_pre = Script('pre.py','temp', 'PRE', all=0, argu = names['n'+str(i)].job._name)
        s_post = Script('post.py', 'temp1', 'POST', all=0, argu = names['n'+str(i)].job._name)
        names['n'+str(i)].scripts = [s_pre,s_post]
        dag.add_node(names['n'+str(i)])
    #Generate Edges
    for j in xrange(1,maxnum):
        names['e'+str(j)] = Edge([nodes[j-1]],[nodes[j]])
        dag.add_edge(names['e'+str(j)])
    return dag

dag = build_dag(5)
dag.write2file('./task/')
