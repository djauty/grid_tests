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


def submit_ratuser(ce_name):
    print 'Submit rat job to', ce_name
    j = Job()
    j.backend = LCG()
    j.backend.requirements.allowedCEs = ce_name
    j.application = RATUser()
    j.application.softwareDir = '/cvmfs/snoplus.gridpp.ac.uk/sl6-00-00-00/sw'
    j.application.ratMacro = 'mymacro.mac'
    j.application.ratBaseVersion = '4.5.0'
    j.application.discardOutput = True
    j.application.outputFile = 'temprat'
    j.application.outputDir = 'user/none'
    j.submit()


def submit_ratuser_batch():
    j = Job()
    j.backend = Batch()
    j.application = RATUser()
    j.application.softwareDir = '/data/snoplus/softwareSL6'
    j.application.ratMacro = 'mymacro.mac'
    j.application.ratBaseVersion = '4.5.0'
    j.application.discardOutput = True
    j.application.outputFile = 'tempbatchrat'
    j.application.outputDir = '/data/snoplus/mottram/gangaOutputs'
    j.submit()

def submit_script(ce_name):
    print 'Submit script to', ce_name
    j = Job()
    j.backend = LCG()
    j.backend.requirements.allowedCEs = ce_name
    j.application = Executable()
    j.application.exe = os.path.join(os.getcwd(), 'myscript.sh')
    j.application.args = [ce_name]
    j.submit()


submit_ratuser_batch()


for ce_name in list_ces():
    #    if 'liv.ac.uk' not in ce_name and 'shef.ac.uk' not in ce_name and \
        #            'ox.ac.uk' not in ce_name and 'susx.ac.uk' not in ce_name:
    #        continue
    if 'qmul.ac.uk' not in ce_name:
        continue
    if check_sl6(ce_name):
        # Can submit a job here
        #submit_script(ce_name)
        submit_ratuser(ce_name)
