import os
from copy import deepcopy
import numpy as np
from ase.io import read
from ase.optimize import BFGSLineSearch
from pymofscreen.calc_swaps import update_calc, check_nprocs
from pymofscreen.error_handler import get_niter, get_error_msgs, update_calc_after_errors, continue_mof
from pymofscreen.compute_environ import choose_vasp_version
from pymofscreen.janitor import clean_files
from pymofscreen.magmom_handler import continue_magmoms

def mof_run(workflow,mof,calc,kpts,images=None,force_nupdown=False):
	"""
	Run an atoms.get_potential_energy() calculation
	Args:
		workflow (class): pymofscreen.screen_phases.worfklow class

		mof (ASE Atoms object): ASE Atoms object for MOF

		calc (dict): ASE Vasp calculator

		kpts (list of ints): k-point grid

		images (int): number of NEB images

		force_nupdown (bool): force NUPDOWN to nearest int

	Returns:
		mof (ASE Atoms object): updated ASE Atoms object

		calc_swaps (list of strings): calc swaps
	"""

	nprocs = workflow.nprocs
	ppn = workflow.ppn
	calc_swaps = workflow.calc_swaps
	refcode = workflow.refcode
	stdout_file = workflow.stdout_file
	calc_swaps = workflow.calc_swaps
	gamma = workflow.kpts_dict['gamma']

	if force_nupdown:
		init_mags = mof.get_initial_magnetic_moments()
		summed_mags = np.sum(np.abs(init_mags))
		nupdown = int(np.round(summed_mags,0))
		calc.int_params['nupdown'] = nupdown
	elif workflow.nupdown is not None:
		calc.int_params['nupdown'] = workflow.nupdown

	gpt_version = sum(kpts) == 3
	if images is not None:
		neb = True
		calc.int_params['images'] = images
	else:
		neb = False
	if not neb:
		try:
			nprocs = check_nprocs(len(mof),nprocs,ppn)
		except:
			pass
	choose_vasp_version(gpt_version,nprocs)
	calc.input_params['kpts'] = kpts
	calc.input_params['gamma'] = gamma
	if calc.int_params['ncore'] is None and calc.int_params['npar'] is None:
		calc.int_params['ncore'] = int(ppn/2.0)
	calc, calc_swaps = update_calc(calc,calc_swaps)
	mof.set_calculator(calc)
	success = False

	try:
		mof.get_potential_energy()
		niter = get_niter('OUTCAR')
		if niter < mof.calc.int_params['nsw'] and mof.calc.converged != True:
			raise SystemError('VASP stopped but did not die')
		success = True
	except:

		if not os.path.isfile('STOPCAR') and not neb:

			old_error_len = 0
			restart_files = ['WAVECAR','CHGCAR']

			while True:

				errormsg = get_error_msgs('OUTCAR',refcode,stdout_file)
				print(errormsg)
				calc, calc_swaps = update_calc_after_errors(calc,calc_swaps,
					errormsg)
				error_len = len(errormsg)
				if error_len == old_error_len:
					break

				clean_files(restart_files)
				mof = continue_mof()
				choose_vasp_version(gpt_version,nprocs)
				mof.set_calculator(calc)

				try:
					mof.get_potential_energy()
					niter = get_niter('OUTCAR')
					if (niter < mof.calc.int_params['nsw'] and 
						mof.calc.converged != True):
						raise SystemError('VASP stopped but did not die')
					success = True
				except:
					pass

				old_error_len = error_len

	if not success:
		mof = None

	return mof, calc_swaps

