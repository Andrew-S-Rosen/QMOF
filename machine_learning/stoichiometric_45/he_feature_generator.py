import numpy as np
import pandas as pd
from ase.io import read
import os
from scipy.stats.mstats import gmean

tabulated_data_path = 'tabulated_data'
xyz_path = os.path.join(
    '..', '..', 'structures_and_band_gaps', 'CSD-13058-SP.xyz')
refcodes_path = 'refcodes.csv'

def get_stats(atomic_nums, tabulated_data):
    vals = np.empty(len(atomic_nums))*np.nan
    for i in range(len(tabulated_data)):
        vals[(atomic_nums == (i+1))] = tabulated_data[i]
    stdmean = np.mean(vals)
    geomean = gmean(np.absolute(vals))
    stdev = np.std(vals)
    maxval = np.max(vals)
    minval = np.min(vals)

    return stdmean, geomean, stdev, maxval, minval

refcodes = np.genfromtxt(refcodes_path, delimiter=',', dtype=str)
group_data = np.genfromtxt(os.path.join(
    tabulated_data_path, 'group.csv'), delimiter=',')
period_data = np.genfromtxt(os.path.join(
    tabulated_data_path, 'period.csv'), delimiter=',')
electroneg_data = np.genfromtxt(
    os.path.join(tabulated_data_path, 'electronegativity.csv'), delimiter=',')
electron_affin_data = np.genfromtxt(
    os.path.join(tabulated_data_path, 'electron_affinity.csv'), delimiter=',')
melting_data = np.genfromtxt(os.path.join(
    tabulated_data_path, 'melting_point.csv'), delimiter=',')+273.15
boiling_data = np.genfromtxt(os.path.join(
    tabulated_data_path, 'boiling_point.csv'), delimiter=',')+273.15
density_data = np.genfromtxt(os.path.join(
    tabulated_data_path, 'density.csv'), delimiter=',')
ionization_data = np.genfromtxt(
    os.path.join(tabulated_data_path, 'ionization_energy.csv'), delimiter=',')

mofs = read(xyz_path, index=':')
data = np.empty((45, len(mofs)))*np.nan
for i, mof in enumerate(mofs):
    print('Generating fingerprint: '+str(i))

    atomic_nums = mof.get_atomic_numbers()
    data_vector = np.empty(45)*np.nan

    data_vector[0] = np.mean(atomic_nums)
    data_vector[1] = gmean(atomic_nums)
    data_vector[2] = np.std(atomic_nums)
    data_vector[3] = np.amax(atomic_nums)
    data_vector[4] = np.amin(atomic_nums)

    data_vector[5:10] = get_stats(atomic_nums, group_data)
    data_vector[10:15] = get_stats(atomic_nums, period_data)
    data_vector[15:20] = get_stats(atomic_nums, electroneg_data)
    data_vector[20:25] = get_stats(atomic_nums, electron_affin_data)
    data_vector[25:30] = get_stats(atomic_nums, melting_data)
    data_vector[30:35] = get_stats(atomic_nums, boiling_data)
    data_vector[35:40] = get_stats(atomic_nums, density_data)
    data_vector[40:45] = get_stats(atomic_nums, ionization_data)

    data[:, i] = data_vector

df = pd.DataFrame(np.transpose(data), index=refcodes)

colnames = ['atomic_num_mean', 'atomic_num_geometric_mean', 'atomic_num_standard_deviation', 'atomic_num_max', 'atomic_num_min',
            'group_num_mean', 'group_num_geometric_mean', 'group_num_standard_deviation', 'group_num_max', 'group_num_min',
            'period_num_mean', 'period_num_geometric_mean', 'period_num_standard_deviation', 'period_num_max', 'period_num_min',
            'electronegativity_mean', 'electronegativity_geometric_mean', 'electronegativity_standard_deviation', 'electronegativity_max', 'electronegativity_min',
            'electron_affinity_mean', 'electron_affinity_geometric_mean', 'electron_affinity_standard_deviation', 'electron_affinity_max', 'electron_affinity_min',
            'melting_mean', 'melting_geometric_mean', 'melting_standard_deviation', 'melting_max', 'melting_min',
            'boiling_mean', 'boiling_geometric_mean', 'boiling_standard_deviation', 'boiling_max', 'boiling_min',
            'density_mean', 'density_geometric_mean', 'density_standard_deviation', 'density_max', 'density_min',
            'ionization_energy_mean', 'ionization_energy_geometric_mean', 'ionization_energy_standard_deviation', 'ionization_energy_max', 'ionization_energy_geometric_min']

df.columns = colnames
df.index.name = 'MOF'
df.to_csv('he_fingerprints.csv', index=True)
