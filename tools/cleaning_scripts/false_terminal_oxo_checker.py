from ase import neighborlist
from ase.io import read
import os
import numpy as np
import warnings

# Path to CIFs
p = r'/path/to/cifs'

# Metals that should not have terminal oxo ligands
metals = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr',
          'Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra',
          'Sc', 'Y', 'La', 'Ac',
          'Ti', 'Zr', 'Hf',
          'Mn',
          'Fe',
          'Co',
          'Ni',
          'Cu', 'Ag',
          'Zn', 'Cd',
          'Al', 'Ga', 'In', 'Tl']

# Get CIFs from folder
cifs = os.listdir(p)
cifs = [cif for cif in cifs if '.cif' in cif]
cifs.sort()

# Check every CIF
for cif in cifs:

    bad = False

    # Read in CIF, ignoring ASE warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        structure = read(os.path.join(p, cif))

    # Get list of atomic symbols
    syms = np.array(structure.get_chemical_symbols())

    # Is one of the specified metals in this MOF
    in_metal_list = False
    for sym in syms:
        if sym in metals:
            in_metal_list = True
            break
    if not in_metal_list:
        continue

    # Generate connectivity matrix
    cutoff = neighborlist.natural_cutoffs(structure)
    nl = neighborlist.NeighborList(
        cutoff, self_interaction=False, bothways=True)
    nl.update(structure)

    # Detect terminal oxo site
    for i, sym in enumerate(syms):

        # If the site is a specified metal...
        if sym in metals:

            # Get neighbors to metal
            bonded_atom_indices = nl.get_neighbors(i)[0]
            if bonded_atom_indices is None:
                continue
            bonded_atom_symbols = syms[bonded_atom_indices]

            # Find bound O atoms
            for j, bonded_atom_symbol in enumerate(bonded_atom_symbols):

                # Determine if it is a terminal oxo
                if bonded_atom_symbol == 'O':
                    cn = len(nl.get_neighbors(bonded_atom_indices[j])[0])
                    if cn == 1:
                        bad = True
                        print('Missing H on terminal oxo:' + cif+'\n')

                if bad:
                    break
        if bad:
            break