def mof_bfgs_run(workflow,mof,calc,kpts,steps=100,fmax=0.05,force_nupdown=False):
	"""
	Run ASE BFGSLineSearch calculation
	Args:
		workflow (class): pymofscreen.screen_phases.worfklow class

		mof (ASE Atoms object): ASE Atoms object for MOF

		calc (dict): ASE Vasp calculator

		kpts (list of ints): k-point grid

		steps (int): maximum number of steps

		fmax (int): force tolerance

		force_nupdown (bool): force NUPDOWN to nearest int

	Returns:
		mof (ASE Atoms object): updated ASE Atoms object

		dyn (class): ASE dynamics class

		calc_swaps (list of strings): calc swaps
	"""

	nprocs = workflow.nprocs
	ppn = workflow.ppn
	calc_swaps = workflow.calc_swaps
	refcode = workflow.refcode
	stdout_file = workflow.stdout_file
	calc_swaps = workflow.calc_swaps
	gamma = workflow.kpts_dict['gamma']

	if force_nupdown:
		init_mags = mof.get_initial_magnetic_moments()
		summed_mags = np.sum(np.abs(init_mags))
		nupdown = int(np.round(summed_mags,0))
		calc.int_params['nupdown'] = nupdown
	elif workflow.nupdown is not None:
		calc.int_params['nupdown'] = workflow.nupdown

	gpt_version = sum(kpts) == 3
	nprocs = check_nprocs(len(mof),nprocs,ppn)
	choose_vasp_version(gpt_version,nprocs)
	calc.input_params['kpts'] = kpts
	calc.input_params['gamma'] = gamma
	if calc.int_params['ncore'] is None and calc.int_params['npar'] is None:
		calc.int_params['ncore'] = int(ppn/2.0)
	calc, calc_swaps = update_calc(calc,calc_swaps)
	mof.set_calculator(calc)
	dyn = BFGSLineSearch(mof,trajectory='opt.traj')
	success = False

	try:
		dyn.run(fmax=fmax,steps=steps)
		success = True
	except:

		if not os.path.isfile('STOPCAR'):

			old_error_len = 0
			restart_files = ['WAVECAR','CHGCAR']

			while True:

				errormsg = get_error_msgs('OUTCAR',refcode,stdout_file)
				print(errormsg)
				calc, calc_swaps = update_calc_after_errors(calc,calc_swaps,
					errormsg)
				error_len = len(errormsg)
				if error_len == old_error_len:
					break

				clean_files(restart_files)
				mof = continue_mof()
				mof.set_calculator(calc)
				dyn = BFGSLineSearch(mof,trajectory='opt.traj')

				try:				
					dyn.run(fmax=fmax,steps=steps)
					success = True
				except:
					pass

				old_error_len = error_len

	if not success:
		mof = None

	return mof, dyn, calc_swaps

def prep_next_run(workflow):
	"""
	Prepare for the next run
	Args:
		workflow (class): pymofscreen.screen_phases.worfklow class
		
	Returns:
		mof (ASE Atoms object): updated ASE Atoms object
	"""

	acc_levels = workflow.acc_levels
	acc_level = acc_levels[workflow.run_i]
	refcode = workflow.refcode
	spin_label = workflow.spin_label
	basepath = workflow.basepath
	success_path = os.path.join(basepath,'results',refcode,acc_level,spin_label)
	outcarpath = os.path.join(success_path,'OUTCAR')
	errorpath = os.path.join(basepath,'errors',refcode,acc_level,spin_label)

	mof = None if os.path.exists(errorpath) else read(outcarpath)
	workflow.run_i += 1

	return mof

def prep_new_run(workflow):
	acc_levels = workflow.acc_levels
	acc_level = acc_levels[workflow.run_i-1]
	refcode = workflow.refcode
	spin_label = workflow.spin_label
	basepath = workflow.basepath
	success_path = os.path.join(basepath,'results',refcode,acc_level,spin_label)
	outcarpath = os.path.join(success_path,'OUTCAR')
	incarpath = os.path.join(success_path,'INCAR')

	mof = read(outcarpath)
	mof_initialized = deepcopy(mof)
	mof_initialized = continue_magmoms(mof_initialized,incarpath)

	return mof_initialized