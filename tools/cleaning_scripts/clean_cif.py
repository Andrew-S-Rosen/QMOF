from ase.io import read, write
import os

cif_path = 'path/to/CIFs'
cifs = os.listdir(cif_path)
cifs.sort()

for cif in cifs:
    mof = read(os.path.join(cif_path, cif))
    write(os.path.join(cif_path, cif), mof)
