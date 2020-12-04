# Overview
As noted in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616), several automated filtering steps were carried out to remove clearly problematic stuctures before carrying out the DFT calculations. However, it is impractical to automatically detect all issues, especially those pertaining to limitations from the X-ray diffraction and crystal refinment process itself.

## Folder and File Organization
The `opt-cifs` folder contains the current version of DFT-optimized CIFs and their refcodes.

- `opt-cifs/clean`: This folder contains the list of CIFs currently recognized as "clean".
- `opt-cifs/issues`: This folder contains the list of CIFs currently recognized as "issues".

## Structural Fidelity Updates
If you spot a material with an error related to its crystal structure and would like to contribute, please carry out the following steps.

1. [Fork the repository](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo).
2. On your branch, move the potentially problematic CIFs from `fidelity_tracker/opt-cifs/clean` to `fidelity_tracker/opt-cifs/issues`.
3. [Commit the change](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/committing-and-reviewing-changes-to-your-project).
4. [Push the change](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/pushing-changes-to-github).
5. [Create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) describing your changes.

## Modifying Structures
Since the QMOF database pulls structures directly from the Cambridge Structural Database (CSD) and is not meant to serve as a structure repository, we are not in a position to manually or automatically update CIFs to correct for any potential upstream structural errors. For now, we will just flag any problematic entries for ease-of-reference.

## Computed Properties
We encourage you to independently supplement the QMOF database with your own data however you see fit. However, we currently do not have an infrastructure set up to systematically accept user contributions for additional VASP-computed properties. Please contact the authors if you wish to discuss options further.
