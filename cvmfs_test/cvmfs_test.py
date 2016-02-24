# Create a set of jobs to test the CVMFS install
import lcgtools
import cmdexec
import os
import optparse
import datetime
import getpass

def list_ces():
    # Ignore queue names
    rtc, out, err = cmdexec.simple('lcg-infosites', '--vo',
                                   'snoplus.snolab.ca', 'ce')
    ces = set()
    for i, line in enumerate(out):
        if i>1:
            ce_name = out[i].split()[-1].partition(":")[0].strip()
            ces.add(ce_name)
    return ces


def check_sl6(ce_name):
    rtc, out, err = cmdexec.simple('lcg-info', ['--vo', 'snoplus.snolab.ca',
                                                '--list-ce', '--attr', 'OSRelease',
                                                '--query', 'CE=*%s*' % ce_name])
    # Will return > 1 if multiple queues, should still just get one value
    release = out[1].split()[-1]
    try:
        release = float(release)
        if release > 6.0:
            return True
    except ValueError:
        print "Skip %s: %s" % (ce_name, release)
    return False


def check_tags(ce_name):
    rtc, out, err = cmdexec.simple('lcg-ManageVOTag', ['-vo', 'snoplus.snolab.ca', 
                                                       '-host', ce_name, '--list'])
    tagged = False
    for line in out:
        if 'VO-snoplus.snolab.ca-cvmfs' in line:
            tagged = True
    return tagged


def submit_ratuser(ce_name, username, password, filename = None, output_dir = None):
    print 'Submit rat job to', ce_name
    j = Job()
    j.backend = LCG()
    j.backend.requirements.allowedCEs = ce_name
    j.application = RATProd()
    # Next line only set if don't want to use default cvmfs setup
    # j.application.softwareEnvironment = '/cvmfs/snoplus.gridpp.ac.uk/sl6/sw/4.6.0/env_rat-4.6.0.sh'
    j.application.rat_db_user = username
    j.application.rat_db_pswd = password
    j.application.ratVersion = '5.2.2'
    j.application.ratMacro = '/cvmfs/snoplus.egi.eu/sl6/sw/%s/rat-%s/mac/production/teloaded/2223keV_gamma.mac' % (j.application.ratVersion, j.application.ratVersion)
    j.application.rat_args += [ '-N', 20, '-o', filename]
    if output_dir is None or filename is None:
        j.application.outputFiles = 'temprat'
        j.application.outputDir = 'user'
        j.application.discardOutput = True
    else:
        j.application.outputFiles = "%s.root" % filename
        j.application.outputDir = output_dir
    j.submit()


def submit_script(ce_name):
    print 'Submit script to', ce_name
    j = Job()
    j.backend = LCG()
    j.backend.requirements.allowedCEs = ce_name
    j.application = Executable()
#    j.application.exe = os.path.join(os.getcwd(), 'myscript.sh')
    j.application.exe = os.path.join(os.getcwd(), "check_system.py")
    j.application.args = [ce_name]
    j.submit()


if __name__=="__main__":
    parser = optparse.OptionParser()
    parser.add_option("-s", dest="name_pattern", help="Check only sites with names containing this pattern")
    parser.add_option("-f", dest="store_file", action="store_true", help="Stores output files (if possible!")
    (options, args) = parser.parse_args()    

    username = raw_input("Username for database access: ")
    password = getpass.getpass("Password for database access: ")

    for ce_name in list_ces():
        check_site = True
        if options.name_pattern:
            if options.name_pattern not in ce_name:
                check_site = False
        if check_site:
            output_file = None
            output_dir = None
            if options.store_file:
                output_file = ce_name.replace(".", "_")
                output_dir = "user/%s" % datetime.date.today().isoformat()
            submit_ratuser(ce_name, username, password, output_file, output_dir)
            submit_script(ce_name)
