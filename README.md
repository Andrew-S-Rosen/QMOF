# QMOF Database

<img src=logo.png>

## Overview
This GitHub repository is the landing page for the Quantum MOF (QMOF) Database – a publicly available dataset of quantum-chemical properties for metal–organic frameworks (MOFs) derived from high-throughput periodic density functional theory calculations. Currently, the QMOF Database contains computed properties for 17,000+ structures!

If you use or wish to cite the QMOF Database, please refer to the following publication:

- A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery", *Matter*, **4**, 1578-1597 (2021). DOI: [10.1016/j.matt.2021.02.015](https://www.cell.com/matter/fulltext/S2590-2385(21)00070-9).

Follow the QMOF Database on Twitter ([@QMOF_Database](https://twitter.com/QMOF_Database)) if you want to be the first to know about the latest news and updates.

## Accessing the QMOF Database
All versions of the QMOF Database can be accessed on Figshare at the following link:
<p align="center">
  <a href="https://doi.org/10.6084/m9.figshare.13147324"><b><i>Access the QMOF Database</i></b></a>
</p>

The files made publicly available with the QMOF Database are described below:

1. `qmof_database.zip`: Structures and tabulated properties of all materials in the QMOF Database. This is likely the data that you're looking for.

2. `vasp_files_A.zip`: Raw VASP input and output files at the PBE-D3(BJ) level of theory for the structurally relaxed MOFs in the QMOF Database. It contains additional properties that may be of interest to some users.

In the above data files, you can find DFT-optimized geometries (lattice constants, atomic positions), energies, partial charges (DDEC6, CM5, Bader), bond orders (DDEC6), spin densities (DDEC6, Bader) and magnetic moments, density of states, band gaps, and more.

If you'd like to download the charge densities, they are available on an [external SharePoint site](https://nuwildcat.sharepoint.com/:f:/s/TGS-QMOF/EqSKtJZ4lmBArOh6_mhml18BqDuIHcyu99GoUw_ILONYiQ?e=qFjVtc).

## GitHub Features
The data underlying the QMOF Database is hosted on Figshare and linked in the "Accessing the QMOF Database" subsection above. Nonetheless, this GitHub page serves several additional purposes:

1. I will use the [Projects](https://github.com/arosen93/QMOF/projects) tab to share any planned additions to the database.
2. Any issues can be raised in the GitHub [Issues](https://github.com/arosen93/QMOF/issues) tracker.
3. Open, public discussions about the QMOF Database are supported via the GitHub [Discussions](https://github.com/arosen93/QMOF/discussions) tab.

## Updates
All updates to the QMOF Database are made on the corresponding [Figshare repository](https://doi.org/10.6084/m9.figshare.13147324) with new version-specific DOIs. All changes are documented in [updates.md](updates.md). It is always best-practice to specify the version of the QMOF Database you used in your work to ensure that your results can be accurately reproduced.

## Fidelity Tracker
See [here](https://github.com/arosen93/QMOF/blob/main/fidelity_tracker) for an up-to-date list of any refcodes with flagged structural fidelity issues not captured via the automated filtering steps. User contributions are highly encouraged!

## Data for Reproducibility 
Beyond the data that makes up the QMOF Database, we host several supplementary resources on this GitHub page to allow others to reproduce results in the QMOF Database paper.

1. [`machine_learning`](machine_learning): Scripts used to train the machine learning models and carry out the dimensionality reduction tasks in the corresponding QMOF Database paper.

2. [`dft_workflow`](dft_workflow): An example input file to run [PyMOFScreen](https://github.com/arosen93/mof_screen), which was used to orchestrate the high-throughput DFT calculations and construct the QMOF Database. A copy of PyMOFScreen is also provided in the folder for convenience.

3. [`tools`](tools): Miscellaneous Python scripts that you may find helpful, such as scripts to filter out problematic MOF structures.

4. [`example_dos`](example_dos): HSE06-D3(BJ) density of states (data and plotting scripts) for the highlighted structures in the QMOF Database paper.

## Licensing
The data underlying the QMOF Database is made publicly available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). This means you can copy it, share it, adapt it, and do whatever you like with it provided that you give [appropriate credit](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) and [indicate any changes](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

## Contact
If you have any questions, feel free to send me an email at rosen@u.northwestern.edu.

## QMOF Database in the Wild
Below is a list of papers that have directly used the QMOF Database:

- V. Fung, J. Zhang, E. Juarez, B. Sumpter, "Benchmarking Graph Neural Networks for Materials Chemistry", *ChemRxiv* (2021). DOI: [10.26434/chemrxiv.13615421](https://doi.org/10.26434/chemrxiv.13615421
).

## Acknowledgments
This work was supported by a fellowship award through the National Defense Science and Engineering Graduate (NDSEG) Fellowship Program, sponsored by the Air Force Research Laboratory (AFRL), the Office of Naval Research (ONR) and the Army Research Office (ARO).

Additional support was provided by the U.S. Department of Energy, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences and Biosciences through the Nanoporous Materials Genome Center under Award Number DE-FG02-17ER16362. 

![NMGC logo](nmgc.png)
