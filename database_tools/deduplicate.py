from pymatgen.core import Structure
from pymatgen.analysis import structure_matcher
import os

folder = 'folder/of/cifs' #folder of CIFs to de-duplicate
new_folder = 'new/folder/to/save/cifs' #folder to save only unique CIFs

mofs = [] #initialize list to store Pymatgen structures
entries = os.listdir(folder) #get all CIFs
entries.sort() #alphabetical sort

#for every CIF, store Pymatgen Structure in list
for entry in entries:

	if '.cif' not in entry:
		continue
	
	#read CIF
	mof_temp = Structure.from_file(os.path.join(folder,entry),primitive=False)

	#tag Pymatgen structure with its name
	mof_temp.name = entry
	mofs.append(mof_temp)

#Initialize StructureMatcher
sm = structure_matcher.StructureMatcher(primitive_cell=True)

#Group structures
groups = sm.group_structures(mofs)
print(str(len(groups))+' unique out of '+str(len(entries))+' total')

#Write out set of only unique CIFs
if not os.path.exists(new_folder):
	os.mkdir(new_folder)
for group in groups:
	mof_temp = group[0]
	mof_temp.to(filename=os.path.join(new_folder,mof_temp.name))
