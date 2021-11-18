# QMOF Database

<img src=logo.png>

## Overview
The Quantum MOF (QMOF) Database is a publicly available dataset of quantum-chemical properties for metal–organic frameworks (MOFs) and coordination polymers derived from high-throughput periodic density functional theory calculations.

## The QMOF Database is now hosted on the Materials Project!
Explore the dataset and more at the following link:
<p align="center">
  <a href="https://materialsproject.org/mofs"><b><i>https://materialsproject.org/mofs</i></b></a>
</p>

Follow the QMOF Database on Twitter ([@QMOF_Database](https://twitter.com/QMOF_Database)) if you want to be the first to know about the latest news and updates.

## Downloading the QMOF Database
The data underlying the QMOF Database is permanently archived on Figshare at the following link:
<p align="center">
  <a href="https://doi.org/10.6084/m9.figshare.13147324"><b><i>Download the QMOF Database</i></b></a>
</p>

The data on Figshare includes DFT-optimized geometries (lattice constants, atomic positions), energies, partial atomic charges (DDEC6, CM5, Bader), bond orders (DDEC6), atomic spin densities (DDEC6, Bader), magnetic moments, band gaps, and more.

To access the VASP input and output files, refer to the following NOMAD repository:

  - [`QMOF Database - PBE`](http://dx.doi.org/10.17172/NOMAD/2021.10.10-1): VASP input and output files for computed properties at the PBE-D3(BJ) level of theory.

You can query the NOMAD entries via `comment` or `external_id`, which refer to the name and QMOF ID for each material, respectively. You can also bulk download the entire dataset on NOMAD [here](https://nomad-lab.eu/prod/rae/gui/dataset/id/O-FUAo0mThSUeXg70cMN3Q?results=datasets).

Due to their large filesizes, charge densities are made available on a separate [Globus Endpoint](https://app.globus.org/file-manager?origin_id=13a0834e-226a-11ec-a0a4-6b21ca6daf73&origin_path=%2F).

## Structures to Remove
Please see [poor_fidelity.txt](poor_fidelity.txt) for a list of structures that will be removed from the QMOF Database in the next release due to poor structural fidelity (e.g. missing H atoms or counterions).

## Citation
If you use or wish to cite the QMOF Database, please refer to the following publication:

* A.S. Rosen, S.M. Iyer, D. Ray, Z. Yao, A. Aspuru-Guzik, L. Gagliardi, J.M. Notestein, R.Q. Snurr. "Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery", *Matter*, **4**, 1578-1597 (2021). DOI: [10.1016/j.matt.2021.02.015](https://doi.org/10.1016/j.matt.2021.02.015).

## Licensing
The data underlying the QMOF Database is made publicly available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). This means you can copy it, share it, adapt it, and do whatever you like with it provided that you give [appropriate credit](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) and [indicate any changes](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

## Contact
If you have any questions, you can reach the corresponding author at the e-mail listed [here](https://asrosen.com/contact).
