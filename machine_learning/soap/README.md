`soap_matrix_generator.py`: Generates SOAP fingerprints for a set of structures. Inputs: `xyz_path` (.xyz file of concatenated XYZs for each structure), `refcodes_path` (.csv file of corresponding refcodes).

`soap_avg_kernel_generator.py`: Generates an averaged SOAP similarity kernel from a folder of SOAP fingerprints. Inputs: `refcodes_path` (.csv of IDs corresponding to N structures), `comparison_refcodes_path` (.csv of IDs corresponding to M structures to compare to), `soaps_path` (path to folder containing SOAP fingerprints genreated from `soap_matrix_generator.py`).

`soap_krr.py`: Trains a KRR model given a square SOAP similarity kernel and property data. Inputs: `kernel_path` (path to SOAP similarity kernel obtained from `soap_avg_kernel_generator.py`), `y_path` (path to .csv of property data to train/test on).

`soap_learning_curves.py`: Same as `soap_krr.py` but loops over increasing training set sizes.

Pre-computed results in the `CSD-13058` folder:
- `train_results_13058.csv`: Training set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.
- `test_results_13058.csv`: Testing set statistics for predicting DFT-optimized band gaps from CSD-13058-SP.