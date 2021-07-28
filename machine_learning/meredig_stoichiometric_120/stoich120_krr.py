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
kernel = 'laplacian' # kernel function
test_size = 0.2  # fraction held-out for testing
seed = 42  # random seed
fingerprint_path = 'meredig_fingerprints.csv' # fingerprints (length N)
y_path = os.path.join('..','qmof-bandgaps.csv') # band gaps (lenght N)

#---------------------------------------
#Read in data
df_features = pd.read_csv(fingerprint_path, index_col=0)
df_BG = pd.read_csv(y_path, index_col=0)['BG_PBE']
df = pd.concat([df_features, df_BG], axis=1, sort=True)
df = df.dropna()
refcodes = df.index

# Make a training and testing set
train_set, test_set = train_test_split(
	df, test_size=test_size, shuffle=True, random_state=seed)
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

# Save results
df_train = pd.DataFrame(np.concatenate((y_train, y_train_pred), axis=1), columns=[
						'DFT', 'ML'], index=refcodes_train)
df_train.to_csv('train_results.csv', header=True, index=True)

df_test = pd.DataFrame(np.concatenate((y_test, y_test_pred), axis=1), columns=[
					   'DFT', 'ML'], index=refcodes_test)
df_test.to_csv('test_results.csv', header=True, index=True)

print('Train size: ', len(y_train))
print('Test size: ', len(y_test))
print('Train/test MAE: ', mean_absolute_error(y_train, y_train_pred),
	  mean_absolute_error(y_test, y_test_pred))
print('Train/test r^2: ', r2_score(y_train, y_train_pred),
	  r2_score(y_test, y_test_pred))
print('Train/test rho: ', spearmanr(y_train, y_train_pred)
	  [0], spearmanr(y_test, y_test_pred)[0])
