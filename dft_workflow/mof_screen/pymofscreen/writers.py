import os
from shutil import copyfile, move

def pprint(printstr):
	"""
	Redirects pprint to stdout
	Args:
		printstr (string): string to print to stdout
	"""
	print(printstr)
	with open('screening.log','a') as txtfile:
		txtfile.write(printstr+'\n')

def write_success(workflow,neb=False):
	"""
	Write out the successful job files
	Args:
		workflow (class): pymofscreen.screen_phases.worfklow class
	"""
	spin_label = workflow.spin_label
	acc_level = workflow.acc_levels[workflow.run_i]
	pprint('SUCCESS: '+spin_label+', '+acc_level)
	refcode = workflow.refcode
	basepath = workflow.basepath
	vasp_files = workflow.vasp_files
	gzip_list = ['AECCAR0','AECCAR2','CHGCAR','DOSCAR','WAVECAR','PROCAR']
	if not neb:
		success_path = os.path.join(basepath,'results',refcode,acc_level,spin_label)
	elif neb:
		success_path = os.path.join(basepath,'results',refcode,acc_level)
	if not os.path.exists(success_path):
		os.makedirs(success_path)
	if not neb:
		if acc_level in ['scf_test','final_spe']:
			files_to_copy = vasp_files+['DOSCAR','EIGENVAL','IBZKPT','PROCAR','AECCAR0','AECCAR2','OSZICAR']
		elif 'dimer' in acc_level:
			files_to_copy = vasp_files+['DIMCAR','MODECAR','NEWMODECAR','CENTCAR']
		else:
			files_to_copy = vasp_files
		for file in files_to_copy:
			if os.path.isfile(file) and os.stat(file).st_size > 0:
				write_to_path = os.path.join(success_path,file)
				if file in gzip_list:
					os.system('gzip < '+file+' > '+file+'.gz')
					move(file+'.gz',write_to_path+'.gz')
				else:
					copyfile(file,write_to_path)
	elif neb:
		tar_file = 'neb.tar.gz'
		os.system('tar -zcvf '+tar_file+' neb')
		if os.path.isfile(tar_file) and os.stat(tar_file).st_size > 0:
			write_to_path = os.path.join(success_path,tar_file)
			copyfile(tar_file,write_to_path)
		os.remove('neb.tar.gz')

def write_errors(workflow,mof,neb=False):
	"""
	Write out the unsuccesful job files
	Args:
		workflow (class): pymofscreen.screen_phases.worfklow class
		
		mof (ASE Atoms object): ASE Atoms object
	"""
	spin_label = workflow.spin_label
	acc_level = workflow.acc_levels[workflow.run_i]
	pprint('ERROR: '+spin_label+', '+acc_level+' failed')
	gzip_list = ['AECCAR0','AECCAR2','CHGCAR','DOSCAR','WAVECAR']
	if acc_level != 'scf_test' and 'neb' not in acc_level:
		if mof is None:
			pprint('^ VASP crashed')
		elif not mof.calc.converged:
			pprint('Calculation not converged')
	refcode = workflow.refcode
	basepath = workflow.basepath
	vasp_files = workflow.vasp_files
	if not neb:
		error_path = os.path.join(basepath,'errors',refcode,acc_level,spin_label)
	elif neb:
		error_path = os.path.join(basepath,'errors',refcode,acc_level,spin_label)
	if not os.path.exists(error_path):
		os.makedirs(error_path)
	if not neb:
		if 'dimer' in acc_level:
			files_to_copy = vasp_files+['DIMCAR','MODECAR','NEWMODECAR','CENTCAR']
		else:
			files_to_copy = vasp_files
		for file in files_to_copy:
			if os.path.isfile(file) and os.stat(file).st_size > 0:
				write_to_path = os.path.join(error_path,file)
				if file in gzip_list:
					os.system('gzip < '+file+' > '+file+'.gz')
					move(file+'.gz',write_to_path+'.gz')
				else:
					copyfile(file,write_to_path)
	elif neb:
		tar_file = 'neb.tar.gz'
		os.system('tar -zcvf '+tar_file+' neb')
		if os.path.isfile(tar_file) and os.stat(tar_file).st_size > 0:
			write_to_path = os.path.join(error_path,tar_file)
			copyfile(tar_file,write_to_path)		
