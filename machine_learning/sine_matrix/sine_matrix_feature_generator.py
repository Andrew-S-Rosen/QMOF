from matminer.featurizers.structure import SineCoulombMatrix
from ase.io import read
from pymatgen.io import ase as pm_ase
import numpy as np
import pandas as pd

# Settings
xyz_path = 'geometries.xyz' # appended list of XYZs (length N)
refcodes_path = 'refcodes.csv' # refcode for each structure (length N)
max_atoms = np.inf # specify if you want an upper max on the # of atoms to consider

#---------------------------------------
# Read in structures
ase_mofs = read(xyz_path, index=':')
refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str)
adaptor = pm_ase.AseAtomsAdaptor()
pm_mofs = [adaptor.get_structure(ase_mof) for ase_mof in ase_mofs if len(ase_mof) <= max_atoms]

# Initialize feature object
featurizer = SineCoulombMatrix()
featurizer.fit(pm_mofs)
features = featurizer.feature_labels()
df = pd.DataFrame(columns=features)

# Get features
for i, pm_mof in enumerate(pm_mofs):
	print('Generating fingerprint: '+str(i))
	fingerprint = featurizer.featurize(pm_mof)
	refcode = refcodes[i]
	df.loc[refcode, :] = fingerprint

# Export features
df.index.name = 'MOF'
df.to_csv('sine_matrix_fingerprints.csv', index=True)
