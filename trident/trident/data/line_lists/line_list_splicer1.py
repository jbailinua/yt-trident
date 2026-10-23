import numpy as np
import csv



#We will treat each column in our files seperately. The first task is to organize the data so we have a list of ion names where the name is repeated as many times as there are lines for that ion

#The first thing we want to do is turn every line in the file into a seperate string that can be indexed. Also, create obvious marker for blank lines
trid_data=list(csv.reader(open('trident_lines.txt', 'r'), delimiter="\t"))
trid_data=[entry[0] for entry in trid_data]
morton_data=list(csv.reader(open('morton_lines.txt', 'r'), delimiter="\t"))
morton_data1=[]
for entry in morton_data:
  if (len(entry)==0):
    morton_data1.append('blank line')
  elif (entry[0]==' '):
    morton_data1.append('blank line')
  else:
    morton_data1.append(entry[0])


#Now we want to find where the entry for each ion starts in the file
morton_start_points=[i for i in range(len(morton_data1)) if (('IP = ' in morton_data1[i]) and ('no ground-term lines' not in morton_data1[i]))]
morton_start_points.append(len(morton_data1))

#This finds us the names of the ions
ion_names=[morton_data1[i][0:7] for i in morton_start_points]
morton_name_column, morton_id, morton_gamma, morton_f, mysource=[], [], [], [], []

#Now we want a list where we have the name of the ion repeated once for each spectral line it has
for i in range(len(morton_start_points)-1):
  ion_name, ion_start, ion_end=ion_names[i], morton_start_points[i], morton_start_points[i+1]
  for entry in morton_data1[ion_start:ion_end]:
    if ((' Ref ' in entry) and ('IP = ' not in entry)):
    #This part gets the unique identifier for the transition/transition group
      j_position=entry.find('J=')
      if (j_position==-1):
        identifier=entry[7:28]
      else:
        identifier=entry[7:j_position]
      
    if (('MltMean' not in entry[:7]) and ('u' not in entry[:7]) and ('v' not in entry[:7])):
      morton_name_column.append(ion_name)
      morton_id.append(
 


#Now we do similar for Cashman table


