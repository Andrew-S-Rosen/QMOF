# Searching Tips

## MOFid
Consider this scenario: you know you want to find MOF-5 (also known as IRMOF-1) in the QMOF Database (or any other MOF database for that matter!) but don't know which entry it corresponds to. One way to find the MOF that you're looking for is to take advantage of a tool called [MOFid](https://github.com/snurr-group/mofid). The MOFid code can generate a unique identifier for a given MOF structure. MOFid information is made publicly available with each structure in the QMOF Database, most structures on [mof.tech.northwestern.edu](https://mof.tech.northwestern.edu/), and the 2019 CoRE MOF Database (see the supporting information [here](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.9b01050)). I outline the steps below:

1. Download the CIF of the desired MOF from the internet (e.g. from the original source publication). An example CIF for MOF-5 is [here](https://github.com/iRASPA/RASPA2/blob/master/structures/mofs/cif/IRMOF-1.cif).
2. Calculate its unique MOFid/MOFkey using the [ID Tool](https://snurr-group.github.io/web-mofid/) by simply uploading the structure and hitting submit.
3. Copy down the MOFid and/or MOFkey information. The MOFkey for MOF-5 is Zn.KKEYFWRCBNTPAC.MOFkey-v1.pcu.
4. For the QMOF Database, we provide the MOFids/MOFkeys for every structure, so you can search the `qmof.json` file provided with the QMOF Database for any entries with the obtained MOFkey (or MOFid). The hits returned for MOF-5 are: LISBIZ_FSR, MIBQAR_FSR, SAHYIK_FSR, SAHYOQ_FSR , XOKHAH_FSR, and so on (this is a very popular MOF). If you are using a MOF Database that doesn't have MOFids/MOFkeys pre-computed, you can calculate the MOFids/MOFkeys using the MOFid [Python interface](https://github.com/snurr-group/mofid).
5. If there are multiple options, take the one you like. I would generally recommend the structure with the lowest energy (per atom), if there are any appreciable differences. 
