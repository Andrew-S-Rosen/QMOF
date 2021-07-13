from ase.io import read, write
import os

cif_path = 'path/to/CIFs'
cifs = os.listdir(cif_path)
cifs.sort()

refcodes = []
mofs = []
for cif in cifs:
	refcodes.append(cif.split('.cif')[0])
	mofs.append(read(os.path.join(cif_path, cif)))
write('mofs.xyz', mofs)

with open('refcodes.csv','w') as w:
	for refcode in refcodes:
		if refcode == refcodes[-1]:
			w.write(refcode)
		else:
			w.write(refcode+',')