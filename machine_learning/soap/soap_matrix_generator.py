from dscribe.descriptors import SOAP
from ase.io import read
import numpy as np
from scipy.sparse import save_npz
import os

# Settings
basepath = os.getcwd()  # base path where avg SOAP matrices will be stored
soap_params = {'rcut': 4.0, 'sigma': 0.1, 'nmax': 9, 'lmax': 9,
			   'rbf': 'gto', 'average': 'off', 'crossover': True}
xyz_path = 'structures.xyz' # appended XYZ of structures (length N)
refcodes_path = 'refcodes.csv' # refcode for each structure (length N)

#---------------------------------------
# Make folder if not present
if not os.path.exists(os.path.join(basepath, 'soap_matrices')):
	os.mkdir(os.path.join(basepath, 'soap_matrices'))

# Read in structures
structures = read(xyz_path, index=':')

# Read in refcodes
refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str).tolist()
if len(refcodes) != len(structures):
	raise ValueError('Mismatch in refcodes and num. structures')

# Get unique species
species = []
for structure in structures:
	syms = np.unique(structure.get_chemical_symbols())
	species.extend([sym for sym in syms if sym not in species])
species.sort()

# Initialize SOAP
soap = SOAP(
	species=species,
	periodic=True,
	sigma=soap_params['sigma'],
	rcut=soap_params['rcut'],
	nmax=soap_params['nmax'],
	lmax=soap_params['lmax'],
	rbf=soap_params['rbf'],
	average=soap_params['average'],
	crossover=soap_params['crossover'],
	sparse=True
)

# Make SOAP fingerprints
for i, structure in enumerate(structures):
	refcode = refcodes[i]
	soap_filename = os.path.join(
		basepath, 'soap_matrices', 'soap_'+refcode+'.npz')
	if os.path.exists(soap_filename):
		continue
	soap_matrix = soap.create(structure)
	save_npz(soap_filename, soap_matrix)
