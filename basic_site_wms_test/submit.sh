#!/bin/bash

# Script to submit to ALL sites via ALL wms

VO=snoplus.snolab.ca

for wms in $(lcg-infosites --vo $VO wms); do
    echo "wms: $wms"
    export GLITE_WMS_WMPROXY_ENDPOINT=$wms
    for ce in $(lcg-infosites --vo $VO ce | awk '/\//{print $6}'); do
	echo "ce: $ce"
        glite-wms-job-submit -a -o allCEsJobIDFile  -r $ce helloworld.jdl
    done
done 

