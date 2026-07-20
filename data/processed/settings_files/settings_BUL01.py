#############################################
# to find "invlib" in the main folder
import sys, os
# path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
# sys.path.insert(0, path)
#############################################

from petro import FourPhaseModel

### DATA ERROR LEVEL ########################
erte =  0.06  # 1 = 100 % (i.e. 0.05 = 5 %)
rste =  0.002 # in seconds (i.e. 0.003 = 3 ms)


### MESH SETTINGS ###########################
paraDX =         0.15 #best of in conventional inversion
paraDX =         0.15    #test PJI
paraMaxCellSize = 5 #Maximum cell size for parametric region in m^2
paraDepth = 40 #Maximum depth for parametric domain, 0 (default) means 0.4 * maximum sensor range
boundary=        1
paraBoundary =   1

### CONVENTIONAL INVERSION SETTINGS #########
##########################################################
# ERT
zWeighte = 0.1 # 0.5
maxItere = 50
lame = 50 # 10

###########################################################
# RST
zWeights = 0.1 # 1.5  # zWeight RST
lams =     50 #20 lambda RST (~50 - 200)
vTop =     200 # Top velocity for gradient stating model
vBottom =   15000 # Bottom velocity for gradient stating model
secNodes = 2
maxIters = 10  # RST

######################################################################
#####################################################################


### JOINT INVERSION SETTINGS ################
zWeight = 0.1  # for values < 1 more smoothing in lateral direction
maxIter = 30 # maximum number of iterations
lam =    50
beta =    10000 #default beta = 10000


# Inversion constraints
poro = 0.25 # porosity 
phi = poro
fr_min = 0.1
fr_max = 0.9
   
# Archie parameter
a=1. #1
m=1.4	# 1.3, 2
n=2.4 	# 2, 2


# Phase VELOCITIES    
vw=1500 # default = 1500
vi=3500 # default = 3500
va=200 # default = 300
vr=6000 # default = 6000

# Phase RESISTIVITIES    
rhow = 100
rhoi=5000
rhoa=10000
rhor=1000

### PLOT SETTINGS ###########################
# Color scale range
cMine =    100 # min value color scale ERT 
cMaxe =    100000# max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    200 # min value color scale RST 
cMaxs =    6000# max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.4
ylimmin = -30

fpm_archie = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 60, 90
yy1, yy2 = -25, -20
landform1 = 'SED'                  