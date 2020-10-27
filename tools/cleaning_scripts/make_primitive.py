import pymatgen as pm
import os

folder = 'path/to/CIFs'
for entry in os.listdir(folder):
	structure = pm.Structure.from_file(os.path.join(folder,entry),primitive=True)
	structure.to(filename=os.path.join(folder,entry))