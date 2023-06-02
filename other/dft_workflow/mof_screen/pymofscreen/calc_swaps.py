from pymofscreen.default_calculators import defaults

def update_calc(calc,calc_swaps):
	"""
	Update a calculator based on pre-defined "swaps"
	Args:
		calc (dictionary): ASE Vasp calculators dictionary

		calc_swaps (list): list of pre-existing calc swaps

	Returns:
		calc (dictionary): updated ASE Vasp calculator

		calc_swaps (list): updated list of swaps
	"""
	for swap in calc_swaps:

		swap.replace(' ','')

		if swap == 'large_supercell':
			calc.special_params['lreal'] = 'Auto'

		elif swap == 'zbrent':
			calc.int_params['ibrion'] = 3
			calc.exp_params['ediff'] = 1e-6
			calc.int_params['nelmin'] = 8
			calc.int_params['iopt'] = 7
			calc.float_params['potim'] = 0

		elif swap in ['dentet', 'grad_not_orth']:
			calc.int_params['ismear'] = 0
			calc.string_params['algo'] = 'Normal'

		elif swap == 'edddav':
			calc.string_params['algo'] = 'All'

		elif swap == 'inv_rot_mat':
			calc.exp_params['symprec'] = 1e-8

		elif swap in ['subspacematrix', 'real_optlay', 'rspher', 'nicht_konv']:
			calc.special_params['lreal'] = False
			calc.string_params['prec'] = 'Accurate'

		elif swap in ['tetirr', 'incorrect_shift']:
			calc.input_params['gamma'] = True

		elif swap in ['pricel', 'sgrcon', 'ibzkpt']:
			calc.exp_params['symprec'] = 1e-8
			calc.int_params['isym'] = 0

		elif swap == 'amin':
			calc.float_params['amin'] = 0.01

		elif swap in ['pssyevx', 'eddrmm']:
			calc.string_params['algo'] = 'Normal'

		elif swap == 'zheev':
			calc.string_params['algo'] = 'Exact'

		elif swap == 'elf_kpar':
			calc.int_params['kpar'] = 1

		elif swap == 'rhosyg':
			calc.exp_params['symprec'] = 1e-4
			calc.int_params['isym'] = 0

		elif swap == 'posmap':
			calc.exp_params['symprec'] = 1e-6

		elif 'pwave' in swap:
			calc.int_params['istart'] = 0

		elif 'sigma=' in swap:
			calc.float_params['sigma'] = float(swap.split('=')[-1])

		elif 'nbands=' in swap:
			calc.int_params['nbands'] = int(swap.split('=')[-1])

		elif 'potim=' in swap:
			calc.float_params['potim'] = float(swap.split('=')[-1])

		elif 'nsw=' in swap:
			calc.int_params['nsw'] = int(swap.split('=')[-1])

		elif 'nelm=' in swap:
			calc.int_params['nelm'] = int(swap.split('=')[-1])

		elif 'ibrion=' in swap:
			calc.int_params['ibrion'] = int(swap.split('=')[-1])

		elif 'istart=' in swap:
			calc.int_params['istart'] = int(swap.split('=')[-1])

		elif 'algo=' in swap:
			calc.string_params['algo'] = swap.split('=')[-1]

		elif 'iopt=' in swap:
			calc.int_params['iopt'] = int(swap.split('=')[-1])

		elif 'isif=' in swap:
			calc.int_params['isif'] = int(swap.split('=')[-1])

		elif 'lreal=' in swap:
			swap_val = swap.split('=')[1].lower()
			if swap_val == 'auto':
				calc.special_params['lreal'] = 'Auto'
			elif swap_val == 'false':
				calc.special_params['lreal'] = False
			elif swap_val == 'true':
				calc.special_params['lreal'] = True

		elif 'fire' in swap:
			calc.int_params['ibrion'] = 3
			calc.int_params['iopt'] = 7
			calc.float_params['potim'] = 0

		elif 'lwave=' in swap:
			swap_val = swap.split('=')[-1].lower()
			if swap_val == 'false':
				calc.bool_params['lwave'] = False

			elif swap_val == 'true':
				calc.bool_params['lwave'] = True
		elif 'nelect=' in swap:
			swap_val = swap.split('=')[-1].lower()
			calc.float_params['nelect'] = float(swap.split('=')[-1])

		elif swap not in ['brions', 'too_few_bands']:
			raise ValueError('Unknown calc swap')

	return calc, calc_swaps

def check_nprocs(n_atoms,nprocs,ppn):
	"""
	Reduce processors if the structure is too small
	Args:
		n_atoms (int): number of atoms in structure

		nprocs (int): total number of processors

		ppn (int): processors per node
		
	Returns:
		nprocs (int): updated total number of processors
	"""

	lower = False
	while n_atoms < nprocs/2:
		if nprocs == ppn:
			lower = True
			break
		nprocs -= ppn
	if lower == True:
		while n_atoms < nprocs/2:
			if nprocs <= 2:
				break
			nprocs -= 2
		defaults['ncore'] = nprocs

	return nprocs