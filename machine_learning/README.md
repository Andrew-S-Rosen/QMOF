In the following folders, you can train various machine learning models and carry out a UMAP dimensionality reduction. These scripts take in the following formatted data:
- A list of appended XYZs (constructed using ASE) for the structures under investigation.
- A .csv of refcodes that correspond to the above structures.
- A .csv of property (in this case, band gap) data with refcodes in the first column and band gap data in a column named 'BG_PBE'.

The scripts in this folder make use of [DScribe](https://github.com/SINGROUP/dscribe), [matminer](https://github.com/hackingmaterials/matminer), [UMAP](https://github.com/lmcinnes/umap), [ASE](https://gitlab.com/ase/ase), [Pymatgen](https://pymatgen.org/), [scikit-learn](https://github.com/scikit-learn/scikit-learn), [PyTorch](https://github.com/pytorch/pytorch), and their respective dependencies.