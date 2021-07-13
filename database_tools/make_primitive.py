from pymatgen.core import Structure
import os

folder = 'path/to/CIFs'
for entry in os.listdir(folder):
	structure = Structure.from_file(os.path.join(folder,entry),primitive=True)
	structure.to(filename=os.path.join(folder,entry))
