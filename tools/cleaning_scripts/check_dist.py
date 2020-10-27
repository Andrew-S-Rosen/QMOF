from ase.io import read
import os
import numpy as np

cutoff = 0.75  # interatomic distance threshold
folder = 'path/to/CIFs'
for cif in os.listdir(folder):
    mof = read(os.path.join(folder, cif))
    d = mof.get_all_distances()
    upper_diag = d[np.triu_indices_from(d, k=1)]
    for entry in upper_diag:
        if entry < cutoff:
            print('Interatomic distance issue:' + cif.split('.')[0])
            break
