import pandas as pd
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt
import os

seed = 42  # random seed
xi = 2  # from SOAP hyperparameter optimization
kernel_path = 'SP-avg_kernel_14482_14482.csv' # SOAP similarity kernel
bandgaps_path = os.path.join(
	'..', 'opt-bandgaps.csv') # .csv of y properties

#---------------------------------------
# Band gaps and refcodes
df = pd.read_csv(bandgaps_path, delimiter=',')
bg = df['BG_PBE'].values
refcodes = df['refcode'].values
refcodes = [i.split('_')[0] for i in refcodes]

# SOAP similarity kernel
K = pd.read_csv(kernel_path, delimiter=',', header=None).to_numpy()
K[K>1] = 1.0 #avoid floating point issues

# Discretize band gaps for colorbar
bg_class = np.empty(len(bg), dtype=object)
for i, b in enumerate(bg):
	if b < 0.5:
		bg_class[i] = '[0 eV, 0.5 eV)'
	elif b < 1:
		bg_class[i] = '[0.5 eV, 1 eV)'
	elif b < 2:
		bg_class[i] = '[1 eV, 2 eV)'
	elif b < 3:
		bg_class[i] = '[2 eV, 3 eV)'
	elif b < 4:
		bg_class[i] = '[3 eV, 4 eV)'
	else:
		bg_class[i] = '[4 eV, 6.5 eV)'
bg_class = np.array(bg_class)

# Generate distance matrix
D = np.sqrt(2-2*K**xi)

# Perform dimensionality reduction
fit = umap.UMAP(metric='precomputed', random_state=seed)
u = fit.fit(D)

# Make static plot
plt.rcParams["figure.dpi"] = 1000
p = umap.plot.connectivity(u, edge_bundling='hammer', edge_cmap='inferno', width=8500, height=8500)
p.texts[0].set_visible(False)
plt.savefig('umap_connect.png',transparent=True)
