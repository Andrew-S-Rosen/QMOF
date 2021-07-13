import numpy as np

#Refer to magmom_handler.py for usage of variables defined here
dblock_metals = np.concatenate((np.arange(21,30,1),np.arange(39,48,1),
	np.arange(71,80,1),np.arange(103,112,1)),axis=0).tolist()
fblock_metals = np.concatenate((np.arange(57,71,1),np.arange(89,103,1)),
	axis=0).tolist()
mag_list = dblock_metals+fblock_metals
nomag_list = [val for val in np.arange(1,119,1) if val not in dblock_metals+fblock_metals]
