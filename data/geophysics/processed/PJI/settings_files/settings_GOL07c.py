#############################################
# to find "invlib" in the main folder
import sys, os
# path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
# sys.path.insert(0, path)
#############################################

from petro import FourPhaseModel

# Inversion settings (sets error for ert (erte) and rst (rste))
erte = 0.06 # 3 % (/100)
rste = 0.0015 # 0.3 ms (/1000)

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
zWeighte = 0.9 # 0.5
lame = 5 #1
maxItere = 50

#RST
zWeights = 0.9 # 0.2
lams =5 #25
vTop = 400 # velocity at the surface of the mesh
vBottom = 15000 # velocity at the bottom of the mesh
secNodes = 2 # Amount of secondary nodes used to ensure accuracy of the forward operator
maxIters = 10

############################################################################################
# JOINT INVERSION
############################################################################################

## JOINT INVERSION SETTINGS ##
zWeight = 0.9 # for values < 1 more smoothing in lateral direction
maxIter = 30 # maximum number of iterations
lam =     5
beta =    10000 #default beta = 10000

# Phase velocities
va = 300
vi = 3500
vw = 1500
vr = 6000 

# Phase resitivities
# rhow=100
rhoi=2000000 # 2000000, 1000000, 500000
rhoa=10000000 # 10000000, 1000000
rhor=8000 # 10000, 20000, 50000, 1000

# Archie parameter
rhow=100 #default = 100 or 60
a=1.     #default = ?
m=1.4      #default = 1.4
n=2.4     #default = 2.4

# Petrophysical settings
poro = 0.5 # porosity; 0.66
phi = poro
fr_min = 0.1
fr_max = 0.9 ; 0.6
phi = poro
fpm = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

### PLOT SETTINGS ###########################
# Color scale range
cMine =    1000 # min value color scale ERT 
cMaxe =    1000000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    500 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.7       

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 260, 290
yy1, yy2 = -20, -10
landform1 = 'RG'               