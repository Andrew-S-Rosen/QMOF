from ase.io import read, write
import os
import subprocess

basepath = 'CSD-opt'
cif_basepath = os.path.join(basepath, 'cifs')

# Append CIFs to an XYZ
cifs = os.listdir(os.path.join(cif_basepath, 'clean'))
cifs.sort()
bad_cifs = os.listdir(os.path.join(cif_basepath, 'issues'))
bad_cifs.sort()
refcodes = [cif.split('.cif')[0] for cif in cifs]
mofs = []
for cif in cifs:
    print('Appending... ' + cif)
    mofs.append(read(os.path.join(cif_basepath, 'clean', cif)))

# Write out XYZ and refcodes
new_name = 'CSD-clean-opt'
xyz_path = os.path.join(basepath, new_name+'.xyz')
refcodes_name = os.path.join(basepath, new_name+'-refcodes.csv')
if os.path.exists(xyz_path):
    os.remove(xyz_path)
write(xyz_path, mofs)
with open(refcodes_name, 'w') as w:
    for i, ref in enumerate(refcodes):
        if i != len(refcodes)-1:
            w.write(ref+',')
        else:
            w.write(ref)

# Zip things up
subprocess.Popen(['gzip', xyz_path])
# subprocess.Popen(['tar','-czvf',cif_basepath+'.tar.gz',cif_basepath])
# rmtree(cif_basepath)
