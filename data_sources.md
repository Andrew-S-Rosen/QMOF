# Data Sources
Here, we describe the data sources for the MOF crystal structures in the QMOF Database.

## Experimetnal MOFs
### CSD
Most materials in the QMOF Database are taken from the [Cambridge Structural Database](https://www.ccdc.cam.ac.uk/structures/) (CSD) with their free solvents removed. To determine which materials in the CSD are sufficiently MOF-like, we used the list of materials in the [CSD MOF Subset](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.7b00441) and the [2019 CoRE MOF Database](https://pubs.acs.org/doi/abs/10.1021/acs.jced.9b00835). Unless otherwise stated, these structures were taken directly from the CSD so that we could use the valuable CSD meta-data to choose which materials to discard in our pre-screening process.

All materials taken from the CSD have `_FSR` at the end of their name. The `source` flag is set to `'CSD'`.

### CoRE 2019

Since v8 of the QMOF Database, some MOFs were taken directly from the 2019 CoRE MOF Database uploaded on [Zenodo](https://doi.org/10.5281/zenodo.3677685
). In these cases, only the free solvent removed structures were adopted. A curated list of CoRE MOFs was taken from [Kancharlapalli et al.](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.0c01229) to reduce the likelihood of obtaining erroneous crystal structures.

All materials taken directly from the CoRE MOF Database have `core_` at the start of their name. The `source` flag is set to `'CoRE'`. Note that there are many materials in the CoRE MOF Database that were instead downloaded directly from the CSD (as described above).

### Pyrene MOFs
A few pyrene-containing MOFs were taken from [prior work](https://pubs.rsc.org/en/content/articlehtml/2021/cs/d0cs00424c) using the data uploaded to the [Materials Cloud](https://doi.org/10.24435/materialscloud:z5-ct).

All materials taken from this dataset have `pyrene_` in their name. The `source` flag is set to `'Pyrene'`.

## Hypothetical MOFs
Since v6 of the QMOF Database, we have now included hypothetical MOFs from various sources.

### ToBaCCo
Several of the MOFs in the database were constructed using the [ToBaCCo code](https://github.com/tobacco-mofs/tobacco_3.0) described in a series of prior studies [here](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.7b00848) and [here](https://pubs.rsc.org/en/content/articlehtml/2019/ce/c8ce01637b). These are described below.

#### Anderson and Gómez-Gualdrón
A database of ToBaCCo-constructed Zr-MOFs was adopted from [prior work](https://aip.scitation.org/doi/full/10.1063/5.0048736) by Andereson and Gómez-Gualdrón. See [here](https://osf.io/7dgvy/) for the dataset. We also exchanged the Zr species for Hf to include hypothetical Hf-MOFs as well.

All materials taken from this dataset have `tobacco_` and `_SR_` in their names. The `source` flag is set to `'Anderson'`.

#### Colón, Gómez-Gualdrón, and Snurr
A database of Cu triangle MOFs was adopted from [prior work](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.7b00848) by Colón, Gómez-Gualdrón, and Snurr. These structures had H atoms in the center of the Cu triangles, which were removed before relaxing their structures with DFT.

All materials taken from this dataset have `tobacco_` in their names. The `source` flag is set to `'ToBaCCo'`.

### Boyd and Woo
Several of the MOFs in the database were constructed using the [TOBASCCO code](https://github.com/peteboyd/tobascco) as described in prior work by [Boyd and Woo](https://pubs.rsc.org/en/content/articlehtml/2016/ce/c6ce00407e). These were obtained from [prior work](https://www.nature.com/articles/s41586-019-1798-7) by Boyd et al. using the Materials Cloud dataset [here](https://doi.org/10.24435/materialscloud:2018.0016/v3). We  made modifications to several of these MOFs prior to structure relaxation to diversify our dataset. For instance, we occasionally exchanged the metals in the inorganic node, and we constructed Al rod MOFs by exchanging the metals in the pre-existing V rod MOFs and protonating the bridging oxo ligands.

All materials taken from this dataset have `boydwoo_` in their names. The `source` flag is set to `'BoydWoo'`.

### Haranczyk Datasets
Several of the MOFs in the database were obtained from prior work by Maciej Haranczyk and coworkers.

#### MOF-5
Hypothetical MOF-5 analogues were obtained from [prior work](https://pubs.acs.org/doi/abs/10.1021/jp401920y) by Haranczyk and colleagues. See [here](http://nanoporousmaterials.org/databases/) for the dataset.

All materials taken from this dataset have `MOF-5` in their names. The `source` flag is set to `'Haranczyk_MOF5'`.

#### MOF-74
Hypothetical MOF-74 analogues were obtained from [prior work](https://pubs.rsc.org/en/content/articlehtml/2016/sc/c6sc01477a) by Haranczyk and colleagues.

All materials taken from this dataset have `mof74` in their names. The `source` flag is set to `'Haranczyk_MOF74'`.
