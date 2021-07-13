# Important Note
If you are just looking to use PyMOFScreen in your own work, please refer to the parent GitHub page for the [PyMOFScreen package](https://github.com/arosen93/mof_screen). The information below is solely meant to reproduce the QMOF database workflow exactly.

# Running the QMOF database DFT Workflow
This directory contains an example input file for running the automated DFT screening procedure used in constructing the QMOF database.

All that needs to be run on the compute cluster is the `opt.py` file in the `runner` folder, which will call PyMOFScreen to screen MOF CIFs found in the `mofpath` directory. First, configure PyMOFScreen to work with your VASP executables and compute cluster. Refer to the [PyMOFScreen GitHub page](https://github.com/arosen93/mof_screen) for full instructions.

Briefly, you will need to...
1. Modify the `mof_screen/pymofscreen/compute_environ.py` file for your compute cluster's scheduling system and how to call the VASP executables.
2. Install PyMOFScreen by going into the `mof_screen` folder and running `pip install .`.
3. Submit a compute job to run the `opt.py` script in the `runner` folder with Python. The only other component of the submission script that is needed is a line reading `export VASP_SCRIPT=run_vasp.py` (the `run_vasp.py` file will be generated automatically). An example submission script for use with a Slurm scheduler can be found in `sub_slurm.job`.