def submit_script():
	j = Job()
	j.application = RATUser()
	j.application.ratMacro = "test_dirac.mac"
	j.application.ratBaseVersion = "5.3.0"
	j.application.args = ['-N', 10]
	j.outputfiles += [GridFile(namePattern = 'output.ntuple.root')]
	j.backend = Dirac(settings={})
	j.submit()

if __name__=="__main__":
	submit_script()
