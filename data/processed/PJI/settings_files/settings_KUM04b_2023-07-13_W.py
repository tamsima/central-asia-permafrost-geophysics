# -*- coding: utf-8 -*-
"""

"""
#############################################
# to find "invlib" in the main folder
import sys, os
#path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
#sys.path.insert(0, path)
#############################################
#############################################
from petro import FourPhaseModel
### DATA ERROR LEVEL ########################
erte =  0.09   # 1 = 100 % (i.e. 0.05 = 5 %)
rste =  0.001  # in seconds (i.e. 0.003 = 3 ms)

### MESH SETTINGS ###########################
paraDX =         0.5 #best of in conventional inversion
# paraDX =         1    #test PJI
paraDepth =      50
paraMaxCellSize= 10    #best of in conventional inversion
# paraMaxCellSize= 15    #test PJI
boundary=        1
paraBoundary =   1

### CONVENTIONAL INVERSION SETTINGS #########
# ERT
zWeighte = 0.2 # zWeiht ERT
lame =     10 # lambda ERT (~10 - 50)
maxItere = 10  # ERT

# RST
zWeights = 0.2 # zWeight RST
lams =     25 # lambda RST (~50 - 200)
vTop =     300 # Top velocity for gradient stating model
vBottom =  15000 # Bottom velocity for gradient stating model
secNodes = 2
maxIters = 10  # RST

#############################################################################
### JOINT INVERSION SETTINGS ################
zWeight = 0.25 # for values < 1 more smoothing in lateral direction
maxIter = 40 # maximum number of iterations
lam =     30
beta =    10000 #default = 10000

# Inversion constraints
poro = 0.3 # porosity
phi = poro
fr_min = 0.1 # 0.4
fr_max = 0.9
                     
# Archie parameter
rhow=2. #best of PJI
a=1.     #best of PJI
m=3      #best of PJI
n=1      #best of PJI

# Phase VELOCITIES    
vw=1500
vi=3500
va=200 # default = 300
vr=8000 # default = 6000

# Phase RESISTIVITIES    
rhoi=2000
rhoa=100000
rhor=1000

### PLOT SETTINGS ###########################
# Color scale range
cMine =    100 # min value color scale ERT 
cMaxe =    10000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    500 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.5

###############################################################################
fpm_archie = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 260, 290
yy1, yy2 = -20, -10
landform1 = 'SED'    