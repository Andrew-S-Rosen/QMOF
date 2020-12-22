In the following folders, you can train various machine learning models and carry out a UMAP dimensionality reduction. These scripts take in the following formatted data:
- A list of appended XYZs (constructed using ASE) for the structures under investigation
- A .csv of refcodes that correspond to the above structures
- A .csv of property (in this case, band gap) data with refcodes in the first column and band gap data in a column named 'BG'

Due to file size limits, you must make your own SOAP similarity kernels and CGCNN encodings. If you have any issues with this, don't hesitate to reach out.

The scripts in this folder make use of [DScribe](https://github.com/SINGROUP/dscribe), [matminer](https://github.com/hackingmaterials/matminer), [UMAP](https://github.com/lmcinnes/umap), [ASE](https://gitlab.com/ase/ase), [Pymatgen](https://pymatgen.org/), [scikit-learn](https://github.com/scikit-learn/scikit-learn), and their respective dependencies.
