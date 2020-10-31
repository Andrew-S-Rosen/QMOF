`meredig_feature_generator.py`: Generates Stoichoimetric-120 encodings. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`meredig_krr.py`: Trains a KRR model given Stoichiometric-120 fingerprints and property data. Inputs: `fingerprint_path` (path to X fingerprints obtained from `meredig_feature_generator.py`), `y_path` (path to .csv of property data to train/test on).

`meredig_learning_curves.py`: Same as `meredig_krr.py` but loops over increasing training set sizes.

Pre-computed results in the `CSD-13058` folder:
- `meredig_fingerprints_13058.csv`: Stoichiometric-120 encodings for the CSD-13058-SP dataset.
- `train_results_13058.csv`: Training set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.
- `test_results_13058.csv`: Testing set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.