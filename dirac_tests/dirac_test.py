#!/usr/bin/env python
##############################
#
# dirac_tests
#
# to check if you can run dirac
# on your current system
#
# Author: David Auty
#         <auty@uablerta.ca
#
#############################

try:
    import argparse
except:
    raise ImportError("argparse not available; python version needs to \
                       be 2.7+")


def submit_script(path, mac, version, events, output_file):
    j = Job()
    j.application = RATUser()
    j.application.ratBaseVersion = version
    if path is "default" and mac is "default":
        mac_file = '/cvmfs/snoplus.egi.eu/sl6/sw/%s/rat-%s/mac/production/teloaded/2223keV_gamma.mac' % (j.application.ratBaseVersion, j.application.ratBaseVersion)
    elif path is "default" and mac is not "default":
        mac_file = '/cvmfs/snoplus.egi.eu/sl6/sw/%s/rat-%s/mac/production/teloaded/%s' % (j.application.ratBaseVersion, j.application.ratBaseVersion, mac)
    elif path is not "default" and mac is not "default":
        mac_file = path + mac
    else:
        print "not a valid path. Please provide path to and mac file"
        return
    print mac_file
    j.application.ratMacro = mac_file
    j.application.args = ['-N', events, '-o', output_file]
    j.outputfiles += [GridFile(namePattern = output_file)]
    j.backend = Dirac(settings={})
    j.submit()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", dest = 'mac_file', help = "which .mac file to \
                      use [2223keV.mac] check path", default = 'default')
    parser.add_argument("-v", dest = 'version', help = "which ratBaseVersion to \
                      use [5.3.0]", default='5.3.0')
    parser.add_argument("-N", dest = 'events', help = "number of events generated \
                      [10]", default = 10)
    parser.add_argument("-o", dest = 'output_file', help = "output file name \
                      [output.ntuple.root]", default = 'output.ntuple.root')
    parser.add_argument("-p", dest = 'path', help = "path to mac file \
                      [/cvmfs/snoplus.egi.eu/sl6/sw/%s/rat-%s/mac/production/teloaded/]", 
                      default = 'default')
    args = parser.parse_args()
    submit_script(args.path, args.mac_file, args.version, args.events, args.output_file)

