from ase import neighborlist
from ase.io import read
import os
import numpy as np
import warnings

# Metals that should not have terminal oxo ligands
metals = ['Li','Na','K','Rb','Cs','Fr',
	'Be','Mg','Ca','Sr','Ba','Ra',
	'Sc','Y','La','Ac',
	'Ti','Zr','Hf',
	'Mn',
	'Fe',
	'Co',
	'Ni',
	'Cu','Ag',
	'Zn','Cd',
	'Al','Ga','In','Tl']

# Path to CIFs
p = r'/path/to/CIFs'

# Get CIFs from folder
cifs = os.listdir(p)
cifs = [cif for cif in cifs if '.cif' in cif]
cifs.sort()

# Check every CIF
bad_list = []
for cif in cifs:

	bad = False

	# Read in CIF, ignoring ASE warnings
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		structure = read(os.path.join(p,cif))

	# Get list of atomic symbols
	syms = np.array(structure.get_chemical_symbols())

	# Is one of the specified metals in this MOF
	if not any(item in syms for item in metals):
		continue

	# Initialize neighbor list
	cutoff = neighborlist.natural_cutoffs(structure)
	nl = neighborlist.NeighborList(cutoff,self_interaction=False,bothways=True)
	nl.update(structure)

	# For every site, check if it is a terminal metal-oxo
	for i, sym in enumerate(syms):

		# Confirm site is in pre-specified metal list
		if sym not in metals:
			continue

		# Get neighbors to metal
		bonded_atom_indices = nl.get_neighbors(i)[0]
		if bonded_atom_indices is None:
			continue
		bonded_atom_symbols = syms[bonded_atom_indices]

		# For every neighbor, check if it's a terminal oxo
		for j, bonded_atom_symbol in enumerate(bonded_atom_symbols):

			# Confirm neighbor is an O atom
			if bonded_atom_symbol != 'O':
				continue

			# Check if the O atom is only bound to the metal
			cn = len(nl.get_neighbors(bonded_atom_indices[j])[0])
			if cn == 1:
				bad = True
				print('Missing H on terminal oxo: ' + cif)
				bad_list.append(cif)

			if bad:
				break
		if bad:
			break

with open('bad_cifs_oxo_check.gcd','w') as w:
	for bad_cif in bad_list:
		w.write(bad_cif + '\n')
