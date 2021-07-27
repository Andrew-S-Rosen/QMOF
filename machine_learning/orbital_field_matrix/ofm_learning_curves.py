import pandas as pd
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import spearmanr
import numpy as np
import os

# Settings
alpha = 0.1
gamma = 0.1
kernel = 'laplacian'  # kernel function
test_size = 0.2  # fraction held-out for testing
seeds = [42, 125, 267, 541, 582]  # random seeds
train_sizes = [2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13, -1]  # train sizes
fingerprint_path = 'ofm_fingerprints.csv' # path to fingerprints (length N)
y_path = os.path.join('..','qmof-bandgaps.csv') # path to band gap data (length N)

#---------------------------------------
#Read in data
df_features = pd.read_csv(fingerprint_path, index_col=0)
df_BG = pd.read_csv(y_path, index_col=0)['BG_PBE']
df = pd.concat([df_features, df_BG], axis=1, sort=True)
df = df.dropna()
refcodes = df.index

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
		train_set, test_set = train_test_split(
			df, test_size=test_size, shuffle=True, random_state=seed)
		if train_size != -1:
			train_set = train_set[0:train_size]
		X_train = train_set.loc[:, (df.columns != 'BG_PBE')]
		X_test = test_set.loc[:, (df.columns != 'BG_PBE')]
		refcodes_train = X_train.index
		refcodes_test = X_test.index

		scaler = MinMaxScaler()
		scaler.fit(X_train)
		X_train = scaler.transform(X_train)
		X_test = scaler.transform(X_test)

		y_train = train_set.loc[:, df.columns == 'BG_PBE'].to_numpy()
		y_test = test_set.loc[:, df.columns == 'BG_PBE'].to_numpy()

		# Train and evaluate KRR model
		krr = KernelRidge(alpha=alpha, gamma=gamma, kernel=kernel)
		krr.fit(X_train, y_train)
		y_train_pred = krr.predict(X_train)
		y_test_pred = krr.predict(X_test)

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
