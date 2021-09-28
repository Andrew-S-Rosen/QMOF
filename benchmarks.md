# ML Model Results

## Overview
When trained on 80% of [QMOF Database v13](https://figshare.com/articles/dataset/QMOF_Database/13147324/13), the testing set ML results for band gap prediction are as follows:
 
| Method | MAE (eV) | R^2 | ρ |
| ----------- | ----------- | ----------- | ----------- |
| Mean of Dataset | 0.940 | --- | --- |
| Sine Matrix Eigenspectrum | 0.539 ± 0.004 | 0.606 ± 0.007 | 0.776 ± 0.004 |
| Stoichiometric-45 | 0.459 ± 0.005 | 0.705 ± 0.007 | 0.826 ± 0.003 |
| Stoichiometric-120 | 0.454 ± 0.006 | 0.713 ± 0.007 | 0.829 ± 0.005 |
| Orbital Field Matrix | 0.410 ± 0.004 | 0.749 ± 0.006 | 0.861 ± 0.002 |
| Average SOAP kernel | 0.344 ± 0.004 | 0.826 ± 0.002 | 0.913 ± 0.001 |
| CGCNN | TBD | TBD | TBD |

You can download the corresponding features for QMOF Database v13 [here](https://nuwildcat.sharepoint.com/:f:/s/TGS-QMOF/Es-51y1ZLmlDmoYOemYqArsBMtyAmG5qAs6UBFHh3C968g?e=0PIJsg).
