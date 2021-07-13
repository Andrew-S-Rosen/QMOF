`meredig_feature_generator.py`: Generates Stoichoimetric-120 encodings. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`meredig_krr.py`: Trains a KRR model given Stoichiometric-120 fingerprints and property data. Inputs: `fingerprint_path` (path to X fingerprints obtained from `meredig_feature_generator.py`), `y_path` (path to .csv of property data to train/test on).

`meredig_learning_curves.py`: Same as `meredig_krr.py` but loops over increasing training set sizes.