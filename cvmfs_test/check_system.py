#!/usr/bin/env python
import os
import sys
import platform
import socket
import subprocess

# First check which version of Enterprise Linux is running
print "Running at "+socket.gethostname()
bits = platform.release().split('.')
release = None
for b in bits:
    if "el" in b:
        release = int(b.strip('el'))
        print release
if not release:
    raise Exception("Unknown system: "+platform.release())

# Print some basic information
print "Check CVMFS"
print os.system("rpm -q -a | grep cvmfs")
print "Check CVMFS/snoplus"
print os.listdir("/cvmfs/snoplus.gridpp.ac.uk")
print "VO_SNOPLUS_SNOLAB_CA_SW_DIR"
print os.environ["VO_SNOPLUS_SNOLAB_CA_SW_DIR"]

# Now run RAT
envfile1 = "/cvmfs/snoplus.gridpp.ac.uk/sl"+str(release)+"/env_cvmfs.sh"
envfile2 = "/cvmfs/snoplus.gridpp.ac.uk/sl"+str(release)+"/sw/4.6.0/env_rat-4.6.0.sh"

script = "#!/bin/bash\n"
script += "source " + envfile1 + "\n"
script += "source " + envfile2 + "\n"
script += "rat -N 5 -o ratoutput -l rat.log ${RATROOT}/mac/production/water/Proton_decay.mac\n"
script_file = open("temp.sh", "w")
script_file.write(script)
script_file.close()

process = subprocess.Popen(["/bin/bash", "temp.sh"], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
output, error = process.communicate()
print os.listdir(os.getcwd())
print "RAT RETURNED: ", process.returncode
if process.returncode!=0:
    print error
sys.exit(process.returncode)
