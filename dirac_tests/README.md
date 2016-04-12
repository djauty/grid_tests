To run dirac_tests you need to have already have a dirac proxy setup

  cd ~/dirac_ui/
  
  . bashrc
  
  dirac-proxy-init -g snoplus.snolab.ca_user -M

and source the data-flow env.sh file

  cd ~/data-flow

  source env.sh

to run need to enter code

  ganga dirac_test.py

