# DAG API
## Mannul

This API is provided for helping HTCondor-unfamiliar people to create a DAG file and its affiliated *.sub files in pure python program.
### API
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
    -argument

class Script:
    _name
    _job
    _position

```
### A small example

- First
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


