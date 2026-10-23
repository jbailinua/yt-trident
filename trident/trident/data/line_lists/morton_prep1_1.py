import numpy as np
import csv
import pickle



morton_data=list(csv.reader(open('morton_lines.txt', 'r'), delimiter="\t"))
morton_data=np.array(['blank line' if ((len(entry)==0) or (len(entry[0])==1)) else entry[0] for entry in morton_data[12:]]) #skip header of file and make blank lines explicit
maybe_indeces=[[0, 7], [19, 28], [59, 68], [69, 78], [79, 88]]  #locations of each data type in the file (iion, wavelength, A, gamma, f)

#First, lets find the line numbers where each ion state begins. This part leaves us with different isotopes as well, which we may not want
found_ions=[]
ion_indeces=[]
for i in range(len(morton_data)):
  line=morton_data[i]
  if (line!='blank line'):
      if ((('GROUND' in line) or ('GRND' in line)) and ('No ground' not in line) and (line[:7] not in found_ions)):   #The lines with ion names in them also have 'GROUND' or 'GRND' to specify things about the ground state
        found_ions.append(line[:7])
        ion_indeces.append(i)
        
#Now lets find where all of the multiplets begin. Each is labelled by an energy state
found_mults=[]
mult_indeces=[]
for i in range(len(morton_data)):
  line=morton_data[i]
  if ((line!='blank line') and (i not in ion_indeces) and ('No ground' not in line)):
    try:
      z=int(line[7])
      found_mults.append(line[7:24])
      mult_indeces.append(i)
    except:
      pass

#Now we want to make a mask that only lets in the lines of data we want, ie, the line directly under each multiplet if a mean is taken, and all lines between multiplets if mean is not taken
mult_mask=[False]*4   #we know we don't need the first lines
for i in range(len(mult_indeces)-1):
  current_index, next_index=mult_indeces[i], mult_indeces[i+1]   #This gives us the correct index in morton_data
  if ('MltMean' in morton_data[current_index+1]):
    mult_mask.extend([False, True]+[False]*(next_index-current_index-2))    
    #this gives us a "False" for the line that statrs the multiplet, "True" for the line right after (which actually has the data), and 'False' for the remaining lines in the multiplet
  else:
    mult_mask.extend([False]+[True]*(next_index-current_index-1))
    #This gives us 'False' for the line that starts the multiplet, and 'True' for all lines in the multiplet
#This completes loop above for last entry in mult_indeces
current_index, next_index=mult_indeces[-1], len(morton_data)
if ('MltMean' in morton_data[current_index+1]):
  mult_mask.extend([False, True]+[False]*(next_index-current_index-2))   
else:
    mult_mask.extend([False]+[True]*(next_index-current_index-1))
mult_mask=np.array(mult_mask)
    
#The mask made above gets us the right lines, but includes some text/header information we don't want. We make masks for these too:

noground_mask=np.array([False if (('No ground' in entry) or (entry[:7] in found_ions) or (entry=='blank line')) else True for entry in morton_data]) #gets rid of all "No ground term" lines, 'blank lines', or lines where ions start

#Between this and mult_mask, should have mostly numerical data by now. Should start to assemble in preliminary dictionary
big_mask=(mult_mask*noground_mask)
preliminary_dict={ion:[] for ion in found_ions}
for i in range(len(found_ions)-1):
  ion, start_index, end_index=found_ions[i], ion_indeces[i], ion_indeces[i+1]
  data_chunk, mask_chunk=morton_data[start_index:end_index], big_mask[start_index:end_index]
  for line in data_chunk[mask_chunk]:
    try:
      wavelength=float(line[19:28])
      elow=float(line[32:37])
      if elow==0.:      
        lineprops=[line[19:28], line[69:78], line[59:68], line[79:88]]  #lambda, gamma, A, f are added ONLY if the lower energy state is ground
        preliminary_dict[ion].append(lineprops)
    except:
      pass
#This completes the loop for the last entry
ion, start_index, end_index=found_ions[-1], ion_indeces[-1], len(morton_data)
data_chunk, mask_chunk=morton_data[start_index:end_index], big_mask[start_index:end_index]
for line in data_chunk[mask_chunk]:
  try:     
    wavelength=float(line[19:28])
    elow=float(line[32:37])
    if elow==0.:
      lineprops=[line[19:28], line[69:78], line[59:68], line[79:88]]  #lambda, gamma, A, f
      preliminary_dict[ion].append(lineprops)   
  except:
    pass
    
#This should create a dictionary using ion names as keys and line properties as values, for all ions which have lines in relavent range. If multiplet means are available they are used. Otherwise not. Some properties may be missing for individual lines, especially f-values. In this case, replace with A. 
pickle.dump(preliminary_dict, open('morton_pre_dict', 'wb'))
 

