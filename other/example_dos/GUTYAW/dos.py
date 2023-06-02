from ase.io import read
from pychemia.code.vasp import VaspXML
import matplotlib.pyplot as plt
from matplotlib import rc

plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14
rc('text', usetex=True)

mof = read('CONTCAR')
Sr = [atom.index for atom in mof if atom.symbol == 'Sr']
O = [atom.index for atom in mof if atom.symbol == 'O']
C = [atom.index for atom in mof if atom.symbol == 'C']
H = [atom.index for atom in mof if atom.symbol == 'H']
S = [atom.index for atom in mof if atom.symbol == 'S']
VaspXML = VaspXML('vasprun.xml')

colors = {'total':"#4d3c40",
'M':"#7248b7",
'C':'#9c9ec4',
'H':"#a4cb4f",
'O':"#c4529c",
'S':"#77b593",
'N':"#c25243"}

s = [0]
p = [1, 2, 3]
d = [4, 5, 6, 7, 8]
fig, ax = plt.subplots(3, figsize=(4, 6))

dos = VaspXML.dos_total
x = dos.energies
spins = [1]
spinlabels = [r'$\uparrow$', r'$\downarrow$']
for i, spin in enumerate(spins):
	y = dos.dos[:, i+1]*spin
	label = 'Total' if i == 0 else None
	ax[0].plot(x, y, '-', alpha=0.8, label=label, color=colors['total'])
ax[0].axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax[0].axhline(y=0, color='k', linestyle='-')
ax[0].legend(loc='upper left')
ax[0].set_xlim([-12, 12])
ax[0].set_ylim([0,80])
ax[0].xaxis.get_ticklocs(minor=True)
ax[0].yaxis.get_ticklocs(minor=True)
ax[0].minorticks_on()
pdos = VaspXML.dos_parametric(atoms=Sr, spin=[0])
for i, spin in enumerate(spins):
	y = pdos.dos[:, i+1]*spin
	label = 'Sr' if i == 0 else None
	ax[1].plot(x, y, '-', alpha=0.8, label=label, color=colors['M'])
ax[1].axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax[1].axhline(y=0, color='k', linestyle='-')
ax[1].legend(loc='upper left')
ax[1].set_xlim([-12, 12])
ax[1].set_ylim([0,10])
ax[1].xaxis.get_ticklocs(minor=True)
ax[1].yaxis.get_ticklocs(minor=True)
ax[1].minorticks_on()
atoms = [C,H,O,S]
atom_names = ['C','H','O','S']
for j, atom in enumerate(atoms):
	pdos = VaspXML.dos_parametric(atoms=atom, spin=[0])
	for i, spin in enumerate(spins):
		y = pdos.dos[:, i+1]*spin
		label = atom_names[j] if i == 0 else None
		ax[2].plot(x, y, '-', alpha=0.8, label=label, color=colors[atom_names[j]])
ax[2].axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax[2].axhline(y=0, color='k', linestyle='-')
ax[2].legend(loc='upper left',ncol=2,columnspacing=1)

ax[2].set_xlim([-12, 12])
ax[2].set_ylim([0,50])
ax[2].xaxis.get_ticklocs(minor=True)
ax[2].yaxis.get_ticklocs(minor=True)
ax[2].minorticks_on()

ax[2].set_xlabel(r'$E-E_{\mathrm{f}}$ (eV)')
ax[1].set_ylabel(r'Density of states (states/eV)')
plt.tight_layout()
plt.savefig('dos.png',dpi=500)
