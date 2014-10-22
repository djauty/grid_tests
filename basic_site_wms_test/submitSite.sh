#!/bin/bash

# Script to submit to a single site (the argument of the script)
# Choose a site first (e.g. via lcg-infosites ce)

VO=snoplus.snolab.ca
echo $@
for wms in $(lcg-infosites --vo $VO wms); do
    echo "wms: $wms"
    export GLITE_WMS_WMPROXY_ENDPOINT=$wms
    glite-wms-job-submit -a -o singleSiteIDFile -r $@ helloworld.jdl
done 

