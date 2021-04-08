from ase.io import read
import os
import numpy as np

cutoff = 0.75  # interatomic distance threshold
folder = 'path/to/CIFs'
bad_list = []
for cif in os.listdir(folder):
	mof = read(os.path.join(folder, cif))
	d = mof.get_all_distances()
	upper_diag = d[np.triu_indices_from(d, k=1)]
	for entry in upper_diag:
		if entry < cutoff:
			print('Interatomic distance issue:' + cif.split('.')[0])
			bad_list.append(cif)
			break

with open('bad_cifs_distance_check.gcd','w') as w:
	for bad_cif in bad_list:
		w.write(bad_cif+'\n')
