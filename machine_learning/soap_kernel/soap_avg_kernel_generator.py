import os
import numpy as np
from sparse import load_npz

# This will make an average kernel matrix of (M x N) dimensions.
# If refcodes_path == comparison_refcodes_path, then M = N.
# This code must be run after `soap_matrix_generator.py`
# Note: This can be memory-intensive.

# Settings
basepath = os.getcwd()  # Base path where results will be stored
refcodes_path = os.path.join('..','qmof-refcodes.csv')  # IDs corresponding to N structures
comparison_refcodes_path = refcodes_path  # IDs corresponding to M structures
soaps_path = os.path.join(basepath, 'soap_matrices') # Path where SOAP matrices are stored

#---------------------------------------
# Read in refcodes
refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str).tolist()

if refcodes_path == comparison_refcodes_path:
	comparison_refcodes = refcodes
else:
	comparison_refcodes = np.genfromtxt(
		comparison_refcodes_path, delimiter=',', dtype=str).tolist()
M = len(refcodes)
N = len(comparison_refcodes)

example_soap = load_npz(os.path.join(soaps_path, os.listdir(soaps_path)[0]))
N_features = np.shape(example_soap)[1]

# Prepare M average SOAPs
print('Initializing M matrix')
avg_soaps_M = np.zeros((M, N_features), dtype=np.float32)
for i in range(M):
	print(refcodes[i])
	p = os.path.join(soaps_path, f'soap_{str(refcodes[i])}.npz')
	soap_temp = load_npz(p).todense()
	avg_soaps_M[i, :] = soap_temp.mean(axis=0)

# Prepare N average SOAPs
if M != N or refcodes_path != comparison_refcodes_path:
	print('Initializing N matrix')
	avg_soaps_N = np.zeros((N, N_features), dtype=np.float32)
	for i in range(N):
		print(comparison_refcodes[i])
		p = os.path.join(soaps_path, f'soap_{str(comparison_refcodes[i])}.npz')
		soap_temp = load_npz(p).todense()
		avg_soaps_N[i, :] = soap_temp.mean(axis=0)

# Compute average kernel matrix
print('Computing K')
if M == N and refcodes_path == comparison_refcodes_path:
	K = avg_soaps_M.dot(avg_soaps_M.T)
	norm = np.sqrt(np.einsum('ii,jj->ij', K, K))
else:
	K = avg_soaps_M.dot(avg_soaps_N.T)
	norm = np.sqrt(np.einsum(
		'ii,jj->ij', avg_soaps_M.dot(avg_soaps_M.T), avg_soaps_N.dot(avg_soaps_N.T)))
K = K/norm

kernel_name = 'avg_soap_kernel.csv'
np.savetxt(os.path.join(basepath, kernel_name), K.T, delimiter=',')
