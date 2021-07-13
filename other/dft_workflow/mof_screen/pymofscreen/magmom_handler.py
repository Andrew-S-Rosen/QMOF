import numpy as np
import os
from ase.io import read
from copy import copy, deepcopy
from pymofscreen.metal_types import mag_list, dblock_metals, fblock_metals
from pymofscreen.writers import pprint

def get_incar_magmoms(incarpath,poscarpath):
	"""
	Read in the magnetic moments in the INCAR
	Args:
		incarpath (string): path to INCAR

		poscarpath (string): path to POSCAR

	Returns:
		mof_mag_list (list of floats): magnetic moments
	"""
	mof_mag_list = []
	init_mof = read(poscarpath)
	with open(incarpath,'r') as incarfile:
		for line in incarfile:
			line = line.strip()
			if 'MAGMOM' in line:
				mag_line = line.split('= ')[1:][0].split(' ')
				for val in mag_line:
					mag = float(val.split('*')[1])
					num = int(val.split('*')[0])
					mof_mag_list.extend([mag]*num)
	if not bool(mof_mag_list):
		mof_mag_list = np.zeros(len(init_mof))
	if len(mof_mag_list) != len(mof_mag_list):
		raise ValueError('Error reading INCAR magnetic moments')

	return mof_mag_list

def get_mag_indices(mof):
	"""
	Get the indices of metals that could be magnetic
	Args:
		mof (ASE Atoms object): MOF structure

	Returns:
		mag_indices (list of ints): indices of aforementioned metlas
	"""
	mag_indices = [atom.index for atom in mof if atom.number in mag_list]

	return mag_indices

def set_initial_magmoms(mof,spin_level):
	"""
	Set the initial magnetic moments for each atom
	Args:
		mof (ASE Atoms object): MOF structure
		
		spin_level (string): determines default spins

	Returns:
		mof (ASE Atoms object): MOF structure with initial magmoms
	"""

	if isinstance(spin_level,list):
		if len(spin_level) != len(mof):
			raise ValueError('Magmom list is incompatible with number of atoms')
		mof.set_initial_magnetic_moments(spin_level)

	elif isinstance(spin_level,str):
		spin_level = spin_level.lower()
		mag_indices = get_mag_indices(mof)
		mof.set_initial_magnetic_moments(np.zeros(len(mof)))

		if 'afm' not in spin_level:
			for mag_idx in mag_indices:
				mag_number = mof[mag_idx].number
				if spin_level == 'high':
					if mag_number in dblock_metals:
						mof[mag_idx].magmom = 5.0
					elif mag_number in fblock_metals:
						mof[mag_idx].magmom = 7.0
					else:
						raise ValueError('Metal not properly classified')
				elif spin_level == 'low':
					mof[mag_idx].magmom = 0.1
				else:
					raise ValueError('Undefined spin level')
		elif spin_level == 'afm_high':
			AFM_cutoff = 5
			Mi = mag_indices[0]
			M_distances = mof.get_distances(Mi,mag_indices,mic=True,vector=False).tolist()
			mag_indices = [mag_indices[i] for i in np.argsort(M_distances).tolist()]
			mags = copy(mag_indices)
			sign = 1
			del mags[0]
			for i, mag_idx in enumerate(mag_indices):
				if i != 0:
					M_distances = mof.get_distances(Mi,mags,mic=True,vector=False).tolist()
					min_idx = np.argmin(M_distances)
					Mj = mags[min_idx]
					d = M_distances[min_idx]
					if d <= AFM_cutoff:
						sign = -sign
					else:
						sign = 1
					Mi = Mj
					mags.remove(Mj)
					del M_distances[min_idx]
				mag_number = mof[mag_idx].number
				if mag_number in dblock_metals:
					mof[mag_idx].magmom = sign*5.0
				elif mag_number in fblock_metals:
					mof[mag_idx].magmom = sign*7.0
				else:
					raise ValueError('Metal not properly classified')
		else:
			raise ValueError('Undefined AFM spin level')

	else:
		raise TypeError('spin_level has wrong type')

	return mof

def continue_magmoms(mof,incarpath):
	"""
	Continue magmoms from prior run
	Args:
		mof (ASE Atoms object): MOF structure
		
		incarpath (string): path to INCAR

	Returns:
		mof (ASE Atoms object): MOF structure with initial magmoms
	"""
	with open(incarpath,'r') as incarfile:
		for line in incarfile:
			line = line.strip()
			if 'ISPIN = 2' in line:
				mof_magmoms = mof.get_magnetic_moments()
				mof.set_initial_magnetic_moments(mof_magmoms)

	return mof

