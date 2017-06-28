#!/usr/bin/env python
# -*-coding:utf-8 -*-
#RoBinZ @ chtc.wisc.edu
#06.27 2017
#The DAG class
#- currently no support data stork

from Node import Node
from Edge import Edge
from Script import Script


class DAG:
    #define a DAG class
    def __init__(self,name = 'new_dag', nodes = [],edges = [],scripts = []):
        self.name = name
        self.author = 'anomymous'
        self.nodes = nodes
        self.edges = edges
        self.scripts = scripts

    def set_dagname(self,name):
        self.name = name

    def set_author(self,author):
        self.name = author

    # all verifications rule are in the add* functions.
    def add_node(self,node):
         '''
         add a single node to dag
         :param node:
         :return:
         '''
         if node.path == '':
             print 'a node must have HTCondor submit file'
             return 1
         self.nodes.append(node)
    def add_edge(self,edge):
        '''
        add a single edge to dag
        :return:
        '''
        self.edges.append(edge)
    def add_script(self,script):
        '''
        add asingle script to dag
        :param script:
        :return:
        '''
        if len(script.post)==0 and len(script.pre) ==0:
            print 'a script must be a pre or post script'
            return 1
        if len(script.post) != 0 and len(script.pre) != 0:
            print 'can not be both pre and post script'
            return 1
        self.scripts.append(script)

    #write the whole dag to a name.dag file
    def write_nodes(self):
        '''
        covert the nodes in to lines in list
        :return: list
        '''
        result = []
        cnt = 0
        for _ in self.nodes:
            strr = 'JOB '+str(_.name)+' '+ _.path+'\n'
            result.append(strr)
            cnt+=1
        print 'successfully write {0} nodes'.format(cnt)
        return result

    def write_scripts(self):
        #example: SCRIPT PRE  B  pre.csh $JOB .gz
        result = []
        cnt = 0
        for _ in self.scripts:
            #distinguish pre or post
            if len(_.pre)!=0:
                strr = 'SCRIPT PRE ' + ' '.join(_.pre)+' '+_.script+' '+_.argu+'\n'
            else:
                strr = 'SCRIPT POST ' + ' '.join(_.post) + ' ' + _.script + ' ' + _.argu+'\n'

            result.append(strr)
            cnt += 1
        print 'successfully write {0} scripts'.format(cnt)
        return result


    def write_edges(self):
        #example PARENT A CHILD B C
        result = []
        cnt = 0
        for _ in self.edges:
            strr = 'PARENT ' + ' '.join(_.parents) + ' '+'CHILD '+' '.join(_.children)+'\n'
            result.append(strr)
            cnt += 1
        print 'successfully write {0} edges'.format(cnt)
        return result



    def write2file(self,tdir):
        strr = tdir
        strr+= str(self.name)+'.dag'
        with open(strr,"w+") as file:
            nodes = self.write_nodes()
            scripts = self.write_scripts()
            edges = self.write_edges()
            file.writelines(nodes+scripts+edges)




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

    dag = DAG('diamond')
    node1 = Node('A','A.submit')
    node2 = Node('B', 'B.submit')
    node3 = Node('C', 'C.submit')
    node4 = Node('D')
    node4.set_path('D.submit')

    s1 = Script('pre.sh',pre = ['B'], argu = '$JOB .gz')
    s2 = Script('pre.sh',post = ['C'])
    s2.set_argu('$JOB .gz')

    e1 = Edge(['A'],['B','C'])
    e2 = Edge(['B'],['D'])

    for _ in [node1,node2,node3,node4]:
        dag.add_node(_)

    for _ in [s1,s2]:
        dag.add_script(_)

    for _ in [e1,e2]:
        dag.add_edge(_)

    dag.write2file('./')

