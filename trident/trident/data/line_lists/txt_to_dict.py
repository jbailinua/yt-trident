import pickle
import csv
import numpy as np

my_dict={}
for line in open('mortcash_lines.txt').readlines():
  online=line.rstrip().split()
  if line.startswith('#'):
    continue
  element, ion_state=online[:2]
  my_dict[element+ion_state]=[]
  
for line in open('mortcash_lines.txt').readlines():
  online=line.rstrip().split()
  if line.startswith('#'):
    continue
  element, ion_state, wavelength, gamma, f_value=online[:5]
  my_dict[element+ion_state].append(np.array([np.float32(wavelength), np.float32(gamma), np.float32(f_value)]))
for key, value in my_dict.items():
  my_dict[key]=np.array(value)

tri_dict={}
for line in open('trident_lines.txt').readlines():
  online=line.rstrip().split()
  if line.startswith('#'):
    continue
  element, ion_state=online[:2]
  tri_dict[element+ion_state]=[]
  
for line in open('trident_lines.txt').readlines():
  online=line.rstrip().split()
  if line.startswith('#'):
    continue
  element, ion_state, wavelength, gamma, f_value=online[:5]
  tri_dict[element+ion_state].append(np.array([np.float32(wavelength), np.float32(gamma), np.float32(f_value)]))
for key, value in tri_dict.items():
  tri_dict[key]=np.array(value)
 
