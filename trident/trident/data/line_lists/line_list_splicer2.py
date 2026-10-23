import numpy as np
import csv



#We will treat each column in our files seperately. The first task is to organize the data so we have a list of ion names where the name is repeated as many times as there are lines for that ion

#The first thing we want to do is turn every line in the file into a seperate string that can be indexed. Also, create obvious marker for blank lines
tri_data=list(csv.reader(open('trident_lines.txt', 'r'), delimiter="\t"))
tri_data=[entry[0] for entry in tri_data]
morton_data=list(csv.reader(open('morton_lines.txt', 'r'), delimiter="\t"))



#Now we cut large vertical columns down the file and catch *mostly* the data we want. Some of them overlap slightly-- these categories have values on different lines



maybe_ion, maybe_lambda, maybe_A, maybe_gamma, maybe_f=[], [], [], [], []
maybe_line_props0=[maybe_ion, maybe_lambda, maybe_A, maybe_gamma, maybe_f]
maybe_indeces=[[0, 7], [19, 27], [59, 68], [69, 78], [79, 88]]


morton_data=morton_data[12:]
for i in range(len(morton_data)):
  if (len(morton_data[i])==0):
    for prop in maybe_line_props0:
      prop.append('blank line')
  else:
    entry=morton_data[i][0]
    for j in range(len(maybe_line_props0)):
      #print(i, j)
      maybe_line_props0[j].append(entry[maybe_indeces[j][0]:maybe_indeces[j][1]]) 
   
      
maybe_line_props=[np.array(entry) for entry in maybe_line_props0]
ion_mask=[]
for i in range(len(maybe_line_props[0])):
  entry=maybe_line_props[0][i]
  try:
    int(entry[0])
    ion_mask.append(False)
  except:
    if ((' I' in entry) or (' V' in entry)):
      ion_mask.append(True)
    else:
      ion_mask.append(False)
      
ion_mask=np.array(ion_mask)
ground_term_mask=np.array([False if 'No g' in entry else True for entry in maybe_A])

#This just makes a list with each ion listed exactly once, in the right order
ion_list=[]
for entry in maybe_line_props[0][ion_mask*ground_term_mask]:
  if entry not in ion_list:
    ion_list.append(entry)
    


#Now we want to make a mask that only reveals multiplet mean values
#mtlmean_mask=np.array([True if 'MltMean' 
#for i in range(len(maybe_line_props[0])):
#  if 

"""
#Now we make a mask for where we have line groupings. We will use chunks of this mask corresponding to each ion later
grouping_starts=[]
mean_starts=[]
for i in range(len(maybe_line_props[0])):
  if ((('u' in maybe_line_props[0][i]) or ('v' in maybe_line_props[0][i])) and ('.' in maybe_line_props[0][i])):
    print(maybe_line_props[0][i])
    grouping_starts.append(i)
  elif ('MltMean' in maybe_line_props[0]):
    grouping_starts.append(i)
    mean_starts.append(i)

#for i in range(len(morton_data)-1):
#  if (i in grouping_starts):
#    end_index=grouping_starts(np.where(grouping_starts==i)[0][0]+1)
#    if (i in mean_starts):
      

#Now we will construct a dictionary with ions as keys and the properties of their lines as values
preliminary_dict={}
done_ions=[]
for i in range(len(ion_list)-1):
#for i in range(10):
  current_ion, next_ion=ion_list[i], ion_list[i+1] #this line is dumb, but it lets me use both "for entry in..." and "for i in range..." syntax
  if (current_ion not in done_ions):
    starting_index, ending_index=np.where(maybe_line_props[0]==current_ion)[0][0], np.where(maybe_line_props[0]==next_ion)[0][0] #this tells us where in the total data the info on this ion starts
    preliminary_dict[current_ion]=[np.array(prop[starting_index:ending_index]) for prop in maybe_line_props[1:]]
    for j in range(starting_index, ending_index):
      if ('.' in maybe_line_props[0][j]):
        print([prop[j] for prop in maybe_line_props])
    done_ions.append(entry)
    print('\n')
#Now for last ion, which is left out of loop
current_ion=ion_list[-1]
starting_index=np.where(maybe_line_props[0]==current_ion)[0][0]
preliminary_dict[current_ion]=[np.array(prop[starting_index:]) for prop in maybe_line_props[1:]]
    

for i in range(10):
  current_ion=maybe_line_props[0][ion_mask][i]  #this line is dumb, but it lets me use both "for entry in..." and "for i in range..." syntax
  next_ion=maybe_line_props[0][ion_mask][i+1]
  if (current_ion not in done_ions):
    starting_index, ending_index=np.where(maybe_line_props[0]==current_ion)[0][0], np.where(maybe_line_props[0]==next_ion)[0][0] #this tells us where in the total data the info on this ion starts
    for j in range(starting_index, ending_index):
      if 
 """ 


