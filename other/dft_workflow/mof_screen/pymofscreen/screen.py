import os
import numpy as np
import sys
from copy import deepcopy
from shutil import copyfile
from pymofscreen.writers import pprint
from pymofscreen.kpts_handler import get_kpts
from pymofscreen.screen_phases import workflows
from pymofscreen.janitor import prep_paths
from pymofscreen.magmom_handler import check_if_new_spin, check_if_skip_low_spin

class screener():
	"""
	This class constructs a high-throughput screening workflow
	"""
	def __init__(self,basepath,mofpath=None,kpts_path='Auto',kppas=None,
		submit_script=None,stdout_file=None):
		"""
		Initialize variables that should be used on all MOFs in a database
		Args:
			basepath (string): path to the base directory for the DFT screening

			mofpath (string): path to the directory containing the CIF files

			kpts_path (string): can be either 'Auto' for an automatic generation
			of the kpoints based on KPPAs or a string representing the path to a
			text file with all the kpoint information (refer to examples/kpts.txt)

			kppas (list of ints): KPPAs to use if kpts_path == 'Auto' (defaults
			to kppas = [100, 1000] for 100 and 1000 KPPA for the low and high
			accuracy runs)

			submit_script (string): path to job submission script

			stdout_file (string): path to the stdout file (defualts to the 
			name of the Python job with a .out extension instead of .py)
		"""
		#Setup default parameters
		self.mofpath = mofpath
		self.basepath = basepath
		pwd = os.getcwd()
		if submit_script is None:
			submit_script = os.path.join(pwd,'sub_screen.job')
		self.submit_script = submit_script
		if stdout_file is None:
			stdout_file = os.path.join(pwd,sys.argv[0].split('.py')[0]+'.out')
		self.stdout_file = stdout_file
		self.kpts_path = kpts_path
		if kppas is None:
			self.kppas = [100,1000]
		else:
			self.kppas = kppas
		prep_paths(basepath)

	def run_screen(self,cif_file,mode,niggli=True,spin_levels=None,nupdowns=None,acc_levels=None,calculators=None):
		"""
		Run high-throughput ionic or volume relaxations
		Args:
			cif_file (string): name of CIF file

			mode (string): 'ionic', 'volume', or 'ts'

			niggli (bool): True/False if Niggli-reduction should be done (defaults
			to niggli=True)
			
			spin_levels (list of lists or list of strings): spin states to consider. If provided
			as a list of lists, each sub-list represents the initial magmom for each atom
			in cif_file. If a list of string, the strings must be 'high', 'low', or 'AFM_high'
			to use pre-set initial magmoms (defaults to ['high','low']) 

			nupdowns (list of ints): value to set NUPDOWN (defaults to None)

			acc_levels (list of strings): accuracy levels to consider

			calculators (function): function to call respective calculator (defaults to
			automatically importing from pymofscreen.default_calculators.calcs)

		Returns:
			best_mof (ASE Atoms objects): ASE Atoms object for optimized MOF
		"""
		#Setup default parameters
		from pymofscreen.default_calculators import calcs
		if calculators is None:
			calculators = calcs
		self.calcs = calculators
		self.niggli = niggli
		basepath = self.basepath

		if mode == 'ionic':
			if acc_levels is None:
				acc_levels = ['scf_test','isif2_lowacc','isif2_medacc',
				'isif2_highacc','final_spe']
		elif mode == 'volume':
			if acc_levels is None:
				acc_levels = ['scf_test','isif2_lowacc','isif3_lowacc',
				'isif3_highacc','final_spe']
		elif mode == 'ts':
			if acc_levels is None:
				acc_levels = ['scf_test','dimer_lowacc']			
		else:
			raise ValueError('Unsupported DFT screening mode')
			
		if 'scf_test' not in acc_levels:
			acc_levels = ['scf_test']+acc_levels
		self.acc_levels = acc_levels

		if spin_levels is None:
			spin_levels = ['high','low']
		if not isinstance(spin_levels,list):
			spin_levels = [spin_levels] 
		self.spin_levels = spin_levels

		if nupdowns is None:
			nupdowns = [None]*len(spin_levels)
		elif nupdowns is not None and len(nupdowns) != len(spin_levels):
			raise ValueError('Length of nupdowns must equal spin_levels')
		self.nupdowns = nupdowns
		spin_labels = ['spin'+str(i+1) for i,j in enumerate(spin_levels)]
		self.spin_labels = spin_labels

		#Make sure MOF isn't running on other process
		if 'POSCAR_' in cif_file:
			refcode = cif_file.split('POSCAR_')[1]
		elif '.cif' in cif_file:
			refcode = cif_file.split('.cif')[0]
		else:
			raise ValueError('Unknown file naming scheme')
		working_cif_path = os.path.join(basepath,'working',refcode)

		if os.path.isfile(working_cif_path):
			pprint('SKIPPED '+refcode+': Running on another process')
			return None
		open(working_cif_path,'w').close()

		#Get the kpoints
		kpts_lo, gamma = get_kpts(self,cif_file,'low')
		kpts_hi, gamma = get_kpts(self,cif_file,'high')
		kpts_dict = {}
		kpts_dict['kpts_lo'] = kpts_lo
		kpts_dict['kpts_hi'] = kpts_hi
		kpts_dict['gamma'] = gamma

		#Initialize variables
		E = np.inf
		mof = None
		prior_spin = None

		#for each spin level, optimize the structure
		for i, spin_level in enumerate(spin_levels):

			spin_label = spin_labels[i]
			self.spin_label = spin_label
			self.nupdown = nupdowns[i]
			pprint('***STARTING '+refcode+': '+spin_label+'***')

			#Check if spin state should be skipped
			if i > 0:
				prior_spin = spin_labels[i-1]
				if spin_levels[i-1] == 'high':
					skip_low_spin = check_if_skip_low_spin(self,mof,refcode,prior_spin)
					if skip_low_spin:
						pprint('Skipping low spin due to low magmoms in prior run')
						continue
			same_spin = False

			#Set up workflow object
			wf = workflows(self,cif_file,kpts_dict,spin_level,prior_spin)

			#for each accuracy level, optimize structure
			for acc_level in acc_levels:

				if acc_level == 'scf_test':
					scf_pass = wf.scf_test()
					if not scf_pass:
						os.remove(working_cif_path)
						return None
					if acc_levels[-1] == 'scf_test':
						os.remove(working_cif_path)
						return scf_pass

				elif acc_level == 'isif2_lowacc':
					mof = wf.isif2_lowacc()
					if mof is None:
						os.remove(working_cif_path)
						return None

					if i > 0:
						is_new_spin = check_if_new_spin(self,mof,refcode,acc_level,spin_label)
						if not is_new_spin:
							same_spin = True
							break

				elif acc_level == 'isif2_medacc':
					mof = wf.isif2_medacc()
					if mof is None:
						os.remove(working_cif_path)
						return None

				elif acc_level == 'isif2_highacc':
					mof = wf.isif2_highacc()
					if mof is None:
						os.remove(working_cif_path)
						return None
				
				elif acc_level == 'isif3_lowacc':
					mof = wf.isif3_lowacc()
					if mof is None:
						os.remove(working_cif_path)
						return None

				elif acc_level == 'isif3_highacc':
					mof = wf.isif3_highacc()
					if mof is None:
						os.remove(working_cif_path)
						return None

				elif 'dimer' in acc_level:
					mof = wf.dimer()
					if mof is None:
						os.remove(working_cif_path)
						return None	

				elif acc_level == 'final_spe':
					mof = wf.final_spe()
					if mof is None:
						os.remove(working_cif_path)
						return None
					if 'dimer' in acc_levels[-2]:
						result_path = os.path.join(basepath,'results',refcode)
						newmodecar = os.path.join(result_path,acc_levels[-2],spin_label,'NEWMODECAR')
						newmodecar_spe = os.path.join(result_path,acc_level,spin_label,'NEWMODECAR')
						copyfile(newmodecar,newmodecar_spe)
						
				else:
					raise ValueError('Unsupported accuracy level')

			#***********SAVE and CONTINUE***********
			if same_spin:
				continue
			E_temp = mof.get_potential_energy()
			if E_temp < E:
				best_mof = deepcopy(mof)

		os.remove(working_cif_path)
		return best_mof

	def run_neb_screen(self,name,initial_atoms,final_atoms,n_images=4,cif_file=None,spin_levels=None,acc_levels=None,calculators=None,nupdowns=None):
		"""
		Run high-throughput NEB (followed by dimer) calculation
		Args:
			name (string): name of CIF file

			initial_atoms (ASE Atoms object): initial structure

			final_atoms (ASE Atoms object): final structure

			n_images (int): number of NEB images

			cif_file (string): name of CIF file to generate kpoints if
			set to 'Auto'

			spin_levels (list of strings): spin states to consider

			acc_levels (list of strings): accuracy levels to consider

			calculators (function): function to call respective calculator (defaults to
			automatically importing from pymofscreen.default_calculators.calcs)
						
		Returns:
			best_mof (ASE Atoms objects): ASE Atoms object for optimized
			MOF given by cif_file (lowest energy spin state)
		"""

		#Setup default parameters
		from pymofscreen.default_calculators import calcs
		if calculators is None:
			calculators = calcs
		self.calcs = calculators
		self.niggli = False
		basepath = self.basepath

		if spin_levels is None:
			spin_levels = ['high','low']
		if not isinstance(spin_levels,list):
			spin_levels = [spin_levels] 
		self.spin_levels = spin_levels

		if acc_levels is None:
			acc_levels = ['scf_test','cineb_lowacc','dimer_lowacc','dimer_medacc',
			'dimer_highacc','final_spe']
		if 'cineb_lowacc' not in acc_levels:
			acc_levels = ['cineb_lowacc']+acc_levels
		if 'scf_test' not in acc_levels:
			acc_levels = ['scf_test']+acc_levels
		self.acc_levels = acc_levels

		if nupdowns is None:
			nupdowns = [None]*len(spin_levels)
		elif nupdowns is not None and len(nupdowns) != len(spin_levels):
			raise ValueError('Length of nupdowns must equal spin_levels')
		self.nupdowns = nupdowns
		spin_labels = ['spin'+str(i+1) for i,j in enumerate(spin_levels)]
		self.spin_labels = spin_labels

		kpts_path = self.kpts_path
		if kpts_path == 'Auto' and cif_file is None:
			raise ValueError('Specify a CIF file if using automatic KPPA')

		#Ensure initial/final state have the same composition
		if initial_atoms.get_chemical_formula() != final_atoms.get_chemical_formula():
			pprint('SKIPPED: Atoms not identical between initial and final state')
			return None

		#Make sure MOF isn't running on other process
		working_cif_path = os.path.join(basepath,'working',name)
		if os.path.isfile(working_cif_path):
			pprint('SKIPPED '+name+': Running on another process')
			return None
		open(working_cif_path,'w').close()

		#Get the kpoints
		if kpts_path == 'Auto':
			kpts_lo, gamma = get_kpts(self,cif_file,'low')
			kpts_hi, gamma = get_kpts(self,cif_file,'high')
		else:
			kpts_lo, gamma = get_kpts(self,name.split('_TS')[0],'low')
			kpts_hi, gamma = get_kpts(self,name.split('_TS')[0],'high')
		kpts_dict = {}
		kpts_dict['kpts_lo'] = kpts_lo
		kpts_dict['kpts_hi'] = kpts_hi
		kpts_dict['gamma'] = gamma

		#Initialize variables
		E = np.inf
		mof = None
		prior_spin = None

		#for each spin level, optimize the structure
		for i, spin_level in enumerate(spin_levels):

			spin_label = spin_labels[i]
			self.spin_label = spin_label
			self.nupdown = nupdowns[i]
			pprint('***STARTING '+name+': '+spin_label+'***')

			#Check if spin state should be skipped
			if i > 0:
				prior_spin = spin_labels[i-1]
				if spin_levels[i-1] == 'high':
					skip_low_spin = check_if_skip_low_spin(self,mof,name,prior_spin)
					if skip_low_spin:
						pprint('Skipping low spin due to low magmoms in prior run')
						continue
			same_spin = False

			#Set up workflow object
			wf = workflows(self,name,kpts_dict,spin_level,prior_spin)

			#for each accuracy level, optimize structure
			for acc_level in acc_levels:

				if acc_level == 'scf_test':
					scf_pass = wf.scf_test(atoms_overwrite=initial_atoms,quick_test=True)
					if not scf_pass:
						os.remove(working_cif_path)
						return None
					if acc_levels[-1] == 'scf_test':
						os.remove(working_cif_path)
						return scf_pass

				elif acc_level == 'cineb_lowacc' and i == 0:
					neb_conv = wf.cineb_lowacc(initial_atoms,final_atoms,n_images)
					if not neb_conv:
						os.remove(working_cif_path)
						return None
					if acc_levels[-1] == 'cineb_lowacc':
						os.remove(working_cif_path)
						return neb_conv

				elif acc_level == 'cineb_lowacc' and i > 0:
					wf.run_i += 1
					continue

				elif 'dimer' in acc_level:
					mof = wf.dimer()
					if mof is None:
						os.remove(working_cif_path)
						return None

				elif acc_level == 'final_spe':
					mof = wf.final_spe()
					if mof is None:
						os.remove(working_cif_path)
						return None
					result_path = os.path.join(basepath,'results',name)
					newmodecar = os.path.join(result_path,acc_levels[-2],spin_label,'NEWMODECAR')
					newmodecar_spe = os.path.join(result_path,acc_level,spin_label,'NEWMODECAR')
					copyfile(newmodecar,newmodecar_spe)

				else:
					raise ValueError('Unsupported accuracy level')

				if acc_level == 'dimer_lowacc' and i > 0:
					is_new_spin = check_if_new_spin(self,mof,name,acc_level,spin_label)
					if not is_new_spin:
						same_spin = True
						break

			#***********SAVE and CONTINUE***********
			if same_spin:
				continue
			E_temp = mof.get_potential_energy()
			if E_temp < E:
				best_mof = deepcopy(mof)

		os.remove(working_cif_path)
		return best_mof