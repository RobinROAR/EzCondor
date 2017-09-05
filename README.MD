# EzCondor
EzCondor is a Python package for making the use of the HTCondor framework more simple and convenient. It's a useful supplement for HTCondor Python-binding.
## Features
- DAG Python API
- Dask module
- Workflow management
- Convenient utilities


## Modules
### 1. DAG API
A simple API for helping new user create a DAG file and its affiliated *.sub files in pure python style.
### 2. Dask module
Some test case for implementing Dask in HTCondor environment.
### 3. Workflow management
A series of workflow management cases based on the DAG API
### 4. Utilities
class Utilities： a class for warp basic submit and monitor functions of HTCondor, and add more available methods like submit job/DAG via classAD.
```python
class Utilities:
 
    def __init__(self,subfile = None):
        self.subfile = subfile
        self.subad = None
        if subfile != None:
            self.jobname = subfile.split(".")[0]
    def submit_subfile(self,subfile = None):
        '''
        submit a job via *.sub file
        :param 
        :return: stdout
        '''
    def submit_ondemand(self,jobname, **kwargs):
        '''
        This function will form a ClassAd and Submit job vid input argument, you must provide necessary argument for ClassAd
        :param
        :return: None
        '''

    def submit_file2AD(self,subfile = None):
	#convert a submit file to ClassAd form and then submit
    def submit_DAG2AD(self, dagfile):
	#convert a DAG submit file to ClassAd form and then submit
    def monitor_job(self):
       #monitor job finishing time
```




