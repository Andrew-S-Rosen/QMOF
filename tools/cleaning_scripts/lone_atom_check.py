from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis import local_env
from pymatgen import Structure
import os

folder = 'path/to/CIFs'
cifs = os.listdir(folder)
cifs.sort()
bad_list = []
for cif in cifs:
	mof = Structure.from_file(os.path.join(folder, cif))
	nn = local_env.CrystalNN()
	graph = StructureGraph.with_local_env_strategy(mof, nn)
	for j in range(len(mof)):
		nbr = graph.get_connected_sites(j)
		if not nbr:
			print('Lone atom issue:' + cif+'\n')
			bad_list.append(cif)
			break

with open('bad_cifs_lone_atom_check.gcd','w') as w:
	for bad_cif in bad_list:
		w.write(bad_cif+'\n')
