In the following folders, you can train various machine learning models and carry out a UMAP dimensionality reduction. These scripts take in the following formatted data:
- A list of appended XYZs (constructed using ASE) for the structures under investigation
- A .csv of refcodes that correspond to the above structures
- A .csv of property (in this case, band gap) data with refcodes in the first column and band gap data in a column named 'BG'

Due to file size limits, the SOAP similarity kernel and the CGCNN encodings for the QMOF database must be downloaded from Figshare.