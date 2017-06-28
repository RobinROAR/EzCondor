#!/usr/bin/env python
# -*-coding:utf-8 -*-
##RoBinZ @ chtc.wisc.edu
#06.27 2017
# This test case is used fot creating a DAG file in following shape:
#------ File name: diamond.dag--------
# JOB  A  A.condor
# JOB  B  B.condor
# JOB  C  C.condor
# JOB  D  D.condor
# SCRIPT PRE  B  pre.csh $JOB .gz
# SCRIPT PRE  C  pre.csh $JOB .gz
# PARENT A CHILD B C
# PARENT B C CHILD D



# Create a DAX
diamond = ADAG("diamond")

# Add some metadata
diamond.metadata("name", "diamond")
diamond.metadata("createdby", "Gideon Juve")

# Add input file to the DAX-level replica catalog
a = File("f.a")
a.addPFN(PFN("gsiftp://site.com/inputs/f.a", "site"))
a.metadata("size", "1024")
diamond.addFile(a)

# Add executables to the DAX-level replica catalog
e_preprocess = Executable(namespace="diamond", name="preprocess", version="4.0", os="linux", arch="x86_64")
e_preprocess.metadata("size", "2048")
e_preprocess.addPFN(PFN("gsiftp://site.com/bin/preprocess", "site"))
diamond.addExecutable(e_preprocess)

e_findrange = Executable(namespace="diamond", name="findrange", version="4.0", os="linux", arch="x86_64")
e_findrange.addPFN(PFN("gsiftp://site.com/bin/findrange", "site"))
diamond.addExecutable(e_findrange)

e_analyze = Executable(namespace="diamond", name="analyze", version="4.0", os="linux", arch="x86_64")
e_analyze.addPFN(PFN("gsiftp://site.com/bin/analyze", "site"))
diamond.addExecutable(e_analyze)

# Add a preprocess job
preprocess = Job(e_preprocess)
preprocess.metadata("time", "60")
b1 = File("f.b1")
b2 = File("f.b2")
preprocess.addArguments("-a preprocess", "-T60", "-i", a, "-o", b1, b2)
preprocess.uses(a, link=Link.INPUT)
preprocess.uses(b1, link=Link.OUTPUT, transfer=True)
preprocess.uses(b2, link=Link.OUTPUT, transfer=True)
diamond.addJob(preprocess)

# Add left Findrange job
frl = Job(e_findrange)
frl.metadata("time", "60")
c1 = File("f.c1")
frl.addArguments("-a findrange", "-T60", "-i", b1, "-o", c1)
frl.uses(b1, link=Link.INPUT)
frl.uses(c1, link=Link.OUTPUT, transfer=True)
diamond.addJob(frl)

# Add right Findrange job
frr = Job(e_findrange)
frr.metadata("time", "60")
c2 = File("f.c2")
frr.addArguments("-a findrange", "-T60", "-i", b2, "-o", c2)
frr.uses(b2, link=Link.INPUT)
frr.uses(c2, link=Link.OUTPUT, transfer=True)
diamond.addJob(frr)

# Add Analyze job
analyze = Job(e_analyze)
analyze.metadata("time", "60")
d = File("f.d")
analyze.addArguments("-a analyze", "-T60", "-i", c1, c2, "-o", d)
analyze.uses(c1, link=Link.INPUT)
analyze.uses(c2, link=Link.INPUT)
analyze.uses(d, link=Link.OUTPUT, transfer=True, register=True)
diamond.addJob(analyze)

# Add dependencies
diamond.depends(parent=preprocess, child=frl)
diamond.depends(parent=preprocess, child=frr)
diamond.depends(parent=frl, child=analyze)
diamond.depends(parent=frr, child=analyze)

# Write the DAX to stdout
import sys

diamond.writeXML(sys.stdout)

# Write the DAX to a file
f = open("diamond.dax", "w")
diamond.writeXML(f)
f.close()