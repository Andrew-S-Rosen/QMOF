NOTE: This is a work in progress.

# Overview
As noted in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616), several automated filtering steps were carried out to remove clearly problematic stuctures before carrying out the DFT calculations. However, it is impractical to automatically detect all issues, especially those pertaining to limitations from the X-ray diffraction and crystal refinment process itself. This section of the GitHub repository attempts to address this, at least in part.

## Folder and File Organization
### CSD-opt
This folder contains the current version of DFT-optimized CIFs and their refcodes.

- `cifs/clean`: This folder contains the list of CIFs currently recognized as "clean".
- `cifs/issues`: This folder contains the list of CIFs currently recognized as "issues".
- The `CSD-clean-opt.xyz.gz` file is a gzip'd `.xyz` of the CIFs in `cifs/clean`.
- The `CSD-clean-opt-refcodes.csv` file is a list of refcodes associated with the `CSD-clean-opt.xyz.gz` file. You can also check this file to see which ones are marked as "clean" instead of unpacking the entire `cifs.tar.gz` file.


## Structural Fidelity Updates
If you spot a structure with an error related to its crystal structure and would like to contribute, please carry out the following steps.

If it's in the DFT-optimized structure list:
1. [Fork the repository](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo).
2. Go to `dev_tools/CSD-opt`. Unpack the `cifs.tar.gz` folder (i.e. `tar -xf cifs.tar.gz`) and then move the potentially problematic CIFs from `cifs/clean` to `cifs/issues`.
3. Delete the existing `.xyz.gz` file in `dev_tools/CSD-opt`.
4. Run `dev_cifs_to_xyz.py`. This will create a new (gzip'd) `.xyz` and a new refcodes `.csv` in `CSD-opt`.
5. Re-compress the `CSD-opt` folder (i.e. `tar -czvf cifs.tar.gz cifs`). This is important so that users don't unpack thousands of individual files anytime they clone the GitHub repo.
6. [Push the change](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/pushing-changes-to-github).
7. [Create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Modifying Structures
Since the QMOF database pulls structures directly from the Cambridge Structural Database (CSD) and is not meant to serve as a structure repository, we are not in a position to manually or automatically update CIFs to correct for any potential upstream structural errors. For now, we will typically just flag entries accordingly for ease-of-reference.

## Computed Properties
We encourage you to independently supplement the QMOF database with your own data however you see fit. However, we currently do not have an infrastructure set up to systematically accept user contributions for additional VASP-computed properties. Please contact the authors if you wish to discuss options further.
