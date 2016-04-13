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


def computing_sites():
    sites = []
    with open('sites.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.translate(None, '\n\t ')
            sites.append(line)
    return sites


def print_sites():
    sites = computing_sites()
    for i in range (len(sites)):
        print sites[i]
    return

def valid_site(ce_name):
    sites = computing_sites()
    for i in range (len(sites)):
        if ce_name == sites[i]:
            return True
    return False

def submit_script(path, mac, version, events, output_file, ce_name):
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
    if ce_name is "default":
        print '\033[1;42m this is being sent to a random backend \033[0m'
        j.backend = Dirac(settings={})
    else:
        message = "this is being sent to %s" % (ce_name)
        print '\033[1;42m' + message + '\033[0m'
        j.backend = Dirac()
        j.backend.settings['Destination'] = ce_name
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
    parser.add_argument("-s", dest = 'ce_name', help = "ce to run on", default = 'default')
    parser.add_argument("-c", dest = 'print_screen', help = "print list of computing sites \
                        to screen", default = False)
    args = parser.parse_args()
    if args.print_screen:
        print_sites()
    if args.ce_name is not 'default':
        if valid_site(args.ce_name) == True:
            submit_script(args.path, args.mac_file, args.version, args.events, args.output_file, args.ce_name)
        else:
            print "\033[1;41m not a valid site name \033[0m"
    else:
        submit_script(args.path, args.mac_file, args.version, args.events, args.output_file, args.ce_name)
