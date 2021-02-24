# QMOF Database

<img src=logo.png>

## Overview
This GitHub repository is the landing page for the Quantum MOF (QMOF) database – a publicly available dataset of quantum-chemical properties for metal–organic frameworks (MOFs) derived from high-throughput periodic density functional theory calculations. Currently, the QMOF database contains computed properties for 15,713 structures!

If you use or wish to cite the QMOF database, please refer to the following publication:

- A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery", *Matter* (in press). Pre-print available at [DOI: 10.26434/chemrxiv.13147616](https://doi.org/10.26434/chemrxiv.13147616).

## Accessing the QMOF Database
All versions of the QMOF database can be accessed on Figshare at the following link:
<p align="center">
  <a href="https://doi.org/10.6084/m9.figshare.13147324"><b><i>Access the QMOF Database</i></b></a>
</p>

The files made publicly available with the QMOF database are described below:

1. `qmof_database.zip`: Structures and tabulated properties of all materials in the QMOF database. This is likely the data that you're looking for.

2. `vasp_files_A.zip`: Raw VASP input and output files at the PBE-D3(BJ) level of theory for the structurally relaxed MOFs in the QMOF database. It contains additional properties that may be of interest to some users.

Additional files are made available on a [Box server](https://northwestern.box.com/s/uasi8jpov51icueu3s3wvcftkgjcwil7), as described below:

3. `charge_densities`: Charge densities for the MOFs in the QMOF database. If you'd like to download all the charge densities, please contact me directly since Box currently has a 15 GB limit on downloads.

4. `ml_reproducibility`: SOAP similarity kernels and CGCNN encodings for the (unrelaxed) QMOF database structures, which can be used with the machine learning scripts described below. This is included solely for reproducibility purposes.

## Purpose of this GitHub Page
The data underlying the QMOF database is hosted on Figshare and linked in the "Accessing the QMOF Database" subsection above. Nonetheless, this GitHub page serves several additional purposes:

1. As detailed in the "Additional Scripts and Tools" subsection below, this GitHub page includes supplementary files that can be used to carry out the machine learning analyses in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

2. It allows for open, public discussions via the GitHub [Discussions](https://github.com/arosen93/QMOF/discussions) tab, where I welcome comments, suggestions, or other forms of open dialogue. Any issues can also be raised in the GitHub [Issues](https://github.com/arosen93/QMOF/issues) tracker.

3. I will use the [Projects](https://github.com/arosen93/QMOF/projects) tab to share any planned updates to the database.

4. If you have developed direct extensions, modifications, or subsets related to the QMOF database, I am more than happy to include a link to your work on this GitHub page so that all QMOF database resources can be linked to one another in a single place.

## Additional Scripts and Tools
Beyond the data that makes up the QMOF database, we host several supplementary resources directly in this GitHub repository that may be of interest:

1. [`machine_learning`](machine_learning): Scripts used to train the machine learning models and carry out the dimensionality reduction tasks in the corresponding [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

2. [`dft_workflow`](dft_workflow): An example input file to run [PyMOFScreen](https://github.com/arosen93/mof_screen), which was used to orchestrate the high-throughput DFT calculations and construct the QMOF database. A copy of PyMOFScreen is also provided in the folder for convenience.

3. [`tools`](tools): Miscellaneous Python scripts that you may find helpful, such as scripts to filter out clearly erroneous MOF structures.

4. [`example_dos`](example_dos): HSE06-D3(BJ) density of states (data and plotting scripts) for the highlighted structures in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616).

## Fidelity Tracker
See [here](https://github.com/arosen93/QMOF/blob/main/fidelity_tracker) for an up-to-date list of any refcodes with flagged structural fidelity issues not captured via the automated filtering steps. User contributions are highly encouraged!

## Updates
All updates to the QMOF database are made on the corresponding [Figshare repository](https://doi.org/10.6084/m9.figshare.13147324) with new version-specific DOIs. All changes are documented in [updates.md](updates.md). It is always best-practice to specify the version of the QMOF database you used in your work to ensure that your results can be accurately reproduced.

## Licensing
The data underlying the QMOF database is made publicly available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). This means you can copy it, share it, adapt it, and do whatever you like with it provided that you give [appropriate credit](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) and [indicate any changes](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

## Contact
If you have any questions, feel free to send me an email at rosen@u.northwestern.edu.

## Acknowledgments
This work was supported by a fellowship award through the National Defense Science and Engineering Graduate (NDSEG) Fellowship Program, sponsored by the Air Force Research Laboratory (AFRL), the Office of Naval Research (ONR) and the Army Research Office (ARO).

Additional support was provided by the U.S. Department of Energy, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences and Biosciences through the Nanoporous Materials Genome Center under Award Number DE-FG02-17ER16362. 

![NMGC logo](nmgc.png)
