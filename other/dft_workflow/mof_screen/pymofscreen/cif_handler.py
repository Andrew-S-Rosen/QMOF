import os
from ase.io import read, write
import numpy as np
from pymofscreen.writers import pprint
try:
	import pymatgen as pm
	from pymatgen.io.cif import CifParser
	has_pm = True
except:
	no_pm = False
	import warnings

def get_cif_files(mofpath,skip_mofs=None):
	"""
	Get the list of CIF files
	Args:
		mofpath (string): directory to CIF files 

		skip_mofs (list): list of MOFs to ignore

	Returns:
		sorted_cifs (list): alphabetized list of CIF files
	"""
	cif_files = []
	if skip_mofs is None:
		skip_mofs = []
	for filename in os.listdir(mofpath):
		filename = filename.strip()
		if '.cif' in filename or 'POSCAR_' in filename:
			refcode = (
				filename.split('.cif')[0]
				if '.cif' in filename
				else filename.split('POSCAR_')[1]
			)
			if refcode not in skip_mofs:
				cif_files.append(filename)
			else:
				pprint(f'Skipping {refcode}')

	return sorted(cif_files)

def cif_to_mof(filepath,niggli):
	"""
	Convert file to ASE Atoms object
	Args:
		filepath (string): full path to structure file

		niggli (bool): if Niggli-reduction should be performed
		
	Returns:
		sorted_cifs (list): alphabetized list of CIF files
	"""

	tol = 0.8
	if niggli and has_pm:
		if '.cif' in os.path.basename(filepath):
			parser = CifParser(filepath)
			pm_mof = parser.get_structures(primitive=True)[0]
		else:
			pm.Structure.from_file(filepath,primitive=True)
		pm_mof.to(filename='POSCAR')
		mof = read('POSCAR')
		write('POSCAR',mof)
	elif niggli:
		warnings.warn('Pymatgen not installed. Niggli set to False',Warning)
	else:
		mof = read(filepath)
		write('POSCAR',mof)

	mof = read('POSCAR')
	d = mof.get_all_distances()
	min_val = np.min(d[d>0])
	if min_val < tol:
		pprint(f'WARNING: Atoms overlap by {str(min_val)}')

	return mof
