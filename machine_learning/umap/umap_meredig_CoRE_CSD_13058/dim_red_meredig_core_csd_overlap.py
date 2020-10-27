import pandas as pd
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch

seed = 42  # random seed
x1 = os.path.join(
    '..', '..', 'stoichiometric_120', 'CSD-13058', 'meredig_fingerprints_13058.csv') # path to X of dataset 1
x2 = 'meredig_fingerprints_core_fsr.csv' # path to X of dataset 2

#---------------------------------------
# Encoding
X1 = pd.read_csv(x1, delimiter=',', header=0, index_col=0).dropna()
refcodes1 = X1.index.values
X2 = pd.read_csv(x2, delimiter=',', header=0, index_col=0).dropna()
refcodes2 = X2.index.values
X = pd.concat([X1,X2],axis=0)
refcodes = X.index.values

# Perform dimensionality reduction
fit = umap.UMAP(n_neighbors=50, min_dist=0.4, random_state=seed)
u = fit.fit(X)

classifier = np.array(['CSD-13058']*len(refcodes1)+['CoRE-2019']*len(refcodes2))
mask = np.zeros(len(refcodes),dtype=bool)
mask[np.arange(0,len(refcodes1))]=0
mask[np.arange(0,len(refcodes2))]=1

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
plt.savefig('umap_meredig_core_csd_overlap.png', transparent=False)
