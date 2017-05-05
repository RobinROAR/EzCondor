#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This Script is used for submitting and monitoring HTCondor job through python-binding.
#
#Robin  March 20,2017
import htcondor
import classad
import os
from subprocess import PIPE,Popen
import time
import sys
from datetime import datetime

class Utilities:
    '''
    A class for wrap submit/monitor function in HTCondor.
    '''
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
        if subfile == None:
            if self.subfile == None:
                print 'No Subfile'
            else:
                subfile = self.subfile
        
        command = 'condor_submit %s' % (subfile)

        result = os.system(command)
        self.monitor_job()
        return result

    def submit_ondemand(self,jobname, **kwargs):
        '''
        This function will form a ClassAd and Submit job vid input argument, you must provide necessary argument for ClassAd
        :param
        :return: None
        '''
        if self.subfile:
            print 'Submit file exists'
            return
        else:
            #form a python dict firstly
            dict_ad = {}
            for name, value in kwargs.items():
                dict_ad[name] = value

            #initialize key arguments if None
            for key,value in zip(['Cmd','UserLog','Err','JobUniverse'],[None,jobname+'.log',jobname+'.err',5]):
                if dict_ad.has_key(key):
                    continue
                else:
                    dict_ad[key]=value

            #convert to classAd
            schedd = htcondor.Schedd()
            ad = classad.ClassAd(dict_ad)
            print 'Job is submitted to cluster: ', schedd.submit(ad)
            #monitor
            self.monitor_job()



    def submit_file2AD(self,subfile = None):
        if subfile == None:
            if self.subfile == None:
                print 'No Subfile'
            else:
                subfile = self.subfile

        os.system('condor_submit -dump ad %s' % (subfile) )
        if os.path.exists('./ad'):
            cad = classad.parseOne(open("./ad"))
            #convert to python dict and remove redundant key
            tmp = dict(cad)
            keys =  tmp.keys()
            for _ in keys:
                if _ in ['Cmd','RequestDisk', 'Requirements','RequestMemory','UserLog','Err','Owener','']:
                    continue
                else:
                    del tmp[_]
                    print 'key: '+_+' Deleted'
                
            #submit to CM
            ad = classad.ClassAd(tmp)
            print 'Current ClassAd: ',ad
            schedd = htcondor.Schedd()
            print 'submit to cluster: ', schedd.submit(ad)
            self.monitor_job()

    def submit_DAG2AD(self, dagfile):
        DAGMAN="/usr/bin/condor_dagman"
        dag = dagfile
        schedd = htcondor.Schedd()
        ad = classad.ClassAd({  "JobUniverse": 7,  "Cmd": DAGMAN, "Arguments": "-f -l . -Lockfile %s.lock -AutoRescue 1 -DoRescueFrom 0 " \
                  "-Dag %s -Suppress_notification -CsdVersion '%s' -Force -Dagman %s" % (dag, dag, htcondor.version(), DAGMAN),
                    "Env": "_CONDOR_MAX_DAGMAN_LOG=0;_CONDOR_DAGMAN_LOG=%s.dagman.out;" \
                     "_CONDOR_SCHEDD_DAEMON_AD_FILE=%s;_CONDOR_SCHEDD_ADDRESS_FILE=%s" %  (dag, htcondor.param["SCHEDD_DAEMON_AD_FILE"], htcondor.param["SCHEDD_ADDRESS_FILE"]),
                    "EnvDelim": ";",
                    "Out": "%s.lib.out" % dag,
                    "Err": "%s.lib.err" % dag,
                    "ShouldTransferFiles": "IF_NEEDED",
                    "UserLog": os.path.abspath("%s.dagman.log" % dag),
                    "KillSig": "SIGTERM",
                    "RemoveKillSig": "SIGUSR1",
                    #"OtherJobRemoveRequirements": classad.ExprTree('eval(strcat("DAGManJobId == ", ClusterId))'),
                    "OnExitRemove": classad.ExprTree('( ExitSignal =?= 11 || ( ExitCode =!= undefined && ExitCode >= 0 && ExitCode <= 2 ) )'),
                    "FileSystemDomain": htcondor.param['FILESYSTEM_DOMAIN'],
                    "Requirements": classad.ExprTree('true || false'),
                    })
        cluster = schedd.submit(ad)
        print("Submitted as cluster %d" % cluster)

    def find_log(self):
        '''
        fine the log file in current new folder
        :return: name of log
        '''
        for dirpath, dirnames, filenames in os.walk('./'):
            for _ in filenames:
                if _.split(".")[-1] == 'log':
                    return _
        print "No log file"
        return 1

    def monitor_job(self):
        '''
        monitor job finishing time
       :return:
        '''
        logfile = self.find_log()
        #monitoring when job finish
        file = open("./"+logfile)
        cnt = 0
        while 1:
            #打印时间
            sys.stdout.write('Used time: '+str(cnt) + "\r")
            #monitoring tail of log
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(1)
                file.seek(where)
                sys.stdout.flush()
                cnt += 1
            else:
                if "Job terminated" in line:
                    print "Job finished!"
                    break



        #analyze the log
        iterator = htcondor.read_events(open("./"+logfile))
        loglist = []
        while True:
            a = dict(iterator.next())
            # parse the datetime
            if a['MyType'] == 'SubmitEvent':
                stime = a['EventTime'].replace('T',' ')
                st = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
                cluster = a['Cluster']

            if a['MyType'] == 'JobTerminatedEvent':
                etime = a['EventTime'].replace('T',' ')

                et = datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
                cluster = a['Cluster']
                break
        print '-----------Analysis Result-------------:'
        print 'Job use %0.2f s in Cluster %s' % ((et-st).seconds, cluster)



if __name__ == '__main__':
    ez = Utilities('job.prepare.submit')
    #ez.submit_subfile()
    #ez.submit_file2AD()  
    #ez.monitor_job()
    ez = Utilities()
    ez.submit_ondemand('test', Cmd = "/home/rzheng27/python_dag/dag/test/prepare.sh", UserUserLog = "/home/rzheng27/python_dag/dag/test/result.prepare.log" )

