import os
import numpy as np
from copy import deepcopy
from ase.io import read
from pymofscreen.compute_environ import get_nprocs
from pymofscreen.writers import pprint, write_success, write_errors
from pymofscreen.janitor import manage_restart_files, clean_files, vtst_cleanup
from pymofscreen.runner import mof_run, prep_next_run, prep_new_run, mof_bfgs_run
from pymofscreen.cif_handler import cif_to_mof
from pymofscreen.magmom_handler import set_initial_magmoms, continue_magmoms
from pymofscreen.error_handler import get_warning_msgs
from pymofscreen.vtst_handler import nebmake, neb2dim, nebef

class workflows():
	"""
	This class constructs a workflow for a given calculation stage
	"""

	def __init__(self,screener,cif_file,kpts_dict,spin_level,prior_spin=None,
		vasp_files=None):
		"""
		Initialize variables that should be used on all MOFs in a database
		Args:
			screener (class): pymofscreen.screen.screener class

			cif_file (string): name of CIF file

			kpts_dict (dict): dictionary containing kpoint and gamma information

			spin_level (string): name of spin level

			prior_spin (string): name of previous spin level (if applicable)
			
			vasp_files (list of strings): VASP files to save
		"""
		self.cif_file = cif_file
		self.kpts_dict = kpts_dict
		self.spin_level = spin_level
		self.acc_levels = screener.acc_levels
		self.spin_label = screener.spin_label
		if vasp_files is None:
			self.vasp_files = ['INCAR','POSCAR','KPOINTS','POTCAR','OUTCAR',
		'CONTCAR','CHGCAR','WAVECAR','EIGENVAL']
		self.calc_swaps = []
		self.run_i = 0
		if '.cif' in cif_file:
			self.refcode = cif_file.split('.cif')[0]
		elif 'POSCAR_' in cif_file:
			self.refcode = cif_file.split('POSCAR_')[1]
		else:
			self.refcode = cif_file
		self.stdout_file = screener.stdout_file
		self.mofpath = screener.mofpath
		self.submit_script = screener.submit_script
		self.basepath = screener.basepath
		self.niggli = screener.niggli
		self.calcs = screener.calcs
		self.nprocs, self.ppn = get_nprocs(self.submit_script)
		self.nupdown = screener.nupdown

		clean_files(self.vasp_files+['CHG','AECCAR0','AECCAR1','AECCAR2'])

		results_partial_paths = []
		error_partial_paths = []
		error_outcar_paths = []
		outcar_paths = []
		for acc_level in self.acc_levels:
			results_partial_paths.append(os.path.join(self.basepath,'results',
				self.refcode,acc_level))
			error_partial_paths.append(os.path.join(self.basepath,
				'errors',self.refcode,acc_level))
		self.results_partial_paths = results_partial_paths
		self.error_partial_paths = error_partial_paths
		for results_partial_path in results_partial_paths:
			outcar_paths.append(os.path.join(results_partial_path,self.spin_label,
				'OUTCAR'))
		for error_partial_path in error_partial_paths:
			error_outcar_paths.append(os.path.join(error_partial_path,
				self.spin_label,'OUTCAR'))
		self.outcar_paths = outcar_paths
		self.error_outcar_paths = error_outcar_paths
		self.prior_spin = prior_spin
		if prior_spin is None:
			self.spin1_final_mof_path = None
		else:
			self.spin1_final_mof_path = os.path.join(results_partial_paths[-1],
				prior_spin,'OUTCAR')
				
	def scf_test(self,atoms_overwrite=None,quick_test=False):
		"""
		Run SCF test job to check for errors
		Returns:
			scf_pass (bool): True if passed SCF test
		"""
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_level = self.spin_level
		spin_label = self.spin_label
		cif_file = self.cif_file
		mofpath = self.mofpath
		spin1_final_mof_path = self.spin1_final_mof_path
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = self.acc_levels[self.run_i]
		niggli = self.niggli
		calcs = self.calcs
		
		if not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			if atoms_overwrite:
				mof = deepcopy(atoms_overwrite)
			else:
				if spin1_final_mof_path is None:
					mof = cif_to_mof(os.path.join(mofpath,cif_file),niggli)
				else:
					mof = read(spin1_final_mof_path)
			mof = set_initial_magmoms(mof,spin_level)
			if quick_test:
				self.calc_swaps.append('nelm=5')
				self.calc_swaps.append('lwave=False')
			pprint('Running '+spin_label+', '+acc_level)
			mof, self.calc_swaps = mof_run(self,mof,calcs('scf_test'),kpts_hi)
			if quick_test:
				self.calc_swaps.remove('nelm=5')
				self.calc_swaps.remove('lwave=False')
			if mof is not None and mof.calc.scf_converged:
				write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return False
		warnings = get_warning_msgs(outcar_paths[self.run_i-1])
		self.calc_swaps.extend(warnings)

		return True

	def isif2_lowacc(self):
		"""
		Run low accuracy ISIF2
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_level = self.spin_level
		spin_label = self.spin_label
		cif_file = self.cif_file
		mofpath = self.mofpath
		prior_spin = self.prior_spin
		spin1_final_mof_path = self.spin1_final_mof_path
		kpts_lo = self.kpts_dict['kpts_lo']
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = acc_levels[self.run_i]
		niggli = self.niggli
		calcs = self.calcs
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)
		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			if prior_spin is None:
				mof = cif_to_mof(os.path.join(mofpath,cif_file),niggli)
			else:
				mof = read(spin1_final_mof_path)
			if sum(kpts_lo) == 3 and sum(kpts_hi) > 3:
				clean_files(['CHGCAR','WAVECAR'])
			else:
				manage_restart_files(prior_results_path)
			mof = set_initial_magmoms(mof,spin_level)
			fmax = 5.0
			pprint('Running '+spin_label+', '+acc_level)
			mof, dyn, self.calc_swaps = mof_bfgs_run(self,mof,calcs('ase_bfgs'),
				kpts_lo,fmax=fmax)
			if mof is not None and dyn:
				loop_i = 0
				converged = False
				clean_files(['opt.traj'])
				while mof is not None and loop_i < 4 and not converged and mof.calc.scf_converged:
					if loop_i == 2 and 'fire' not in self.calc_swaps and 'zbrent' not in self.calc_swaps:
						self.calc_swaps.append('fire')
					mof = read('OUTCAR')
					mof = continue_magmoms(mof,'INCAR')
					mof, self.calc_swaps = mof_run(self,mof,
						calcs('isif2_lowacc'),kpts_lo)
					if mof is None:
						break
					converged = mof.calc.converged
					loop_i += 1
			if 'fire' in self.calc_swaps:
				self.calc_swaps.remove('fire')
			if mof is not None and mof.calc.scf_converged and mof.calc.converged:
				write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof

	def isif2_medacc(self):
		"""
		Run medium accuracy ISIF2
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_label  = self.spin_label
		kpts_lo = self.kpts_dict['kpts_lo']
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = acc_levels[self.run_i]
		calcs = self.calcs
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)

		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			mof = prep_new_run(self)
			if sum(kpts_lo) == 3 and sum(kpts_hi) > 3:
				clean_files(['CHGCAR','WAVECAR'])
			else:
				manage_restart_files(prior_results_path)
			pprint('Running '+spin_label+', '+acc_level)
			mof,self.calc_swaps = mof_run(self,mof,calcs('isif2_medacc'),kpts_hi)
			if mof is not None and mof.calc.scf_converged and mof.calc.converged:
				write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof

	def isif2_highacc(self):
		"""
		Run high accuracy ISIF2
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_label = self.spin_label
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = acc_levels[self.run_i]
		calcs = self.calcs
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)

		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			mof = prep_new_run(self)
			manage_restart_files(prior_results_path)
			pprint('Running '+spin_label+', '+acc_level)
			mof,self.calc_swaps = mof_run(self,mof,calcs('isif2_highacc'),kpts_hi)
			if mof is not None and mof.calc.scf_converged and mof.calc.converged:
				if 'large_supercell' in self.calc_swaps:
					self.calc_swaps.remove('large_supercell')
					mof = read('OUTCAR')
					mof = continue_magmoms(mof,'INCAR')
					mof, self.calc_swaps = mof_run(self,mof,calcs('isif2_highacc'),kpts_hi)
					if mof is not None and mof.calc.scf_converged and mof.calc.converged:
						write_success(self)
					else:
						write_errors(self,mof)
				else:
					write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None
			
		return mof

	def isif3_lowacc(self):
		"""
		Run low accuracy ISIF3
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_label = self.spin_label
		kpts_lo = self.kpts_dict['kpts_lo']
		acc_level = acc_levels[self.run_i]
		calcs = self.calcs
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)
		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			mof = prep_new_run(self)
			converged = False
			loop_i = 0
			n_runs = 15
			manage_restart_files(prior_results_path)
			while not converged and loop_i < n_runs:
				if loop_i == 10 and 'fire' not in self.calc_swaps and 'zbrent' not in self.calc_swaps:
					self.calc_swaps.append('fire')
				pprint('Running '+spin_label+', '+acc_level+': iteration '+str(loop_i)+'/'+str(n_runs-1))
				mof,self.calc_swaps = mof_run(self,mof,calcs('isif3_lowacc'),kpts_lo)
				if mof is None:
					break
				converged = mof.calc.converged
				mof = read('OUTCAR')
				mof = continue_magmoms(mof,'INCAR')
				loop_i += 1
			if 'fire' in self.calc_swaps:
				self.calc_swaps.remove('fire')
			if mof is not None and converged:
				write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof

	def isif3_highacc(self):
		"""
		Run high accuracy ISIF3
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_label = self.spin_label
		kpts_lo = self.kpts_dict['kpts_lo']
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = acc_levels[self.run_i]
		calcs = self.calcs
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)

		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			mof = prep_new_run(self)
			converged = False
			loop_i = 0
			n_runs = 15
			V_diff = np.inf
			V_cut = 0.01
			V0 = mof.get_volume()
			if sum(kpts_lo) == 3 and sum(kpts_hi) > 3:
				clean_files(['CHGCAR','WAVECAR'])
			else:
				manage_restart_files(prior_results_path)
			while (not converged or V_diff > V_cut) and loop_i < n_runs:
				if loop_i == 10 and 'fire' not in self.calc_swaps and 'zbrent' not in self.calc_swaps:
					self.calc_swaps.append('fire')
				pprint('Running '+spin_label+', '+acc_level+': iteration '+str(loop_i)+'/'+str(n_runs-1))
				mof,self.calc_swaps = mof_run(self,mof,calcs('isif3_highacc'),
					kpts_hi)
				if mof is None:
					break
				if loop_i > 0:
					converged = mof.calc.converged
				mof = read('OUTCAR')
				V = mof.get_volume()
				mof = continue_magmoms(mof,'INCAR')
				if loop_i > 0:
					V_diff = np.abs((V-V0))/V0
				V0 = V
				loop_i += 1
			if mof is not None and converged and V_diff <= V_cut and 'large_supercell' in self.calc_swaps:
				self.calc_swaps.append('nsw=100')
				self.calc_swaps.remove('large_supercell')
				pprint('Running '+spin_label+', '+acc_level+' (LREAL=False)')
				mof,self.calc_swaps = mof_run(self,mof,calcs('isif3_highacc'),
					kpts_hi)
				self.calc_swaps.remove('nsw=100')
				if mof is not None and mof.calc.converged:
					write_success(self)
				else:
					write_errors(self,mof)
			else:
				write_errors(self,mof)
				if mof is not None and V_diff > V_cut:
					pprint('^ Change in V of '+str(V_diff)+' percent')
			if 'fire' in self.calc_swaps:
				self.calc_swaps.remove('fire')
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof

	def final_spe(self):
		"""
		Run final single point
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_label = self.spin_label
		kpts_hi = self.kpts_dict['kpts_hi']
		acc_level = acc_levels[self.run_i]
		calcs = self.calcs
		self.calc_swaps = []
		prior_results_path = os.path.join(self.results_partial_paths[self.run_i-1],spin_label)

		if os.path.isfile(outcar_paths[self.run_i-1]) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			mof = prep_new_run(self)
			manage_restart_files(prior_results_path)
			pprint('Running '+spin_label+', '+acc_level)
			mof,self.calc_swaps = mof_run(self,mof,calcs('final_spe'),kpts_hi)
			if mof is not None and mof.calc.scf_converged:
				write_success(self)
			else:
				write_errors(self,mof)
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof

	def cineb_lowacc(self,initial_atoms,final_atoms,n_images):
		"""
		Run CI-NEB low accuracy calculation
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		spin_level = self.spin_level
		kpts_lo = self.kpts_dict['kpts_lo']
		calcs = self.calcs
		nprocs = self.nprocs
		pwd = os.getcwd()
		partial_path = self.results_partial_paths[self.run_i]
		data_path = os.path.join(partial_path,'neb.tar.gz')
		partial_error_path = self.error_partial_paths[self.run_i]
		error_data_path = os.path.join(partial_error_path,'neb.tar.gz')
		neb_conv = False
		if nprocs % n_images != 0:
			raise ValueError(str(nprocs)+' procs not divisible by '+str(n_images))
		if not os.path.isfile(data_path) and not os.path.isfile(error_data_path):
			if initial_atoms.get_chemical_formula() != final_atoms.get_chemical_formula():
				raise ValueError('POSCAR1 and POSCAR2 must have same atoms')
			nebmake(initial_atoms,final_atoms,n_images)
			initial_atoms = set_initial_magmoms(initial_atoms,spin_level)
			pprint('Running CI-NEB (pre-dimer)')
			initial_atoms,self.calc_swaps = mof_run(self,initial_atoms,calcs('cineb_lowacc'),kpts_lo,images=n_images)
			ediffg = calcs('cineb_lowacc').exp_params['ediffg']
			neb_conv = nebef(ediffg)
			os.chdir(pwd)
			if neb_conv:
				write_success(self,neb=True)
			else:
				write_errors(self,initial_atoms,neb=True)
			vtst_cleanup()
		elif os.path.isfile(data_path):
			pprint('COMPLETED: CI-NEB (pre-dimer)')
			neb_conv = True
		self.run_i += 1
		if not neb_conv:
			pprint('Skipping rest because of errors')
			return False

		return neb_conv

	def dimer(self):
		"""
		Run dimer
		Returns:
			mof (ASE Atoms object): updated ASE Atoms object
		"""
		acc_levels = self.acc_levels
		outcar_paths = self.outcar_paths
		error_outcar_paths = self.error_outcar_paths
		spin_level = self.spin_level
		spin_label = self.spin_label
		prior_spin = self.prior_spin
		acc_level = acc_levels[self.run_i]
		prior_acc_level = acc_levels[self.run_i-1]
		results_partial_paths = self.results_partial_paths
		pwd = os.getcwd()
		if 'lowacc' in acc_level:
			kpts = self.kpts_dict['kpts_lo']
		else:
			kpts_lo = self.kpts_dict['kpts_lo']
			kpts = self.kpts_dict['kpts_hi']
		calcs = self.calcs
		if 'neb' in prior_acc_level and prior_spin is None:
			prior_results_path = os.path.join(results_partial_paths[self.run_i-1])
			prior_results_file = os.path.join(prior_results_path,'neb.tar.gz')
		elif 'lowacc' in acc_level and prior_spin is not None:
			prior_results_path = os.path.join(results_partial_paths[-1],prior_spin)
			prior_results_file = os.path.join(prior_results_path,'OUTCAR')
		else:
			prior_results_file = outcar_paths[self.run_i-1]
			prior_results_path = os.path.join(results_partial_paths[self.run_i-1],spin_label)
		if os.path.isfile(prior_results_file) and not os.path.isfile(outcar_paths[self.run_i]) and not os.path.isfile(error_outcar_paths[self.run_i]):
			if 'scf_test' in prior_acc_level:
				mof = prep_new_run(self)
				manage_restart_files(prior_results_path,dimer=False)
			elif 'neb' in prior_acc_level and prior_spin is None:
				manage_restart_files(prior_results_path,neb=True)
				mof = neb2dim()
				mof = set_initial_magmoms(mof,spin_level)
			elif 'lowacc' in acc_level and prior_spin is not None:
				mof = read(prior_results_file)
				mof = set_initial_magmoms(mof,spin_level)
				manage_restart_files(prior_results_path,dimer=True,wavechg=False)
			else:
				mof = prep_new_run(self)
				manage_restart_files(prior_results_path,dimer=True)
				if 'medacc' in acc_level and sum(kpts_lo) == 3 and sum(kpts) > 3:
					clean_files(['CHGCAR','WAVECAR'])
			if 'highacc' in acc_level and 'large_supercell' in self.calc_swaps:
				self.calc_swaps.remove('large_supercell')
			pprint('Running '+spin_label+', '+acc_level)
			mof,self.calc_swaps = mof_run(self,mof,calcs(acc_level),kpts)
			if mof is not None and mof.calc.scf_converged and mof.calc.converged:
				write_success(self)
			else:
				write_errors(self,mof)
			vtst_cleanup()
		elif os.path.isfile(outcar_paths[self.run_i]):
			pprint('COMPLETED: '+spin_label+', '+acc_level)
		mof = prep_next_run(self)
		os.chdir(pwd)
		if mof is None:
			pprint('Skipping rest because of errors')
			return None

		return mof