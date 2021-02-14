# Overview
As noted in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616), several automated filtering steps were carried out to remove clearly problematic stuctures before carrying out the DFT calculations. However, it is impossible to automatically detect all issues, especially those pertaining to limitations from the X-ray diffraction and crystal refinment process itself. The fidelity tracker is a place to publicly mark any existing issues, which are to be logged in [`issue_tracker.txt`](https://github.com/arosen93/QMOF/blob/main/fidelity_tracker/issue_tracker.txt).

## Structural Fidelity Updates
If you spot a material with an error related to its crystal structure and would like to contribute, please do the following:

1. [Fork the repository](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo).
2. Update the [`issue_tracker.txt`](https://github.com/arosen93/QMOF/blob/main/fidelity_tracker/issue_tracker.txt), listing the ID of the structure (including `_FSR`) and the reason for removal.
3. [Commit the change](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/committing-and-reviewing-changes-to-your-project).
4. [Push the change](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/pushing-changes-to-github).
5. [Create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) describing your changes.

## Modifying Structures
Since the QMOF database pulls structures directly from the Cambridge Structural Database (CSD) and is not meant to serve as a structure repository, we are not in a position to manually or automatically update CIFs to correct for any potential upstream structural errors. For now, we will just flag any problematic entries for ease-of-reference.
