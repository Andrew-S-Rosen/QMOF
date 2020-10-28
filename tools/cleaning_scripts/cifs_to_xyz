from ase.io import read, write
import os

cif_path = 'path/to/CIFs'
cifs = os.listdir(cif_path)
cifs.sort()

mofs = []
for cif in cifs:
    mofs.append(read(os.path.join(cif_path, cif)))
write('mofs.xyz', mofs)
