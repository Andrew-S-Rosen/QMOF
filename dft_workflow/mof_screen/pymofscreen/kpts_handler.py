import numpy as np
import os
try:
	import pymatgen as pm
	from pymatgen.io.cif import CifParser
	from pymatgen.io.vasp.inputs import Kpoints
	has_pm = True
except:
	has_pm = False

def get_kpts(screener,cif_file,level):
	"""
	Obtain the number of kpoints
	Args:
		screener (class): pymofscreen.screener class

		cif_file (string): name of CIF file

		level (string): accuracy level

	Returns:
		kpts (list of ints): kpoint grid
		
		gamma (bool): True for gamma-centered
	"""
	niggli = screener.niggli
	mofpath = screener.mofpath
	kpts_path = screener.kpts_path
	kppas = screener.kppas
	kpts = None
	if not mofpath:
		mofpath = ''
		
	if kpts_path == 'Auto' and has_pm:

		if level == 'low':
			kppa = kppas[0]
		elif level == 'high':
			kppa = kppas[1]
		else:
			raise ValueError('kpoints accuracy level not defined')
		filepath = os.path.join(mofpath,cif_file)
		if '.cif' in cif_file:
			parser = CifParser(filepath)
			pm_mof = parser.get_structures(primitive=niggli)[0]
		else:
			pm_mof = pm.Structure.from_file(filepath,primitive=niggli)
		pm_kpts = Kpoints.automatic_density(pm_mof,kppa)
		kpts = pm_kpts.kpts[0]

		if pm_kpts.style.name == 'Gamma':
			gamma = True
		else:
			gamma = None
	elif kpts_path == 'Auto' and not has_pm:
		raise ValueError('Pymatgen not installed. Please provide a kpts file.')
	else:
		old_cif_name = cif_file.split('.cif')[0].split('_')[0]
		infile = open(kpts_path,'r')
		lines = infile.read().splitlines()
		infile.close()

		for i in range(len(lines)):
			if old_cif_name in lines[i]:
				if level == 'low':
					kpts = lines[i+1]
					gamma = lines[i+2]
				elif level == 'high':
					kpts = lines[i+3]
					gamma = lines[i+4]
				else:
					raise ValueError('Incompatible KPPA with prior runs')
				break
		kpts = np.squeeze(np.asarray(np.matrix(kpts))).tolist()
		if not kpts or len(kpts) != 3:
			raise ValueError('Error parsing k-points for '+cif_file)

		if gamma == 'True':
			gamma = True
		elif gamma == 'False':
			gamma = False
		else:
			raise ValueError('Error parsing gamma for '+cif_file)

	return kpts, gamma