def get_abs_magmoms(mof,incarpath):
	"""
	Get absolute magmoms, indices, and ispin value from INCAR
	Args:
		mof (ASE Atoms object): MOF structure
		
		incarpath (string): path to INCAR

	Returns:
		abs_magmoms (list of floats): absolute values of magmoms

		mag_indices (list of ints): ASE indices

		ispin (bool): True if ispin = 2 in INCAR
	"""
	mag_indices = get_mag_indices(mof)
	ispin = False
	with open(incarpath,'r') as incarfile:
		for line in incarfile:
			line = line.strip()
			if 'ISPIN = 2' in line:
				ispin = True
				mof_magmoms = mof.get_magnetic_moments()
				abs_magmoms = np.abs(mof_magmoms[mag_indices])
	if not ispin:
		abs_magmoms = np.zeros(len(mag_indices))

	return abs_magmoms, mag_indices, ispin

def continue_failed_magmoms(mof):
	"""
	If job failed, try to read magmoms from OUTCAR
	Args:
		mof (ASE Atoms object): MOF structure
	
	Returns:
		mof (ASE Atoms object): MOF structure with old magmoms
	"""
	self_resort = []
	file = open('ase-sort.dat', 'r')
	lines = file.readlines()
	file.close()
	for line in lines:
	    data = line.split()
	    self_resort.append(int(data[1]))
	magnetic_moments = np.zeros(len(mof))
	n = 0
	lines = open('OUTCAR', 'r').readlines()
	for line in lines:
	    if line.rfind('magnetization (x)') > -1:
	        for m in range(len(mof)):
	            magnetic_moments[m] = float(lines[n + m + 4].split()[4])
	    n += 1
	sorted_magmoms = np.array(magnetic_moments)[self_resort]
	ispin = False
	with open('INCAR','r') as incarfile:
		for line in incarfile:
			line = line.strip()
			if 'ISPIN = 2' in line:
				ispin = True
	if ispin and all(sorted_magmoms == 0.0):
		raise ValueError('Error reading magmoms from failed OUTCAR')
	mof.set_initial_magnetic_moments(sorted_magmoms)

	return mof

def check_if_new_spin(screener,mof,refcode,acc_level,current_spin):
	"""
	Check if new spin converged to old spin
	Args:
		screener (class): pymofscreen.screen.screener class

		mof (ASE Atoms object): MOF structure

		refcode (string): name of MOF

		acc_level (string): current accuracy level

		current_spin (string): current spin level

	Returns:
		True or False depending on if new spin converged to old spin
	"""
	basepath = screener.basepath
	spin_labels = screener.spin_labels
	results_partial_path = os.path.join(basepath,'results',refcode,acc_level)
	success_path = os.path.join(results_partial_path,current_spin)
	incarpath = os.path.join(success_path,'INCAR')
	mof = deepcopy(mof)
	mof = continue_magmoms(mof,incarpath)

	for prior_spin in spin_labels:
		if prior_spin == current_spin:
			break
		old_mof_path = os.path.join(results_partial_path,prior_spin,'OUTCAR')
		old_incar_path = os.path.join(results_partial_path,prior_spin,'INCAR')
		mag_indices = get_mag_indices(mof)
		old_mof = read(old_mof_path)
		old_abs_magmoms, old_mag_indices, old_ispin = get_abs_magmoms(old_mof,old_incar_path)
		mof_mag = mof.get_initial_magnetic_moments()[mag_indices]
		if old_ispin:
			old_mof_mag = old_mof.get_magnetic_moments()[mag_indices]
		else:
			old_mof_mag = [0]*len(mag_indices)
		mag_tol = 0.1
		if np.sum(np.abs(mof_mag - old_mof_mag) >= mag_tol) == 0:
			pprint('Skipping rest because '+current_spin+' converged to '+prior_spin)
			return False
	return True

def check_if_skip_low_spin(screener,mof,refcode,spin_label):
	"""
	Check if low spin job should be skipped
	Args:
		screener (class): pymofscreen.screen.screener class

		mof (ASE Atoms object): MOF structure

		refcode (string): name of MOF

		spin_label (string): current spin label

	Returns:
		skip_low_spin (bool): True if low spin should be skipped
	"""
	acc_levels = screener.acc_levels
	acc_level = acc_levels[-1]
	basepath = screener.basepath
	success_path = os.path.join(basepath,'results',refcode,acc_level,spin_label)
	incarpath = os.path.join(success_path,'INCAR')
	skip_low_spin = False

	abs_magmoms, mag_indices, ispin = get_abs_magmoms(mof,incarpath)
	if not mag_indices:
		skip_low_spin = True
	else:
		if np.sum(abs_magmoms < 0.1) == len(abs_magmoms):
			skip_low_spin = True

	return skip_low_spin