import numpy as np
import csv
import pickle


#This file compares and compiles info from 3 spectral files
#First we load pre-processed Morton:
morton_dict=pickle.load(open('morton_dict', 'rb'))
m_dict, used_A, no_A=morton_dict['fixed_dict'], morton_dict['used_A'], morton_dict['no_gamma_no_A']

#Now we load up Trident
tri_data, tri_dict0=[], {}
for line in open('trident_lines.txt').readlines():
  online=line.rstrip().split()
  if line.startswith("#") or len(online) < 5:
    continue
  ion=' '.join(online[0:2])
  tri_dict0[ion]=[]
  tri_data.append(line)
  
for ion in tri_dict0.keys():
  for line in tri_data:
    if ion in line:
      tri_dict0[ion].append([line[15:26], line[30:42], 'None in Trident', line[46:58], 'Trident'])

#And now Cashman
cashman_data, cashman_dict0=[], {}
for line in open('cashman_lines.txt').readlines():
  if line.startswith('#'):
    continue
  online=line.rstrip().split()
  ion=' '.join(online[1:3])
  
  cashman_dict0[ion]=[]
  cashman_data.append(line)
  
for ion in cashman_dict0.keys():
  for line in cashman_data:
    if ion in line:
      cashman_dict0[ion].append([line[90:98], 'None in Cashman', 'None in Cashman', line[105:113], 'Cashman'])
      
#Now we turn everything into arrays
cashman_dict={ion:np.array(lines) for ion, lines in cashman_dict0.items()}
tri_dict={ion:np.array(lines) for ion, lines in tri_dict0.items()}

#FINALLY, we start comparing!
#m_cash_dict={}
shared_ions=[ion for ion in cashman_dict.keys() if ion in m_dict.keys()]
exclusive_ions_m=[ion for ion in m_dict.keys() if ion not in cashman_dict.keys()]  #These ions are only in Morton 
exclusive_ions_cash=[ion for ion in cashman_dict.keys() if ion not in m_dict.keys()] #These ions are only in Cashman, so we can't use due to lack of gamma/A values. But we do have one of these ions in Trident (Ar I), so maybe we'll use Trident data for that one
#shared_lines, exclusive_lines={}


#First we deal with shared ions between Morton/Cashman
d_lambda_threshold=0.4
combined_dict0={ion:[] for ion in shared_ions}
for ion in shared_ions:
  m_data, c_data=m_dict[ion], cashman_dict[ion]
  #We want to replace line data present in Morton with that present in Cashman, where available. So check each Morton line-->if in Cashman, replace values.
  #If not in Cashman, keep Morton values. For values that ARE in Cashman, but not Morton, we don't have full data (unless data is in Trident....)
  
  #If len(data)==1, make it a list--> an array, to get array len 1 which is iterable, when array len 0 is not. We can't just make them all array([]) first, as it turns non-len1 lists into len1 lists
  if (len(c_data)==1 and len(m_data)==1):
    lambda_m, lambda_c=np.float64([m_data[:, 0]]), np.float64([c_data[:, 0]])
    print(ion, 'both 1')
  elif (len(c_data)==1):
    lambda_m, lambda_c=np.float64(m_data[:, 0]), np.float64([c_data[:, 0]])
    print(ion, 'c_data 1')
  elif (len(m_data)==1):
    lambda_m, lambda_c=np.float64([m_data[:, 0]]), np.float64(c_data[:, 0])
    print(ion, 'm_data 1')
  else:
    lambda_m, lambda_c=np.float64(m_data[:, 0]), np.float64(c_data[:, 0])
    print(ion, 'none 1')
  for i in range(len(m_data)):
    deltas=np.array(abs(lambda_m[i]-lambda_c))  #shape of _lambda_c
    if min(deltas)<d_lambda_threshold:
      #We found Cashman line very close to Morton--> should replace M data with C data for this line
      cashman_index=np.where(deltas==min(deltas))[0][0]  #this is where data is located in Cashman. Have to do extra indexing because np.where can return several indeces
      line_info=np.array([c_data[cashman_index, 0], m_data[i, 1], m_data[i, 2], c_data[cashman_index, 3], 'MortCash']) #we now have a mixture of Morton/Cashman data
      combined_dict0[ion].append(line_info)
    else:
      #There's no line in Cashman to match this line in Morton--> just use Morton data
      combined_dict0[ion].append(m_data[i])

#We now have a dictionary of shared ions between Morton/Cashman. For each shared ion, if a line was in Morton and Cashman, now has updated Cashman data. If line in Cashman but not Morton, do not have full data. 

#Now, add in any Morton ions not covered by Cashman
for ion in exclusive_ions_m:
  combined_dict0[ion]=m_dict[ion]
  
for ion, lines in combined_dict0.items():
  combined_dict0[ion]=np.array(lines)  
#Without using Trident data to fill in blanks, this is as far as we can go. We have a spectral file!
pickle.dump(combined_dict0, open('mortcash_dict', 'wb'))

#This shows us where we still have blanks in the data
final_blank_dict={}
ion_column, lambda_column, gamma_column, f_column, source_column=[], [], [], [], []
for ion, lines in combined_dict0.items():
  blanks=np.array([True if 'blank' in line else False for line in lines])
  final_blank_dict[ion]=blanks
  ion_column.extend([ion]*len(lines[~blanks]))
  lambda_column.extend(lines[~blanks, 0])
  gamma_column.extend(lines[~blanks, 1])  #A is index 2, but we only use if we don't have f
  f_column.extend(lines[~blanks, 3])
  source_column.extend(lines[~blanks, 4])

datafile='try1.txt'
data=np.column_stack([ion_column, lambda_column, gamma_column, f_column, source_column])
np.savetxt(datafile, data, fmt=['%- 6s', '% 09s', '% 9s', '%- 9s', '% 8s'])





















