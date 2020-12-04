import pandas as pd
import umap
import umap.plot
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import output_file, save
import os

seed = 42  # random seed
x = os.path.join(
	'..', '..', 'stoichiometric_120', 'CSD-13058', 'meredig_fingerprints.csv') # .csv of X encodings

# ---------------------------------------
# Encoding
X = pd.read_csv(x, delimiter=',', header=0, index_col=0).dropna()
refcodes = X.index.values
maxZ = X['range Number']+1

# Perform dimensionality reduction
fit = umap.UMAP(n_neighbors=50, min_dist=0.4, random_state=seed)
u = fit.fit(X)

# Make static plot
points = u.embedding_
width = 8500
height = 8500
point_size = 100.0 / np.sqrt(points.shape[0])
dpi = 1000
plt.rcParams["figure.dpi"] = dpi
fig = plt.figure(figsize=(width / dpi, height / dpi))
ax = fig.add_subplot(111)
sc = ax.scatter(points[:, 0], points[:, 1], s=point_size, c=maxZ, cmap='turbo')
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
cb = plt.colorbar(sc, aspect=25)
cb.ax.minorticks_on()
cb.set_ticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
cb.ax.tick_params(labelsize=14)
plt.savefig('umap_13058_Z.png', transparent=False)

# Make interactive plot
hover_data = pd.DataFrame({'Refcode': refcodes, 'maxZ': maxZ})
p_int = umap.plot.interactive(
	u, labels=maxZ, color_key_cmap='turbo', hover_data=hover_data, point_size=2)
output_file('umap_13058_Z.html')
save(p_int)
