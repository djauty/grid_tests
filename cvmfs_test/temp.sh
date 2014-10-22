#!/bin/bash
source /cvmfs/snoplus.gridpp.ac.uk/sl6/sw/4.6.0/env_rat-4.6.0.sh
rat -N 5 -o ratoutput -l rat.log ${RATROOT}/mac/production/water/Proton_decay.mac
