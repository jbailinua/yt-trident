import numpy as np
import csv
import pickle


#This script takes partially processed Morton data and tries to fill in some missing values
#These are dictionaries that will hold masks for each ion saying if they have proper gamma/A values or not
preliminary_dict=pickle.load(open('morton_pre_dict', 'rb'))


#This removes isotopes from our database, as their lines are too close for us to resolve anyways
fixed_dict0={}
for ion in preliminary_dict.keys():
  try:
    ion_test=int(ion[0])
  except:
    if (ion!='D I    '):
      fixed_dict0[ion]=[]
#Since we removed some keys above, go only by keys of fixed_dict0
used_A0={ion:[] for ion in fixed_dict0.keys()}   
no_gamma_no_A0={ion:[] for ion in fixed_dict0.keys()}
#fixed_dict0, used_A0, no_gamma_no_A0={ion:[] for ion in preliminary_dict.keys()}, {ion:[] for ion in preliminary_dict.keys()}, {ion:[] for ion in preliminary_dict.keys()}


for ion in fixed_dict0.keys():
#for ion in preliminary_dict.keys():
  for line in preliminary_dict[ion]:
    try:  #If we have both values and everything seems fine, just pass line to new dict
      new_gamma=float(line[1])  
      used_A0[ion].append(False)
      no_gamma_no_A0[ion].append(False)
      fixed_dict0[ion].append(line+['Morton'])
    except:
      try:  #If we have only A, use that for gamma as well and pass new line to new dict
        new_gamma=float(line[2])  
        used_A0[ion].append(True)
        no_gamma_no_A0[ion].append(False)
        fixed_dict0[ion].append([line[0], line[2], line[2], line[3], 'Morton'])
      except:  #If we have neither gamma nor A, we just pass line to new dict and hope to figure it out later. Many of these also have no f-values
        used_A0[ion].append(False)
        no_gamma_no_A0[ion].append(True)
        fixed_dict0[ion].append([line[0]]+3*['blank']+['Morton'])
        

#Ok, now we have to turn everything into arrays so the dumb masks will work. I wanted to make everything floats too, but can't because arrays must all be same data type
fixed_dict={ion.strip():np.array(fixed_dict0[ion]) for ion in fixed_dict0.keys()}
used_A={ion.strip():np.array(used_A0[ion]) for ion in used_A0.keys()}
no_gamma_no_A={ion.strip():np.array(no_gamma_no_A0[ion]) for ion in no_gamma_no_A0.keys()}

morton_dict={'fixed_dict':fixed_dict, 'used_A':used_A, 'no_gamma_no_A':no_gamma_no_A}
pickle.dump(morton_dict, open('morton_dict', 'wb'))
  

