# QMOF Database

<img src=logo.png>

## Overview
This GitHub repository is the landing page for the Quantum MOF (QMOF) database – a publicly available dataset of quantum-chemical properties for 14,000+ metal–organic framework structures. The QMOF database is described in detail in DOI: [10.26434/chemrxiv.13147616](https://doi.org/10.26434/chemrxiv.13147616).

## Purpose of this GitHub Page
The data underlying the QMOF database is hosted on Figshare and linked in the "Accessing the QMOF Database" subsection below. Nonetheless, this GitHub page serves several purposes:

1. As detailed in the "Scripts and Tools" subsection below, this GitHub page includes supplementary files that can be used to carry out the machine learning analyses in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

2. It allows for open, public discussions via the GitHub [Issues](https://github.com/arosen93/QMOF/issues) tab. While any issues can certainly be raised here, I also welcome comments, suggestions, or other forms of open dialogue in the Issues tracker.

3. Occasionally, I may use the [Projects](https://github.com/arosen93/QMOF/projects) tab to share any planned updates to the database, once they are in a state to be publicly announced.

4. If you have developed direct extensions, modifications, or subsets related to the QMOF database, I am more than happy to include a link to your work on this GitHub page so that all QMOF database resources can be linked to one another in a single place.

## Accessing the QMOF Database
The most up-to-date version of the QMOF database can be accessed on Figshare: [**QMOF Database Download**](https://doi.org/10.6084/m9.figshare.13147324).

The individual files uploaded to Figshare are described in greater detail below.

1. `qmof_database.zip`: This contains the structures and tabulated properties of all materials in the QMOF database. This is likely the file you're looking for, and you'll probably be most interested in the CSD-14204-opt directory inside the `.zip` file.

2. `vasp_files.zip`: This contains the VASP input and output files used in constructing the QMOF database. Most users do not need this raw data, but it is available if you wish to access it. For the POTCAR selection, see Table S2 of the Supporting Information. If you require data for the intermediate stages of the workflow, please email me directly.

3. `soap_kernels.zip` and `cgcnn_encodings.zip`: These folders contain the SOAP similarity kernels and CGCNN encodings for the QMOF database structures, which can be used with the machine learning scripts described below.

4. Charge densities associated with DFT-optimized structures can be found on an external Box server [here](https://northwestern.box.com/s/f3s930zx33di4y73gvosz9d0h5obtuoj).

## Additional Scripts and Tools
Beyond the data that makes up the QMOF database, we host several supplementary resources directly in this GitHub repository that may be of interest:

1. `machine_learning`: This folder contains scripts used to train the machine learning models and carry out the dimensionality reduction tasks in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616). These codes make use of [DScribe](https://github.com/SINGROUP/dscribe), [matminer](https://github.com/hackingmaterials/matminer), [UMAP](https://github.com/lmcinnes/umap), [ASE](https://gitlab.com/ase/ase), [Pymatgen](https://pymatgen.org/), [scikit-learn](https://github.com/scikit-learn/scikit-learn), and their respective dependencies.

2. `dft_workflow`: This folder contains an example input file to run [PyMOFScreen](https://github.com/arosen93/mof_screen), which was used to orchestrate the high-throughput DFT calculations and construct the QMOF database. A copy of PyMOFScreen is also provided in the folder for convenience.

3. `tools`: This folder contains miscellaneous Python scripts that you may find helpful, such as scripts that can help make a "DFT-ready" set of MOFs from a folder of CIFs.

4. `example_dos`: This folder contains HSE06-D3(BJ) density of states (data and plotting scripts) for the highlighted structures in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

5. `dev_changes`: This folder is primarily as a way to contribute changes to the QMOF database, such as flagging any structural fidelity issues not captured via the automated filtering scripts. Please read [this document](dev_changes/README.md) for details and how to contribute.

## Updates
Several updates are planned for the QMOF database. Upon their release, the Figshare repository will be updated, and a new version-specific DOI will be created. All changes will be documented in [updates.md](updates.md).

## Citing the QMOF Database
If you use or wish to reference the QMOF database, please cite the following paper:

- [A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery with a New Electronic Structure Database", *ChemRxiv* (2020). DOI: 10.26434/chemrxiv.13147616](https://doi.org/10.26434/chemrxiv.13147616).

It is also best practice to specify the version of the QMOF database you used in your work to ensure that your results can be accurately reproduced. This can be done by specifying the corresponding version number on the Figshare repository (currently, it is just v1).

If you use [PyMOFScreen](https://github.com/arosen93/mof_screen) in your own work, please cite the following reference:

- [A.S. Rosen, J.M. Notestein, R.Q. Snurr. "Identifying Promising Metal–Organic Frameworks for Heterogeneous Catalysis via High‐Throughput Periodic Density Functional Theory", *J. Comput. Chem.*, **40**, *12*, 1305–1318 (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1002/jcc.25787).

## Contact
If you have any questions, feel free to send me an email at rosen@u.northwestern.edu.


## Acknowledgments
This work was supported by a fellowship award through the National Defense Science and Engineering Graduate (NDSEG) Fellowship Program, sponsored by the Air Force Research Laboratory (AFRL), the Office of Naval Research (ONR) and the Army Research Office (ARO).

Additional support was provided by the U.S. Department of Energy, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences and Biosciences through the Nanoporous Materials Genome Center under Award Number DE-FG02-17ER16362. 

![NMGC logo](nmgc.png)
