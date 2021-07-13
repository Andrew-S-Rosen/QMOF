import os
import pandas as pd

# Settings
cif_folder_path = '/path/to/cifs'  # path to folder of CIFs
new_cif_folder_path = '/path/to/cifs_with_charges'  # path to folder to store new CIFs
charge_xlsx_path = '/path/to/ddec.xlsx'  # path to .xlsx file of (e.g. DDEC) charges
sheet_name = 'partial_charges_PBE' # sheet name in .xlsx with charge data
last_loop_flag = '_atom_site_type_symbol' # last flag in loop_ above atom symbols in CIF

# Make new folder to store new CIFs
if not os.path.exists(new_cif_folder_path):
	os.mkdir(new_cif_folder_path)

# Get all CIFs
cifs = os.listdir(cif_folder_path)
cifs.sort()

# Get charges
df_charges = pd.read_excel(charge_xlsx_path, index_col=0, header=None,
						sheet_name=sheet_name, engine='openpyxl')

# Write out new CIFs
for cif in cifs:

	# Initialize variables
	new_cif = ''
	i = 0
	write_charges = False

	# Parse old cif and add new column
	with open(os.path.join(cif_folder_path,cif), 'r') as f:

		# Charges for this MOF
		charges = df_charges.loc[cif.split('.cif')[0]]
		charges = charges.dropna()

		# Loop through old CIF
		for line in f:

			if last_loop_flag in line:
				new_cif += line + ' _atom_site_charge\n'
				write_charges = True
				continue

			if i == len(charges):
				write_charges = False
			
			if write_charges:
				new_cif += line.strip() + '  ' + str(charges.iloc[i]) + '\n'
				i += 1
			else:
				new_cif += line

	# Write out new CIF
	with open(os.path.join(new_cif_folder_path,cif),'w') as f:
		f.write(new_cif)
