import pandas as pd
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt
import os

seed = 42  # random seed
x = os.path.join(
	'..', '..', 'stoichiometric_120', 'CSD-14482', 'meredig_fingerprints.csv')  # .csv of X encodings
bandgaps_path = os.path.join(
	'..', 'opt-bandgaps.csv')  # .csv of y properties

# ---------------------------------------
# Band gaps and refcodes
df = pd.read_csv(bandgaps_path, delimiter=',', header=0, index_col=0)
bg = df['BG_PBE'].values

# Encoding
X = pd.read_csv(x, delimiter=',', header=0, index_col=0).dropna()
refcodes = X.index.values

# Discretize band gaps for colorbar
bg_class = np.empty(len(refcodes), dtype=object)
bg = np.empty(len(refcodes))
for i, ref in enumerate(refcodes):
	b = df.loc[ref]['BG_PBE']
	bg[i] = b
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

# Perform dimensionality reduction
fit = umap.UMAP(n_neighbors=50, min_dist=0.4, random_state=seed)
u = fit.fit(X)

# Make static plot
plt.rcParams["figure.dpi"] = 1000
p = umap.plot.connectivity(u, edge_bundling='hammer',
						   edge_cmap='inferno', width=8500, height=8500)
p.texts[0].set_visible(False)
plt.savefig('umap_connect.png', transparent=True)
