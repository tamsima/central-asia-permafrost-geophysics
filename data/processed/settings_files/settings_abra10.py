#############################################
# to find "invlib" in the main folder
import sys, os
# path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
# sys.path.insert(0, path)
#############################################

from petro import FourPhaseModel

# Inversion settings (sets error for ert (erte) and rst (rste))
erte = 0.08 # 3 % (/100), 0.008
rste = 0.0006 # 0.3 ms (/1000), 0.0004

# Mesh settings
paraDX =         0.15 #best of in conventional inversion
paraDX =         1    #test PJI
paraDepth =      40    #Maximum depth for parametric domain, 0 (default) means 0.4 * maximum sensor range
paraMaxCellSize= 5    #best of in conventional inversion
paraMaxCellSize= 15    # Maximum cell size for parametric region in m^2
boundary=        1
paraBoundary =   1

# Parameters
#ERT
zWeighte = 0.1 #0.5
lame = 5 #1
maxItere = 50

#RST
zWeights = 0.1 #0.7
lams = 5
vTop = 350 # velocity at the surface of the mesh
vBottom = 15000 # velocity at the bottom of the mesh
secNodes = 2 # Amount of secondary nodes used to ensure accuracy of the forward operator
maxIters = 10

#######################################################
# JOINT INVERSION
#######################################################

## JOINT INVERSION SETTINGS ##
zWeight = 0.1 # for values < 1 more smoothing in lateral direction, 0.4 is good
maxIter = 30 # maximum number of iterations
lam =     5 # 1
beta =    10000 #default beta = 10000

# Phase velocities
va = 300
vi = 3500
vw = 1500
vr = 6000 

# Phase resitivities
rhoi=80000
rhoa=1000000
rhor=10000

# best
# rhoi = 80000/100000, rhoa = 1000000, rhor = 10000, 15000, rhow = 10,100

# Archie parameter
rhow=10  #default = 100 or 60
a=1.     #default = ?
m=1.4      #default = 1.4
n=2.4     #default = 2.4


# Petrophysical settings
poro = 0.3 # porosity
phi = poro
fr_min = 0.1
fr_max = 0.9
phi = poro
fpm = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,rhow=rhow, vr=vr)

###################################################
# Virtual borehole
vbhdepth = -50 # -40 works well
vbh_xpos = 60

### PLOT SETTINGS ###########################
# Color scale range
cMine =    1000 # min value color scale ERT 
cMaxe =    100000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    500 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.6
ylimmin = None

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 60, 90
yy1, yy2 = -25, -20
landform1 = 'MO'                     