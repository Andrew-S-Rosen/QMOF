`sine_matrix_feature_generator.py`: Generates sine Coulomb matrix eigenspectrum. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`sine_matrix_krr.py`: Trains a KRR model given sine Coulomb matrix-based fingerprints and property data. Inputs: `fingerprint_path` (path to X fingerprints obtained from `sine_matrix_feature_generator.py`), `y_path` (path to .csv of property data to train/test on).

`sine_matrix_learning_curves.py`: Same as `sine_matrix_krr.py` but loops over increasing training set sizes.

Pre-computed results in the `CSD-13058` folder:
`sine_matrix_fingerprints_13058.csv`: sine Coulomb matrix eigenspectrum for the CSD-13058-SP dataset.
`train_results_13058.csv`: Training set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.
`test_results_13058.csv`: Testing set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.