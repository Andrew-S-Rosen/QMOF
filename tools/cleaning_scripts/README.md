These tools can be used to clean up a set of CIFs obtained from the [MOF subset of the Cambridge Structural Database](https://sites.google.com/view/csdmofsubset/home). A brief description of each file is shown below:

`ase_formatter.py`: This script reads in a list of CIFs with ASE and writes them back out again. This seems a bit silly, but it's because the default formatting of the CIFs obtained from the CSD with ConQuest are not immediately suitable for use with a variety of Python packages like Pymatgen. I recommend running this script first.

`make_primitive.py`: This script converts a list of CIFs to their Niggli-reduced primitive cells. I recommend running this second.

`check_dist.py`: This script will check for small interatomic distances.

`lone_atom_check.py`: This script will check for lone atoms in the framework, as determined using Pymatgen's `CrystalNN` tool.

`deduplicate.py`: This script will de-duplicate a list of CIFs by using Pymatgen's `StructureMatcher` utility. 

`cifs_to_xyz.py`: This script converts a folder of CIFs to an ASE-formatted appended XYZ file and refcodes `.csv` file.

`xyz_to_cifs.py`: This script converts an ASE-formatted appended XYZ file to a folder of CIFs.
