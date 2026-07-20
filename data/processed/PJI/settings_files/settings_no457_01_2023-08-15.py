#############################################
# to find "invlib" in the main folder
import sys, os
# path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
# sys.path.insert(0, path)
#############################################

from petro import FourPhaseModel

### DATA ERROR LEVEL ########################
erte =  0.09  # 1 = 100 % (i.e. 0.05 = 5 %)
rste =  0.001 # in seconds (i.e. 0.003 = 3 ms)


### MESH SETTINGS ###########################
paraDX =         0.15 #best of in conventional inversion
paraDX =         1    #test PJI
paraMaxCellSize = 15# Maximum cell size for parametric region in m^2
paraDepth = 40 #Maximum depth for parametric domain, 0 (default) means 0.4 * maximum sensor range
boundary=        1
paraBoundary =   1

### CONVENTIONAL INVERSION SETTINGS #########
# ERT
zWeighte = 0.1
maxItere = 50
lame = 10

# RST
zWeights = 0.1 #0.5  # zWeight RST
lams =     10 # lambda RST (~50 - 200)
vTop =     350 # Top velocity for gradient stating model
vBottom =  15000 # Bottom velocity for gradient stating model
secNodes = 2
maxIters = 10  # RST

######################################################################
#####################################################################


### JOINT INVERSION SETTINGS ################
zWeight = 0.1 # for values < 1 more smoothing in lateral direction
maxIter = 20 # maximum number of iterations
lam =     10
beta =    10000 #default beta = 10000

# Inversion constraints
poro = 0.25 # porosity
phi = poro
fr_min = 0.1
fr_max = 0.9
                     
# Archie parameter
rhow=15
a=1
m=2.8
n=1.1 

# Phase VELOCITIES    
vw=1500
vi=3500
va=100
vr=6000 # default = 6000

# Phase RESISTIVITIES    
rhoi=30000
rhoa=1000000
rhor=5000

### PLOT SETTINGS ###########################
# Color scale range
cMine =    100 # min value color scale ERT 
cMaxe =    100000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    500 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.5
ylimmin = -40

fpm_archie = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 260, 290
yy1, yy2 = -20, -10
landform1 = 'SED'            