from pymofscreen.screen import screener
from pymofscreen.default_calculators import defaults
import os

# Specifies paths
basepath = os.path.join(os.getcwd(), '..')  # path to store results
mofpath = os.path.join(basepath, 'mofpath')  # path where MOF CIFs are
submit_script = 'sub_slurm.job'  # path to job submission script

# Modifies the defaults in `default_calculators.py
defaults['algo'] = 'Fast'

# Get CIF files
cif_files = os.listdir(mofpath)
cif_files.sort()
s = screener(basepath, mofpath, submit_script=submit_script, kppas=[100, 1000])

# Run DFT calculations
for cif_file in cif_files:
	mof = s.run_screen(cif_file, 'volume', spin_levels=['high'], acc_levels=[
					   'scf_test', 'isif2_lowacc', 'isif3_lowacc', 'isif3_highacc', 'final_spe'])
