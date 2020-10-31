from ase.io import read, write
import os

cif_path_base = 'CSD-opt'

# Append CIFs to an XYZ
cifs = os.listdir(os.path.join(cif_path_base, 'clean'))
cifs.sort()
bad_cifs = os.listdir(os.path.join(cif_path_base, 'issues'))
bad_cifs.sort()
refcodes = [cif.split('.cif')[0] for cif in cifs]
mofs = []
for cif in cifs:
    print('Appending... ' + cif)
    mofs.append(read(os.path.join(cif_path_base, 'clean', cif)))

# Write out XYZ and refcodes
new_name = 'CSD-clean-opt'
xyz_name = os.path.join(cif_path_base, new_name+'.xyz')
refcodes_name = os.path.join(cif_path_base, new_name+'-refcodes.csv')
write(xyz_name, mofs)
with open(refcodes_name, 'w') as w:
    for i, ref in enumerate(refcodes):
        if i != len(refcodes)-1:
            w.write(ref+',')
        else:
            w.write(ref)
os.system('gzip '+xyz_name)
