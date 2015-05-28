#!/bin/bash

# Script to submit to ALL sites via ALL wms
# should create a proxy which is valid for 1 hour

VO=snoplus.snolab.ca

#create proxy
voms-proxy-init --voms $VO --valid 1:0
myproxy-init -d -n

#loop over all wms
for wms in $(lcg-infosites --vo $VO wms); do
    echo "wms: $wms"
    export GLITE_WMS_WMPROXY_ENDPOINT=$wms

    var=$(echo $wms | awk -F":" '{print $1,$2,$3}') 
    set -- $var
    
    #check wms for certain strings to submit the right jobs to the right wms and then submit the jobs to all sites
    if [[ $2 == *rl* ]]; then 
        echo $2                       
        for ce in $(lcg-infosites --vo $VO ce | awk '/\//{print $6}'); do
	        echo "ce: $ce"
            glite-wms-job-submit -a -o jobIDfile_rl -r $ce myproxytest_rl.jdl
        done
    elif [[ $2 == *gl* ]]; then
        for ce in $(lcg-infosites --vo $VO ce | awk '/\//{print $6}'); do
	        echo "ce: $ce"
            glite-wms-job-submit -a -o jobIDfile_gl -r $ce myproxytest_gl.jdl
        done
    elif [[ $2 == *ic* ]]; then 
        for ce in $(lcg-infosites --vo $VO ce | awk '/\//{print $6}'); do
	        echo "ce: $ce"
            glite-wms-job-submit -a -o jobIDfile_ic -r $ce myproxytest_ic.jdl
        done
    fi 
done