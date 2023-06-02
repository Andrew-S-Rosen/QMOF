import os
import numpy as np
import time
from shutil import copyfile, rmtree, move
from ase.io import read, write
from ase.neb import NEB
from pymofscreen.janitor import clean_files

def nebmake(initial_atoms,final_atoms,n_images):
	"""
	Make interpolated images for NEB
	Args:
		initial_atoms (ASE Atoms object): initial MOF structure
		
		final_atoms (ASE Atoms object): final MOF structure

		n_images (int): number of NEB images
	"""
	pwd = os.getcwd()
	neb_path = os.path.join(pwd,'neb')
	if os.path.exists(neb_path):
		rmtree(neb_path)
	os.makedirs(neb_path)
	os.chdir(neb_path)

	images = [initial_atoms]
	images.extend(initial_atoms.copy() for _ in range(n_images))
	images.append(final_atoms)

	neb = NEB(images)
	neb.interpolate('idpp',mic=True)
	for i, neb_image in enumerate(neb.images):
		ii = f'0{str(i)}' if i < 10 else str(i)
		os.mkdir(os.path.join(neb_path,ii))
		write(os.path.join(neb_path,ii,'POSCAR'),neb_image,format='vasp')
	write_dummy_outcar(os.path.join(neb_path,'00','OUTCAR'),initial_atoms.get_potential_energy())
	write_dummy_outcar(os.path.join(neb_path,ii,'OUTCAR'),final_atoms.get_potential_energy())

def write_dummy_outcar(name,E):
	"""
	Construct a dummy OUTCAR for images 0 and n
	Args:
		name (string): name of file to write

		E (float): energy to write out in dummy OUTCAR
	"""
	with open(name,'w') as wf:
		wf.write(
			f'  energy  without entropy=                   energy(sigma->0) =     {str(E)}'
			+ '\n'
		)

def neb2dim():
	"""
	Construct initial dimer job from NEB
	"""
	pwd = os.getcwd()
	neb_path = os.path.join(pwd,'neb')
	os.chdir(neb_path)
	os.system('vfin.pl neb_fin')
	time.sleep(5)
	neb_fin_path = os.path.join(neb_path,'neb_fin')
	os.chdir(neb_fin_path)
	os.system('nebresults.pl')
	copyfile(os.path.join(neb_fin_path,'exts.dat'),os.path.join(neb_path,'exts.dat'))
	os.chdir(neb_path)
	if os.stat(os.path.join(neb_path,'exts.dat')).st_size == 0:
		raise ValueError('Error with exts.dat file')
	os.system('neb2dim.pl')
	old_dim_path = os.path.join(neb_path,'dim')
	new_dim_path = os.path.join(pwd,'dim')
	move(old_dim_path,new_dim_path)
	os.chdir(new_dim_path)
	mof = read('POSCAR')

	max_F = 0
	high_i = 0
	if os.stat(os.path.join(neb_fin_path,'nebef.dat')).st_size == 0:
		raise ValueError('nebef.dat not written')
	with open(os.path.join(neb_fin_path,'nebef.dat'),'r') as rf:
		for i, line in enumerate(rf):
			line = line.strip()
			max_F_temp = np.fromstring(line,dtype=float,sep=' ')[1]
			if max_F_temp > max_F:
				max_F = max_F_temp
				high_i = i
	try:
		str_high_i = f'0{str(high_i)}' if high_i < 10 else str(high_i)
		move(os.path.join(neb_fin_path,str_high_i,'WAVECAR.gz'),os.path.join(new_dim_path,'WAVECAR.gz'))
		os.system('gunzip WAVECAR.gz')
	except:
		pass

	return mof

def dimmins(dis):
	"""
	Run dimmins.pl
	Args:
		dis (float): displacement vector
	"""
	os.system('vfin.pl dim_fin')
	rmtree('dim_fin')
	os.system(f'dimmins.pl POSCAR MODECAR {str(dis)}')

def nebef(ediffg):
	"""
	Run nebef.pl
	Args:
		ediffg (float): specified EDIFFG vlaue in VASP

	Returns:
		neb_conv (bool): True if NEB converged within EDIFFG
	"""
	ediffg = abs(ediffg)
	clean_files(['POSCAR'])
	open('nebef.dat','w').close()
	os.system('nebef.pl > nebef.dat')
	max_F = 0
	if os.stat('nebef.dat').st_size == 0:
		raise ValueError('nebef.dat not written')
	with open('nebef.dat','r') as rf:
		for line in rf:
			line = line.strip()
			max_F_temp = np.fromstring(line,dtype=float,sep=' ')[1]
			if max_F_temp > max_F:
				max_F = max_F_temp
	return max_F != 0.0 and max_F <= ediffg