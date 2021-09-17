# QMOF Database

<img src=logo.png>

## Overview
This GitHub repository is the landing page for the Quantum MOF (QMOF) Database – a publicly available dataset of quantum-chemical properties for metal–organic frameworks (MOFs) and coordination polymers derived from high-throughput periodic density functional theory calculations. Currently, the QMOF Database contains computed properties for 20,000+ structures, including both experimentally synthesized and hypothetical materials.

If you use or wish to cite the QMOF Database, please refer to the following publication:

* A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery", *Matter*, **4**, 1578-1597 (2021). DOI: [10.1016/j.matt.2021.02.015](https://doi.org/10.1016/j.matt.2021.02.015).

For reproducibility purposes, also make sure to mention the version of the QMOF Database you used in your work.

Follow the QMOF Database on Twitter ([@QMOF_Database](https://twitter.com/QMOF_Database)) if you want to be the first to know about the latest news and updates.

## Accessing the QMOF Database
Tabulated data within the QMOF Database is permanently archived on Figshare at the following link:
<p align="center">
  <a href="https://doi.org/10.6084/m9.figshare.13147324"><b><i>Access the QMOF Database [v13]</i></b></a>
</p>

The data on Figshare includes DFT-optimized geometries (lattice constants, atomic positions), energies, partial atomic charges (DDEC6, CM5, Bader), bond orders (DDEC6), atomic spin densities (DDEC6, Bader), magnetic moments, band gaps, and more.

To access the VASP input and output files, refer to the following NOMAD repository:

  - [`QMOF Database - PBE`](https://nomad-lab.eu/prod/rae/gui/dataset/id/O-FUAo0mThSUeXg70cMN3Q): VASP input and output files for computed properties at the PBE-D3(BJ) level of theory.

Due to their large filesizes, charge densities are made available on a separate [SharePoint server](https://nuwildcat.sharepoint.com/:f:/s/TGS-QMOF/EqSKtJZ4lmBArOh6_mhml18BqDuIHcyu99GoUw_ILONYiQ?e=qFjVtc).

## Structure Sources
For a description of where the initial structures were sourced from, please refer to [data_sources.md](https://github.com/arosen93/QMOF/blob/main/data_sources.md).

## Updates
Updates to the QMOF Database are made on the corresponding Figshare repository with new version-specific DOIs. Changes are documented in [updates.md](updates.md). It is best-practice to specify the version of the QMOF Database you used in your work to ensure that your results can be accurately reproduced.

## Database Handling Tips
Miscellaneous Python scripts that you may find helpful can be found at [database_tools](database_tools), such as scripts to filter out problematic MOF structures. If you are looking for a specific MOF in the QMOF Database but don't know its identifier, please follow the suggestions at [mofid_search.md](mofid_search.md). 

## Machine Learning
For scripts to generate features and train ML models, refer to [machine_learning](machine_learning). For ML model performance on QMOF Database, please refer to [benchmarks.md](benchmarks.md).

## Issue Tracking
If you spot an issue with using or accessing the QMOF Database, please describe it in detail on the [Issues](https://github.com/arosen93/QMOF/issues) tracker. Similarly, if you identify any materials with structural fidelity issues not captured via the automated filtering steps, please share them so that they can be removed in future versions.

## Licensing
The data underlying the QMOF Database is made publicly available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). This means you can copy it, share it, adapt it, and do whatever you like with it provided that you give [appropriate credit](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) and [indicate any changes](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

## Contact
If you have any questions, you can reach the corresponding author at the e-mail listed [here](https://asrosen.com/contact).

## QMOF Database in the Wild
Below is a list of papers that have directly used the QMOF Database:

- V. Fung, J. Zhang, E. Juarez, B. Sumpter, "Benchmarking Graph Neural Networks for Materials Chemistry", *npj Computational Materials* (2021). DOI: [10.1038/s41524-021-00554-0](https://doi.org/10.1038/s41524-021-00554-0
).

## Acknowledgments
This work was supported by a fellowship award through the National Defense Science and Engineering Graduate (NDSEG) Fellowship Program, sponsored by the Air Force Research Laboratory (AFRL), the Office of Naval Research (ONR) and the Army Research Office (ARO).

Additional support was provided by the U.S. Department of Energy, Office of Basic Energy Sciences, Division of Chemical Sciences, Geosciences and Biosciences through the Nanoporous Materials Genome Center under Award Number DE-FG02-17ER16362. 

![NMGC logo](nmgc.png)
