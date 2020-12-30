import pandas as pd
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch

seed = 42  # random seed
x = 'meredig_fingerprints_42349.csv' # X encodings of QMOF-42362
csd_14482 = os.path.join(
	'..', 'opt-bandgaps.csv') # .csv of QMOF-14482 data

#---------------------------------------
# Encoding
X = pd.read_csv(x, delimiter=',', header=0, index_col=0).dropna()
refcodes = X.index.values

df_csd_14482 = pd.read_csv(csd_14482, delimiter=',')
csd_14482_refs = df_csd_14482['refcode'].values
csd_14482_class = [i for i, ref in enumerate(
	refcodes) if ref in csd_14482_refs]
classifier = np.array(['QMOF-42349']*len(refcodes))
classifier[csd_14482_class] = 'QMOF-14482'
mask = np.zeros(len(refcodes),dtype=bool)
mask[csd_14482_class]=1

# Perform dimensionality reduction
fit = umap.UMAP(n_neighbors=50, min_dist=0.4, random_state=seed)
u = fit.fit(X)

# Make static plot
points = u.embedding_
labels = classifier
width = 8500
height = 8500
point_size = 100.0 / np.sqrt(points.shape[0])
dpi = 1000
plt.rcParams["figure.dpi"] = dpi
color_key_cmap = 'Paired_r'
fig = plt.figure(figsize=(width / dpi, height / dpi))
ax = fig.add_subplot(111)
color_key = plt.get_cmap(color_key_cmap)(np.linspace(0, 1, np.unique(labels).shape[0]))
unique_labels = np.unique(labels)
num_labels = unique_labels.shape[0]
legend_elements = [
				Patch(facecolor=color_key[i], label=unique_labels[i])
				for i, k in enumerate(unique_labels)
			]
new_color_key = {k: color_key[i] for i, k in enumerate(unique_labels)}
colors = pd.Series(labels).map(new_color_key)
ax.scatter(points[:, 0][~mask], points[:, 1][~mask], s=point_size, c=colors[~mask],alpha=0.5)
ax.scatter(points[:, 0][mask], points[:, 1][mask], s=point_size, c=colors[mask],alpha=0.5)
ax.legend(handles=legend_elements)
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.savefig('umap_meredig.png', transparent=False)
