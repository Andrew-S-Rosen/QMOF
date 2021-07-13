import pandas as pd
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import spearmanr
import numpy as np

# Settings
xi = 2
alpha = 1E-3
gamma = 0.1
test_size = 0.2  # fraction held-out for testing
seeds = [42, 125, 267, 541, 582]  # random seeds
train_sizes = [2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13, -1]  # train sizes
kernel_path = 'kernel.csv' # path to NxN kernel
y_path = 'opt-bandgaps.csv'  # path to band gaps (length N)
refcodes_path = 'refcodes.csv' # path to refcoeds (length N)

#---------------------------------------
# Read in data
K = pd.read_csv(kernel_path, header=None, delimiter=',').to_numpy()
K = K**xi
y = pd.read_csv(y_path, index_col=0)['BG_PBE'].values
refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str)

mae = []
r2 = []
rho = []
mae_std = []
r2_std = []
rho_std = []
for train_size in train_sizes:
	mae_test_seeds = []
	r2_test_seeds = []
	rho_test_seeds = []
	for seed in seeds:

		# Make a training and testing set
		splitter = ShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
		train_indices, test_indices = next(splitter.split(y))
		if train_size != -1:
			train_indices = train_indices[0:train_size]
		y_train = y[train_indices]
		y_test = y[test_indices]
		K_train = K[train_indices, :][:, train_indices]
		K_test = K[test_indices, :][:, train_indices]
		refcodes_train = refcodes[train_indices]
		refcodes_test = refcodes[test_indices]

		# Train and evaluate KRR model
		krr = KernelRidge(alpha=alpha, kernel='precomputed')
		krr.fit(K_train, y_train)
		y_train_pred = krr.predict(K_train)
		y_test_pred = krr.predict(K_test)

		mae_test_seeds.append(mean_absolute_error(y_test, y_test_pred))
		r2_test_seeds.append(r2_score(y_test, y_test_pred))
		rho_test_seeds.append(spearmanr(y_test, y_test_pred)[0])

	mae.append(np.average(mae_test_seeds))
	r2.append(np.average(r2_test_seeds))
	rho.append(np.average(rho_test_seeds))
	mae_std.append(np.std(mae_test_seeds))
	r2_std.append(np.std(r2_test_seeds))
	rho_std.append(np.std(rho_test_seeds))

	print('Training size: ', train_size)
	print('Avg. testing MAE: ', np.round(np.average(mae_test_seeds), 3))
	print('Avg. testing r^2: ', np.round(np.average(r2_test_seeds), 3))
	print('Avg. testing rho: ', np.round(np.average(rho_test_seeds), 3))

np.savetxt('learning_curve_avg.csv',np.vstack([mae,r2,rho]),delimiter=',')
np.savetxt('learning_curve_std.csv',np.vstack([mae_std,r2_std,rho_std]),delimiter=',')