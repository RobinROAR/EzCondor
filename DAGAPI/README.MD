# DAG Python API
## Abstract

- This DAG API is provided for helping HTCondor-unfamiliar people to create a DAG and affiliated *.sub files in pure python environment. 
 - Users are able to use the common model language on workflow like Nodes and Edges to form a DAG job. Then the API will automatically generate the corresponding DAG files and submitfiles as needed.


### Struct
```python
class DAG:
     _name
     Nodes
     Edges

class Node:
    _name
    Job
    Scripts

class Edge:
    _parents
    _children

class Job:
    _name
    _executable
    _argument

class Script:
    _name
    _job
    _position

Other tools

```
### A small example

```python
from DAG import DAG

#Firstly, we need to create some necessary objects for a DAG file.
#Create a job, a Job must be initialized with (name, executable)
j1 = Job('job1','a.sh')
# we can add commands to a job discription file except for the initial values。
j1.add_commands(should_transfer_files='YES',
                 when_to_transfer_output='ON_EXIT',
                 Arguments='in1 in2 out1', Queue = 3)

#Create Script objects, a Script must be initialized with (scriptname, job, position)
s1 = Script('a.sh','j1','PRE')
s2 = Script('a.sh','j1','POST', argu = '$JOB .gz')

#Now, we begin to create a DAG
#Create a DAG object, a DAG must be initialized with name.
dag = DAG('diamond.dag')
#Create a Node, initialized with a node name, and assign values.
node1 = Node('A')
#Assign previously created Job object.
node1.job = j1
#Assign scripts
node1.scripts = [s1,s2]
node2 = Node('B')
node2.job = j2
node2.scripts = [s2]
#Create Edge objects
e1 = Edge(['A','D'],['B','C'])
e2 = Edge(['A'],['B'])

#Add elements to the DAG
for _ in [node1,node2,node3,node4]:
    dag.add_node(_)
for _ in [e1,e2]:
    dag.add_edge(_)

#Write to file
dag.write2file('./')

```

### 2. Tools
#### dag2dataflow.py: 
A tool which reads a DAG description file(*.dag) and outputs a dataflow result.

```python
# dag file example:
# File name: diamond.dag
#    JOB  A  test.py
#    JOB  B  test.py
#    PARENT A CHILD B C
#    PARENT B C CHILD D
# a dataflow model:
#   [{input: ..., transform: name.  output: ....}...]

robin@RobinLaptop:~/LocalProject/HTCondorPython$ ./step0418.py t.py
test.py has no marco: input
test.py has no marco: input
[{'Input': ['8788.abc', 'uim.data', 'mathematica.sh'], 'T': 'A', 'Output': ['t.py', 'test.py']}, {'Input': ['8788.abc', 'uim.data', 'mathematica.sh'], 'T': 'B', 'Output': ['t.py', 'test.py']}]
```

#### dag_makefile.py: 
a common script used as a PRE script before every node in DAG, which can make sure all nodes in a workflow can be executed only if its input and output meet the following rule. 

-  Rule:
```python
if a OP node:
    if all input_sandbox files exist:
        if all output_sandbox files exist:
            if the all output files are created lately than all input files:
                turn into NOOP
            else:
                no change # new input
        else:
            no change  # lack output 
    else：
        turn into NOOP
if a NOOP node:
    if all input—sandbox files exist:
        if all output files exist:
            if all output files created lately than all input files:
                no change  #no new input
            else:
                turn into OP
        else:
            turn into OP
    else:
        no change   # lack input
```

### Dependencies
#### ExtractMacros.py
 a class for extracting macros and their values in a submit file  

```python
class ExtractMacros:
	def __init__(self,filename):
        	self.filename = filename
	def handle_process(self,line, queue): 
	#a fuction to handle the queue of input or out put  = in.$(Process)
	def extract_rm(self,line,regulation,queue):
	# match target regulation, add all its value in a list and return	
	def extract(self, *args):
       '''
       main function for extracting the content of target macros
       1. accept more than one macros
       2. the result is a dict which its keys are macros and values are the content of macros.
        :return: a dict include target macros
        '''
```
#### ModifyNode.py :  
class ModifyNode： a class for modifying single node in dag
```python
#This class is used for changing a node's status by modifying its description file.
class ModifyNode:
    def __init__(self,nodename):
        self.filename = nodename

    def detect_status(self,macro,status):
        # check whether a macro's value matches the giving status.
    def change_to_noop(self):
        # change a Dag node to noop
    def reverse_noop(self):
        # reverse a noop nodes to  a Dag node to normal status.
```
