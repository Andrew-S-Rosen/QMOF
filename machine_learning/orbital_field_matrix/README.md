`ofm_feature_generator.py`: Generates (flattened) orbital field matrices. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`ofm_krr.py`: Trains a KRR model given orbital field matrix fingerprints and property data. Inputs: `fingerprint_path` (path to X fingerprints obtained from `ofm_feature_generator.py`), `y_path` (path to .csv of property data to train/test on).

`ofm_learning_curves.py`: Same as `ofm_krr.py` but loops over increasing training set sizes.

Pre-computed results in the `CSD-13058` folder:
- `ofm_fingerprints_13058.csv`: Flattened orbital field matrix fingerprints for the CSD-13058-SP dataset.
- `train_results_13058.csv`: Training set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.
- `test_results_13058.csv`: Testing set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.