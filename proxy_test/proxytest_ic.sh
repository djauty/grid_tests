#!/bin/bash

# This should use lcg-infosites, but that seems not
# to work for the gridpp VO for now, but the actual
# LFC does.

export LFC_HOST=lfc.gridpp.rl.ac.uk

# Tweak the last component of this for other people, 
# change the whole thing for other VOs

export LFC_HOME=/grid/snoplus.snolab.ca/myproxytests/icwms

# Pick an SE. Not using the sites' default close SE
# though we could really since everything's getting
# registered in the LFC anyway.

targetSE=$VO_SNOPLUS_SNOLAB_CA_DEFAULT_SE

# Function to run a CPU burn process while we sleep 
# to avoid tripping inefficient jobs killers
busywait() {
	./burnP6 &
	pid=$!
	sleep $1
	kill ${pid}
}


chmod u+x ./burnP6
myhost=$(hostname -f)
echo ${LFC_HOST}
echo ${LFC_HOME}

#shortened from 100 to 10 hours
#for ((h=0;h<=10;h++)); do
#    for ((m=0;m<=50;m=m+10)); do
for ((h=0;h<=10;h++));do
    for ((m=0;m<60;m=m+10));do
	datestr=$(date +"%F-%T")
	voms-proxy-info --all
	date >proxyinfo
	echo ${GRID_JOBID} >>proxyinfo
	voms-proxy-info --all >>proxyinfo
	foutname=myproxytest-${myhost}_${datestr}_${h}.${m}
	lcg-cr -d ${targetSE} -P myproxytests/icwms/${foutname} -l lfn:/grid/snoplus.snolab.ca/myproxytests/icwms/${foutname} file://$(pwd)/proxyinfo
	busywait 600
    done
done


	
