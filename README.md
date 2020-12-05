# QMOF Database

<img src=logo.png>

## Overview
This GitHub repository is the landing page for the Quantum MOF (QMOF) database – a publicly available dataset of quantum-chemical properties derived from high-throughput periodic density functional theory calculations for 14,000+ metal–organic frameworks. The QMOF database is described in detail in DOI: [10.26434/chemrxiv.13147616](https://doi.org/10.26434/chemrxiv.13147616). All initial structures (with free solvent removed) were obtained from the [Cambridge Structural Database](https://www.ccdc.cam.ac.uk/solutions/csd-core/components/csd/) based on the list of materials identified as MOFs in the [CSD MOF subset](https://sites.google.com/view/csdmofsubset/home) and [CoRE MOF database](https://zenodo.org/record/3677685). The actual data underlying the QMOF database is hoted on Figshare at DOI: [10.6084/m9.figshare.13147324](https://doi.org/10.6084/m9.figshare.13147324).

## Purpose of this GitHub Page
The data underlying the QMOF database is hosted on Figshare and linked in the "Accessing the QMOF Database" subsection below. Nonetheless, this GitHub page serves several purposes:

1. As detailed in the "Scripts and Tools" subsection below, this GitHub page includes supplementary files that can be used to carry out the machine learning analyses in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

2. It allows for open, public discussions via the GitHub [Issues](https://github.com/arosen93/QMOF/issues) tab. While any issues can certainly be raised here, I also welcome comments, suggestions, or other forms of open dialogue in the Issues tracker.

3. I will use the [Projects](https://github.com/arosen93/QMOF/projects) tab to share any planned updates to the database.

4. If you have developed direct extensions, modifications, or subsets related to the QMOF database, I am more than happy to include a link to your work on this GitHub page so that all QMOF database resources can be linked to one another in a single place.

## Accessing the QMOF Database
All versions of the QMOF database can be accessed on Figshare at the link below:
<p align="center">
  <a href="https://doi.org/10.6084/m9.figshare.13147324"><b><i>Access the QMOF Database</i></b></a>
</p>

The individual files uploaded to Figshare are as follows:

1. `qmof_database.zip`: This contains the structures and tabulated properties of all structurally relaxed materials in the QMOF database. This is likely the data that you're looking for.

2. `vasp_files.zip`: This contains the raw VASP input and output files for the structurally relaxed MOFs in the QMOF database. It contains additional properties that may be of interest to some users (e.g. total/projected density of states, detailed population analyses, other typical outputs).

3. `soap_kernels.zip` and `cgcnn_encodings.zip`: These folders contain the SOAP similarity kernels and CGCNN encodings for the (unrelaxed) QMOF database structures, which can be used with the machine learning scripts described below.

4. Charge densities associated with DFT-optimized structures can be found on an external Box server [here](https://northwestern.box.com/s/f3s930zx33di4y73gvosz9d0h5obtuoj).

## Additional Scripts and Tools
Beyond the data that makes up the QMOF database, we host several supplementary resources directly in this GitHub repository that may be of interest:

1. `machine_learning`: This folder contains scripts used to train the machine learning models and carry out the dimensionality reduction tasks in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

2. `dft_workflow`: This folder contains an example input file to run [PyMOFScreen](https://github.com/arosen93/mof_screen), which was used to orchestrate the high-throughput DFT calculations and construct the QMOF database. A copy of PyMOFScreen is also provided in the folder for convenience.

3. `tools`: This folder contains miscellaneous Python scripts that you may find helpful, such as scripts to filter out clearly erroneous MOF structures.

4. `example_dos`: This folder contains HSE06-D3(BJ) density of states (data and plotting scripts) for the highlighted structures in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

5. `fidelity_tracker`: This folder tracks any additional structural fidelity issues not captured via the automated filtering scripts (user contributions are welcome). See [here](https://github.com/arosen93/QMOF/tree/main/fidelity_tracker/opt-cifs) for an up-to-date list of any refcodes with flagged structural errors. Please read [this document](fidelity_tracker/README.md) for details on how to contribute to the fidelity tracker.

## Updates
All updates to the QMOF database are made on the corresponding [Figshare repository](https://doi.org/10.6084/m9.figshare.13147324) with new version-specific DOIs. All changes are documented in [updates.md](updates.md).

## Citing the QMOF Database
If you use or wish to reference the QMOF database, please cite the following pre-print until the peer-reviewed publication is released:

- [A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery with a New Electronic Structure Database", *ChemRxiv* (2020). DOI: 10.26434/chemrxiv.13147616](https://doi.org/10.26434/chemrxiv.13147616).

It is also best-practice to specify the version of the QMOF database you used in your work to ensure that your results can be accurately reproduced. This can be done by specifying the corresponding version number on the Figshare repository and/or referencing the version-specific DOI of the Figshare repository that you use.

If you use [PyMOFScreen](https://github.com/arosen93/mof_screen) in your own work, please cite the following reference:

- [A.S. Rosen, J.M. Notestein, R.Q. Snurr. "Identifying Promising Metal–Organic Frameworks for Heterogeneous Catalysis via High‐Throughput Periodic Density Functional Theory", *J. Comput. Chem.*, **40**, *12*, 1305–1318 (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1002/jcc.25787).

## Licensing
The data underlying the QMOF database is made publicly available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). This means you can copy it, share it, adapt it, and do whatever you like with it provided that you give [appropriate credit](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) and [indicate any changes](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

## Contact
If you have any questions, feel free to send me an email at rosen@u.northwestern.edu.

## Acknowledgments
This work was supported by a fellowship award through the National Defense Science and Engineering Graduate (NDSEG) Fellowship Program, sponsored by the Air Force Research Laboratory (AFRL), the Office of Naval Research (ONR) and the Army Research Office (ARO).

Additional support was provided by the U.S. Department of Energy, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences and Biosciences through the Nanoporous Materials Genome Center under Award Number DE-FG02-17ER16362. 

![NMGC logo](nmgc.png)
