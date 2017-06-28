# DAG API
## Mannul
- Job
    - a job, intitilized with a name, exe, and argument(select)
    - attributes:
        - name
        - exe
        - argu
        - path

- Script
    - __init__(name,job,position,argu = None)
    - attributes:
        - name
        - job
        - position
        - path: read_only
        - argu

- Node
    - __init__(self,name,job = None, scripts=[]):
    - attributes:
        - name:  the name of node
        - job: a job object
        - scripts: a list of script object
- DAG:
    -  __init__(self,name = 'new_dag', nodes = [],edges = []):
    - attributes:



# rules:
- Dag:
    - add_node(): check a node must have all necessary element
    - add_edges(): the related nodes must in dag.nodes

- Script:
    a script must exist
