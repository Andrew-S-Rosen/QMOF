This file documents all updates to the QMOF database on Figshare.

# Current version
[v6](https://figshare.com/articles/dataset/QMOF_Database/13147324). Total size: 18,333 structures (17,026 de-duplicated).

# Changelog
- [v6](https://figshare.com/articles/dataset/QMOF_Database/13147324/6): Added 2620 DFT-optimized MOFs. 1217 were taken from the CSD using the usual protocol. 1188 were hypothetical MOFs obtained from the [Boyd & Woo dataset](https://doi.org/10.24435/materialscloud:2018.0016/v3).  148 were hypothetical MOF-74 and MOF-5 analogues obtained from Haranczyk's [nanoporousmaterials.org](http://nanoporousmaterials.org/databases/). 48 were hypothetical Zr MOFs made with [ToBaCCo](https://github.com/tobacco-mofs/tobacco_3.0) and obtained from [Anderson and coworkers](https://osf.io/7dgvy/). 19 were experimental pyrene MOFs from [Smit and coworkers](https://doi.org/10.24435/materialscloud:z5-ct). The maximum number of atoms per unit cell was raised to 500. 5/7/2021.
- [v5](https://figshare.com/articles/dataset/QMOF_Database/13147324/5): Release corresponding to the forthcoming published paper. No changes to the database compared to v3. Fixes a bug in `get_subset_data.py` that did not correctly write out the updated `.json` file. 2/12/21.
- [v4](https://figshare.com/articles/dataset/QMOF_Database/13147324/4): No changes to the database compared to v3. Includes a few minor typo fixes and better `.xlsx` reader. 1/12/21.
- [v3](https://figshare.com/articles/dataset/QMOF_Database/13147324/3): Added CM5 partial charges for every structure and 3000+ Bader charges (and spin densities). Patched some minor bugfixes with the unrelaxed properties for a few MOF structures, deprecated a few structures, and flagged more duplicates. Continued restructuring of main QMOF database for increased useability. 12/23/20.
- [v2](https://figshare.com/articles/dataset/QMOF_Database/13147324/2): ~1500 new structures with pore-limiting diameter greater than 2.4 Å, computed using Zeo++ prior to structure relaxation, were added to the QMOF database along with their DFT-computed properties. The cap on the maximum number of atoms per primitive cell was raised from 150 to 300. 12/05/20.
- [v1](https://figshare.com/articles/dataset/QMOF_Database/13147324/1): Initial release corresponding to the QMOF database [pre-print](https://dx.doi.org/10.26434/chemrxiv.13147616). 10/28/20.
