`he_feature_generator.py`: Generates Stoichoimetric-45 encodings. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`he_krr.py`: Trains a KRR model given Stoichiometric-45 fingerprints and property data. Inputs: `fingerprint_path` (path to X fingerprints obtained from `he_feature_generator.py`), `y_path` (path to .csv of property data to train/test on).

`he_learning_curves.py`: Same as `he_krr.py` but loops over increasing training set sizes.