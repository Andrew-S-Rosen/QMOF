import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import spearmanr

# Settings
xi = 2
alpha = 1E-3
test_size = 0.2  # fraction held-out for testing
seed = 42  # random seed
kernel_path = 'kernel.csv' # path to NxN kernel
refcodes_path = 'refcodes.csv' # path to refcodes (length N)
y_path = 'opt-bandgaps.csv' # path to band gaps (length N)

#---------------------------------------
# Read in data
K = pd.read_csv(kernel_path, header=None, delimiter=',').to_numpy()
K = K**xi
y = pd.read_csv(y_path, index_col=0)['BG_PBE'].values
refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str)

# Make a training and testing set
splitter = ShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
train_indices, test_indices = next(splitter.split(y))
y_train = y[train_indices]
y_test = y[test_indices]
K_train = K[train_indices, :][:, train_indices]
K_test = K[test_indices, :][:, train_indices]
refcodes_train = refcodes[train_indices]
refcodes_test = refcodes[test_indices]
del K, y, refcodes

# Train and evaluate KRR model
krr = KernelRidge(alpha=alpha, kernel='precomputed')
krr.fit(K_train, y_train)
y_train_pred = krr.predict(K_train)
y_test_pred = krr.predict(K_test)

# Save results
df_train = pd.DataFrame(np.vstack((y_train,y_train_pred)).T, columns=[
						'DFT', 'ML'], index=refcodes_train)
df_train.index.name = 'MOF'
df_train.to_csv('train_results.csv', header=True, index=True)

df_test = pd.DataFrame(np.vstack((y_test,y_test_pred)).T, columns=[
					   'DFT', 'ML'], index=refcodes_test)
df_test.index.name = 'MOF'
df_test.to_csv('test_results.csv', header=True, index=True)

print('Train size: ', len(train_indices))
print('Test size: ', len(test_indices))
print('Train/test MAE: ', mean_absolute_error(y_train, y_train_pred), mean_absolute_error(y_test, y_test_pred))
print('Train/test r^2: ', r2_score(y_train, y_train_pred), r2_score(y_test, y_test_pred))
print('Train/test rho: ', spearmanr(y_train, y_train_pred)[0], spearmanr(y_test, y_test_pred)[0])
