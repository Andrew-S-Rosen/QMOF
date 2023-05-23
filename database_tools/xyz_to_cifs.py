from ase.io import read, write
import numpy as np
import os

# Converts an appended .xyz to a folder of CIFs

# Relevant filenames
refcode_path = r'/path/to/refcodes.csv' # path to refcodes
xyz_path = r'/path/to/geometries.xyz' # path to XYZ of all structures
new_folder = r'cifs' # path to new folder store CIFs

# ----------------------
refs = np.genfromtxt(refcode_path,delimiter=',',dtype=str)
mofs = read(xyz_path,index=':')

if not os.path.exists(new_folder):
	os.mkdir(new_folder)
for i, mof in enumerate(mofs):
	write(os.path.join(new_folder, f'{refs[i]}.cif'), mof)
