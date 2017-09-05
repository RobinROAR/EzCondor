#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RobinZ @ chtc.wisc.edu
#06.27 2017
#The DAG class
#- currently no support data stork

from Node import Node
from Job import Job
from Edge import Edge
from Script import Script
import os


class DAG(object):
    #define a DAG class
    def __init__(self,name = 'new_dag'):
        self._name = name
        self._author = 'anomymous'
        self._nodes = []
        self._edges = []

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if name == '':
            raise ValueError('a name should not be empty')
        else:
            self._name = name
    @property
    def path(self):
        return os.path.abspath(self._name)

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        if nodes == []:
            raise ValueError('nodes should not be empty')
        else:
            self._nodes = nodes

    # all verifications rule are in the add* functions.
    def add_node(self,node):
         '''
         add a single node to dag
         :param node:
         :return:
         '''
         #firstly check weather a node has the necessary element
         if node.job != None:
            self.nodes.append(node)

    @property
    def edges(self):
        return self._edges

    def add_edge(self,edge):
        '''
        add a single edge to dag
        :return:
        '''

        nnames = []
        for _ in self.nodes:
            nnames.append(_.name)

        if ( set(edge.children).issubset(set(nnames)) ) and ( set(edge.parents).issubset(nnames) ):
            self._edges.append(edge)
        else:
            print 'Edge error!'
            print set(edge.children),set(nnames)


    def write_nodes(self):
        '''
        covert the nodes in to lines in list
        :return: list
        '''
        result = []
        cnt = 0
        for _ in self.nodes:
            if _.job != None:
                strr = 'JOB '+str(_.name)+' '+ _.job._name+'\n'
                result.append(strr)
                cnt+=1
        print 'prepare to write {0} nodes'.format(cnt)
        return result


    def write_scripts(self):
        # example: SCRIPT PRE  B  pre.csh $JOB .gz
        result = []
        cnt = 0
        for _ in self._nodes:
            if len(_.scripts) != 0:
                for i in _.scripts:
                    # allnodes case
                    if i._all == 1:
                        if i.position in ['PRE', 'pre', 'Pre']:
                            strr = 'SCRIPT PRE ' + 'ALL_NODES' + ' ' + i.path + ' ' + i.argu + '\n'
                        else:
                            strr = 'SCRIPT POST ' + 'ALL_NODES' + ' ' + i.path + ' ' + i.argu + '\n'
                        result.append(strr)
                    else:
                    # distinguish pre or post
                        if i.position in ['PRE','pre','Pre']:
                            strr = 'SCRIPT PRE '+_.name + ' ' + i.path + ' ' + i.argu + '\n'
                        else:
                            strr = 'SCRIPT POST ' + _.name + ' ' + i.path + ' ' + i.argu + '\n'

                        result.append(strr)
                    cnt += 1
        #eliminate repeated lines
        result = list(set(result))
        print 'prepare to write {0} scripts'.format(cnt)
        return result

    def write_edges(self):
        #example PARENT A CHILD B C
        result = []
        cnt = 0
        for _ in self.edges:
            strr = 'PARENT ' + ' '.join(_.parents) + ' '+'CHILD '+' '.join(_.children)+'\n'
            result.append(strr)
            cnt += 1
        print 'prepare write {0} edges'.format(cnt)
        return result



    def write2file(self,tdir):
        strr = tdir
        strr+= str(self._name)
        with open(strr,"w+") as file:
            nodes = self.write_nodes()
            scripts = self.write_scripts()
            edges = self.write_edges()
            file.writelines(nodes+scripts+edges)
        print 'Dag file: {0}  is written. '.format(str(self._name))




if __name__ == '__main__':
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
    s1 = Script('a.sh','j1','PRE')
    s2 = Script('a.sh','j1','POST', argu = '$JOB .gz')


    node1 = Node('A')
    node1.job = j1
    node1.scripts = [s1]
    node2 = Node('B')
    node2.job = j1
    node2.scripts = [s2]


    node3 = Node('C')
    node4 = Node('D')


    e1 = Edge(['A'],['B','C'])
    e2 = Edge(['A'],['B'])

    for _ in [node1,node2,node3,node4]:
        dag.add_node(_)

    for _ in [e1,e2]:
        dag.add_edge(_)

    dag.write2file('./')

