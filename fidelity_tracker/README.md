# Overview
As noted in the [QMOF database paper](https://doi.org/10.26434/chemrxiv.13147616), several automated filtering steps were carried out to remove clearly problematic stuctures before carrying out the DFT calculations. However, it is impractical to automatically detect all issues, especially those pertaining to limitations from the X-ray diffraction and crystal refinment process itself. The fidelity tracker is a place to publicly mark any existing issues, which are to be logged in `issue_tracker.txt`. 

## Folder and File Organization
The zipped `opt-cifs` folder contains the current version of DFT-optimized CIFs and their refcodes.

- `opt-cifs/clean`: This folder contains the list of CIFs currently recognized as "clean".
- `opt-cifs/issues`: This folder contains the list of CIFs currently recognized as "issues".

## Structural Fidelity Updates
If you spot a material with an error related to its crystal structure and would like to contribute, please modify the `issue_tracker.txt` file, listing the refcode (including `_FSR`) and the reason it should be flagged.

## Modifying Structures
Since the QMOF database pulls structures directly from the Cambridge Structural Database (CSD) and is not meant to serve as a structure repository, we are not in a position to manually or automatically update CIFs to correct for any potential upstream structural errors. For now, we will just flag any problematic entries for ease-of-reference.
