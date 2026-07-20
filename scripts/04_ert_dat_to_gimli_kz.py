# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 05:09:34 2021
- Makes _rhoa.txt file that is needed for the inversion and plotting of ERT data

Transforms data from Res2DInv format (.dat) to unified dataformat that is needed in pygimli
ATTENTION:This script only works if there are two txt or dat files. The .dat file HAS TO BE ONLY NUMBERS
So all strings need to be deleted from that file first.

ATTENTION: Depending on which configuration (Wenner, Dipol-Dipol,..) was used, this should be adapted in the end!
@author: MathysT
"""
import pygimli as pg
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
import pandas as pd
from pygimli.physics import ert
import matplotlib.pyplot as plt
import math

# %% ATTENTION: CHANGE Profile name
config = 'W' # doesnt matter
profile = 'gl09_2024-08-13_W5m'
###############################################################################

path = r'C:\Users\mathyst\switchdrive\Geophysics\pyGIMLi\data_unified\ERT'
os.chdir(path)
extension = '.dat'
source = os.path.join(path,profile)+'.dat'

if os.path.isdir(os.path.join(path, profile)) == True:
    print('Directory already exists')
else:
    os.mkdir(os.path.join(path, profile))

    
destination_folder = os.path.join(path, profile)
shutil.copy(source, destination_folder)
topo_source = os.path.join(path,profile)+'_topo.txt'
shutil.copy(topo_source, destination_folder)
os.chdir(os.path.join(path, profile))

#Write new file for inversion
fileW = profile+'_rhoa.txt' # Creates a new txt file to write into
fileR = profile+'.dat' # This is where the resistivity data is stored
fileTopo = profile+'_topo.txt' # Topo file (should contain no strings!)

data=np.loadtxt(fileR) # load data file 
topo=np.loadtxt(fileTopo) # load topo file 

# Get one array of the altitude values (z)
z = topo[:,1] 


f=open(fileR,'r') # open file to read only
n=0
for line in f: # read line after line
  n+=1  # number of measurements
f.close()

# Retrieve the number of topography points
f=open(fileTopo,'r')
t=0
for line in f: # read line after line
  t+=1  # number of topography point
f.close()

fw=open(fileW,'w') # open file to write into
fw.write('%i \t # Number of sensors \n# x z \n'  %t)
for i in range(t) : 
    fw.write('%.2f %.2f \n' %(topo[i][0],z[i]))
fw.write('%i \t # Number of measurements \n# a b m n rhoa err\n'  %n)

# write electrode positions, apparent resistivity (rhoa) and err (set to 0.01 here)
spacing = topo[1][0] - topo[0][0]

for i in range(n) :  # write into 3 columns: shoot position - geophone position - rhoa 
    if config == 'W':
        fw.write('%i %i %i %i %.2f %.3f \n' %((data[i][1]/spacing+1), (data[i][3]/spacing+1), data[i][5]/spacing+1, data[i][7]/spacing+1,data[i][9], 0.04)) 
    elif config == 'DD':
        fw.write('%i %i %i %i %.2f %.3f \n' %((data[i][1]/spacing+1), (data[i][3]/spacing+1), data[i][5]/spacing+1, data[i][7]/spacing+1,data[i][9], 0.04)) 
      #fw.write('%i %i %i %i %7.2f\n' %(data[i][0]/data[0][1]+1, (data[i][0]+3*data[i][1])/data[0][1]+1, (data[i][0]+1*data[i][1])/data[0][1]+1, (data[i][0]+2*data[i][1])/data[0][1]+1, data[i][2])) 
      #fw.write('%i %i %i %i %7.2f %5.2f\n' %(data[i][0]/data[0][1]+1, (data[i][0]+3*data[i][1])/data[0][1]+1, (data[i][0]+1*data[i][1])/data[0][1]+1, (data[i][0]+2*data[i][1])/data[0][1]+1, data[i][2]/(2*np.pi*2), data[i][5]+0.01)) 
fw.close()

print('ERT file ready')
