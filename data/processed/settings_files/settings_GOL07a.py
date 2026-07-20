#############################################
# to find "invlib" in the main folder
import sys, os
# path = os.popen("git rev-parse --show-toplevel").read().strip("\n")
# sys.path.insert(0, path)
#############################################

from petro import FourPhaseModel

# Inversion settings (sets error for ert (erte) and rst (rste))
erte = 0.08 # 3 % (/100)
rste = 0.002 # 0.3 ms (/1000) ; 0.001

# Mesh settings
paraDX =         0.15 #best of in conventional inversion
#paraDX =         1    #test PJI
paraDepth =      40    #Maximum depth for parametric domain, 0 (default) means 0.4 * maximum sensor range
paraMaxCellSize= 5    #best of in conventional inversion
paraMaxCellSize= 15    # Maximum cell size for parametric region in m^2
boundary=        1
paraBoundary =   1

# Parameters
#ERT
zWeighte = 0.5
lame = 10
maxItere = 15

#RST
zWeights = 0.5 #1
lams = 10
vTop = 200  # velocity at the surface of the mesh ; 300
vBottom = 10000 # velocity at the bottom of the mesh; 12000
secNodes = 2 # Amount of secondary nodes used to ensure accuracy of the forward operator
maxIters = 15

############################################################################################
# JOINT INVERSION
############################################################################################

## JOINT INVERSION SETTINGS ##
zWeight = 0.5 # for values < 1 more smoothing in lateral direction
maxIter = 10 # maximum number of iterations
lam =     10 # 30 works well or 10
beta =    10000 #default beta = 10000

# Phase velocities
va = 100   # default = 300 ; 100
vi = 3500
vw = 1500
vr = 6000 # default = 6000

# Phase resitivities
# rhow=
rhoi=10000	# 10000, 100000
rhoa=150000 	# 100000, 1000000
rhor=5000	#5000

# Archie parameter
rhow=50 #default = 100 or 60; 50
a=1.     #default = 1	; 1
m=1.8  #default = 1.4; 1.4
n=2.4   #default = 2.4 ; 1.4

# Petrophysical settings
poro = 0.3 # porosity
phi = poro
fr_min = 0.1 #0.3
fr_max = 0.9 #0.9
phi = poro
fpm_archie = FourPhaseModel(phi=poro, va=va, vi=vi, vw= vw, m=m, n=n,
                     rhow=rhow, vr=vr)

### PLOT SETTINGS ###########################
# Color scale range
cMine =    100 # min value color scale ERT 
cMaxe =    100000 # max value color scale ERT
cMape =    'turbo_r' #color map ERT
cMins =    200 # min value color scale RST 
cMaxs =    6000 # max value color scale RST
cMaps =    'viridis_r' #color map RST
cMaxp = 0.7      

# Zone of Interest (ZOI) definition
zoff = 0
xx1, xx2 = 260, 290
yy1, yy2 = -20, -10
landform1 = 'SED'            