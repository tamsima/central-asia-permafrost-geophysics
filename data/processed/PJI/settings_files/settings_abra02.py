#############################################

#############################################

from petro import FourPhaseModel

### DATA ERROR LEVEL ########################
erte =  0.08  # 1 = 100 % (i.e. 0.05 = 5 %)
rste =  0.0017 # in seconds (i.e. 0.003 = 3 ms)

### MESH SETTINGS ###########################
paraDX =         0.15 #best of in conventional inversion
paraDX =         1    #test PJI
paraMaxCellSize = 15# Maximum cell size for parametric region in m^2
paraDepth = 40 #Maximum depth for parametric domain, 0 (default) means 0.4 * maximum sensor range
boundary=        1
paraBoundary =   1

### CONVENTIONAL INVERSION SETTINGS #########
# ERT
# Parameters
zWeighte = 0.9
maxItere = 50
lame = 10

# RST
zWeights = 0.9 # zWeight RST
lams =     1 # lambda RST (~50 - 200)
vTop =     350 # Top velocity for gradient stating model
vBottom =  12000 # Bottom velocity for gradient stating model
secNodes = 2
maxIters = 10  # RST

################################################################################
#  JOINT INVERSION
###############################################################################

### JOINT INVERSION SETTINGS ################
zWeight = 0.9 # for values < 1 more smoothing in lateral direction # 1!! works well here
maxIter = 30# maximum number of iterations
lam =     1
beta =    10000 #default beta = 10000

# Inversion constraints
poro = 0.5 # porosity
phi = poro
fr_min = 0.1
fr_max = 0.9
                     
# Archie parameters
rhow=2 # other parameters used and to try out: 3, 60, 100
a=1.
m=2. # other values: 1.4, 1.5, 3.4, 2.5, 2
n=2.4 # other values: 2.5

# Phase VELOCITIES    
vw=1500
vi=3500
va=300 # default = 300
vr=6000 # 5500

# Phase RESISTIVITIES  
rhoi=800000  #default = 1000000, best= 1000000 or 3000000
rhoa=1000000 # default =10000000, best = 10000000 or 1000000
rhor=5000 #default = 20000, best =20000

# best combos:
# 
#rhoi = 3000000, rhoa = 1000000, rhor = 30000
#rhoi = 100000, rhoa = 1000000, rhor = 20000

###################################################
# Virtual borehole
vbhdepth = -50 # -40 works well
vbh_xpos = 260

### PLOT SETTINGS ###########################
# Color scale range
cMine =    100 # min value color scale ERT 
cMaxe =    100000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    500 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.6
ylimmin = -60

fpm = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

##########################################################
# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 260, 290
yy1, yy2 = -20, -10
landform1 = 'RG'

# Second ZOI (different landform)
xx3, xx4 = 150, 180
yy3, yy4 = -30, -20
landform2 = 'SED'
                     