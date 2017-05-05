#!/usr/bin/env python

from __future__ import print_function
import htcondor, classad
import os, sys

DAGMAN="/usr/bin/condor_dagman"
dag = sys.argv[1]
#test dag existence
os.stat(dag)
schedd = htcondor.Schedd()
ad = classad.ClassAd({
  "JobUniverse": 7,
  "Cmd": DAGMAN,
  "Arguments": "-f -l . -Lockfile %s.lock -AutoRescue 1 -DoRescueFrom 0 " \
    "-Dag %s -Suppress_notification -Force -Dagman %s" % (dag, dag, DAGMAN),
  "Env": "_CONDOR_MAX_DAGMAN_LOG=0;_CONDOR_DAGMAN_LOG=%s.dagman.out;" \
    "_CONDOR_SCHEDD_DAEMON_AD_FILE=%s;_CONDOR_SCHEDD_ADDRESS_FILE=%s" %
    (dag, htcondor.param["SCHEDD_DAEMON_AD_FILE"],
    htcondor.param["SCHEDD_ADDRESS_FILE"]),
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
  #"TransferIn": classad.ExprTree('false'),
  #"TransferInputSizeMB": 0,
})
cluster = schedd.submit(ad)
print("Submitted as cluster %d" % cluster)