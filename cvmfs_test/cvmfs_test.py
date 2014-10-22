# Create a set of jobs to test the CVMFS install
import lcgtools
import cmdexec
import os


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


def submit_ratuser(ce_name):
    print 'Submit rat job to', ce_name
    j = Job()
    j.backend = LCG()
    j.backend.requirements.allowedCEs = ce_name
    j.application = RATUser()
    # Next line only set if don't want to use default cvmfs setup
    # j.application.softwareEnvironment = '/cvmfs/snoplus.gridpp.ac.uk/sl6/sw/4.6.0/env_rat-4.6.0.sh'
    j.application.ratBaseVersion = '5.0.1'
    j.application.ratMacro = '/cvmfs/snoplus.gridpp.ac.uk/sl6/sw/%s/rat-%s/mac/production/teloaded/2223keV_gamma.mac' % (j.application.ratBaseVersion, j.application.ratBaseVersion)
    j.application.nEvents = 5
    j.application.discardOutput = True
    j.application.outputFile = 'temprat'
    j.application.outputDir = 'user/none'
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


for ce_name in list_ces():
#    print ce_name, check_tags(ce_name)
#    if 'alberta' not in ce_name:
#        continue
#    if check_tags(ce_name) is False:
#        submit_script(ce_name)
#    else:
#        submit_ratuser(ce_name)
    submit_ratuser(ce_name)

