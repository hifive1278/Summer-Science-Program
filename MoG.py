import math
import numpy as np
import sys
import SEL
import FandG
import MathPhysicsPset8

k = 0.0172020989484 #Gaussian gravitational constant
cAU = 173.144643267 #speed of light in au/(mean solar)day
eps = math.radians(23.4374) #Earth's obliquity
mag = np.linalg.norm

#Accept input file and extract data
textfile = sys.argv[1]
arrYears = np.loadtxt(textfile, usecols = (0))
arrMonths = np.loadtxt(textfile, usecols = (1))
arrDays = np.loadtxt(textfile, usecols = (2))
arrHours = np.loadtxt(textfile, usecols = (3), dtype = np.str0)
arrRAs = np.loadtxt(textfile, usecols = (4), dtype = np.str0)
arrDecs = np.loadtxt(textfile, usecols = (5), dtype = np.str0)
arrSunVecX = np.loadtxt(textfile, usecols = (6))
arrSunVecY = np.loadtxt(textfile, usecols = (7))
arrSunVecZ = np.loadtxt(textfile, usecols = (8))
numObservations = arrYears.size

#Convert sexagesimal inputs to decimal Julian dates
arrJulianDays = np.zeros(numObservations)

for x in range(numObservations):
    Y = arrYears[x]
    M = arrMonths[x]
    splitArr = arrHours[x].split(":")
    decimalVal = float(splitArr[0]) + float(splitArr[1])/60 + float(splitArr[2])/3600
    D = arrDays[x] + decimalVal / 24
    julian0 = 367*Y - int(7*(Y+int((M+9)/12))/4) + int(275*M/9) + D + 1721013.5
    arrJulianDays[x] = julian0

t0 = 367*2021 - int(7*(2021+int((7+9)/12))/4) + int(275*7/9) + 24 + 7/24 + 1721013.5 #Already has values for epoch, July 24 2021 7:00 UTC

#Handle inputs if more than three observations provided, and find taus
obs1 = 0
obs2 = 1
obs3 = 2
if (arrJulianDays.size > 3):
    obs1 = int(input("Input the index of your first preferred observation:"))
    obs2 = int(input("Input the index of your second preferred observation:"))
    obs3 = int(input("Input the index of your third preferred observation:"))
tau3 = k*(arrJulianDays[obs3] - arrJulianDays[obs2])
tau1 = k*(arrJulianDays[obs1] - arrJulianDays[obs2]) #A little buggy depending on the order the user inputs the three considered observations
tau = (tau3 - tau1)
taus = [tau1, tau3, tau]

#Convert sexagesimal RA to decimal
decimalValRA = np.zeros(numObservations)
for x in range(numObservations):
    splitArr = arrRAs[x].split(":")
    decimalVal = float(splitArr[0]) + float(splitArr[1])/60 + float(splitArr[2])/3600
    decimalValRA[x] = decimalVal 

#Convert sexagesimal dec to decimal
decimalValDec = np.zeros(numObservations)
for x in range(numObservations):
    splitArr = arrDecs[x].split(":")
    if (float(splitArr[0]) < 0):
        decimalVal = float(splitArr[0]) - float(splitArr[1])/60 - float(splitArr[2])/3600
    else:
        decimalVal = float(splitArr[0]) + float(splitArr[1])/60 + float(splitArr[2])/3600
    decimalValDec[x] = decimalVal 

#Convert to radians
decimalValRA *= 15
decimalValRA *= (math.pi/180)
decimalValDec *= (math.pi/180)

#Create rhohats from decimal RA/Dec
rhohat1 = [math.cos(decimalValRA[0]) * math.cos(decimalValDec[0]), math.sin(decimalValRA[0]) * math.cos(decimalValDec[0]), math.sin(decimalValDec[0])]
rhohat2 = [math.cos(decimalValRA[1]) * math.cos(decimalValDec[1]), math.sin(decimalValRA[1]) * math.cos(decimalValDec[1]), math.sin(decimalValDec[1])]
rhohat3 = [math.cos(decimalValRA[2]) * math.cos(decimalValDec[2]), math.sin(decimalValRA[2]) * math.cos(decimalValDec[2]), math.sin(decimalValDec[2])]
rhohat1 = np.array(rhohat1)
rhohat2 = np.array(rhohat2)
rhohat3 = np.array(rhohat3)

#Establish sun vector from file inputs
sun1 = [arrSunVecX[0], arrSunVecY[0], arrSunVecZ[0]]
sun1 = np.array(sun1)
sun2 = [arrSunVecX[1], arrSunVecY[1], arrSunVecZ[1]]
sun2 = np.array(sun2)
sun3 = [arrSunVecX[2], arrSunVecY[2], arrSunVecZ[2]]
sun3 = np.array(sun3)

#Calculate each D
D0 = np.dot(rhohat1, np.cross(rhohat2, rhohat3))
D11 = np.dot(np.cross(sun1, rhohat2), rhohat3)
D12 = np.dot(np.cross(sun2, rhohat2), rhohat3)
D13 = np.dot(np.cross(sun3, rhohat2), rhohat3)
D21 = np.dot(np.cross(rhohat1, sun1), rhohat3)
D22 = np.dot(np.cross(rhohat1, sun2), rhohat3)
D23 = np.dot(np.cross(rhohat1, sun3), rhohat3)
D31 = np.dot(rhohat1, np.cross(rhohat2, sun1))
D32 = np.dot(rhohat1, np.cross(rhohat2, sun2))
D33 = np.dot(rhohat1, np.cross(rhohat2, sun3))
Ds = [D0, D21, D22, D23]

#Call scalar equation of legrange
realRoots,rhos = SEL.SEL(taus,sun2,rhohat2,Ds) 

#Allows user to select which viable root/rho combination to proceed with 
r2 = 0
print("Please enter the index of your selected root between: 0 -", len(realRoots)-1)
whichRoot = input()
if (whichRoot == "0"):
    r2 = realRoots[0]
elif (whichRoot == "1"):
    r2 = realRoots[1]
elif (whichRoot == "2"):
    r2 = realRoots[2]
else:
    print("Index selection could not be identified")

#Truncated, initial values for f's and g's
flag = "function" #Can also be "third" or "fourth" depending on what you want to run to refine f and g
init_f1 = 1 - tau1**2/(2*r2**3)
init_f3 = 1 - tau3**2/(2*r2**3)
init_g1 = tau1 - tau1**3/(6*r2**3)
init_g3 = tau3 - tau3**3/(6*r2**3)

#Find d's
d1 = -init_f3/(init_f1*init_g3 - init_f3*init_g1)
d3 = init_f1/(init_f1*init_g3 - init_f3*init_g1)

#Find c's
c1 = init_g3/(init_f1*init_g3 - init_g1*init_f3)
c2 = -1
c3 = -init_g1/(init_f1*init_g3 - init_g1*init_f3)

#Find rho magnitudes
rho1 = (c1*D11 + c2*D12 + c3*D13)/(c1*D0)
rho2 = (c1*D21 + c2*D22 + c3*D23)/(c2*D0)
rho3 = (c1*D31 + c2*D32 + c3*D33)/(c3*D0)

#Find r vectors
r1 = rho1*rhohat1 - sun1
r2 = rho2*rhohat2 - sun2
r3 = rho3*rhohat3 - sun3

#Find observaition 2 velocity vector
r2dot = d1*r1 + d3*r3

#Refine f and g through iteration (if flag=="function")
f1,g1 = FandG.fg(tau1,r2,r2dot,flag)
f3,g3 = FandG.fg(tau3,r2,r2dot,flag)

#Correct for speed of light
t1 = arrJulianDays[0] - rho1/cAU
t2 = arrJulianDays[1] - rho2/cAU
t3 = arrJulianDays[2] - rho3/cAU

#Refined tau values
tau3 = k*(t3 - t2)
tau1 = k*(t1 - t2)
tau = (tau3 - tau1)
taus = [tau1, tau3, tau]

#Iterate to refine rho2 and r2 
currRho2 = rho2
lastRho2 = 0
iterations = 0
while abs(currRho2 - lastRho2) > 1e-12:
    lastRho2 = currRho2

    d1 = -f3/(f1*g3 - f3*g1)
    d3 = f1/(f1*g3 - f3*g1)

    c1 = g3/(f1*g3 - g1*f3)
    c2 = -1
    c3 = -g1/(f1*g3 - g1*f3)

    rho1 = (c1*D11 + c2*D12 + c3*D13)/(c1*D0)
    rho2 = (c1*D21 + c2*D22 + c3*D23)/(c2*D0)
    rho3 = (c1*D31 + c2*D32 + c3*D33)/(c3*D0)

    r1 = rho1*rhohat1 - sun1
    r2 = rho2*rhohat2 - sun2
    r3 = rho3*rhohat3 - sun3

    r2dot = d1*r1 + d3*r3

    f1,g1 = FandG.fg(tau1,r2,r2dot,flag)
    f3,g3 = FandG.fg(tau3,r2,r2dot,flag)

    t1 = arrJulianDays[0] - rho1/cAU
    t2 = arrJulianDays[1] - rho2/cAU
    t3 = arrJulianDays[2] - rho3/cAU

    tau3 = k*(t3 - t2)
    tau1 = k*(t1 - t2)
    tau = (tau3 - tau1)
    taus = [tau1, tau3, tau]

    currRho2 = rho2
    iterations += 1
    # print("Iterations passed:", iterations, "Change in rho2=", currRho2 - lastRho2,"Light-travel time:", rho2/cAU*24*60*60)

print("Range (rho2):", rho2, "AU")
eclipticTrans = np.array([[1,0,0], [0, math.cos(eps), math.sin(eps)], [0, -math.sin(eps), math.cos(eps)]])
eclipticR2 = np.matmul(eclipticTrans, r2)
eclipticR2dot = np.matmul(eclipticTrans, r2dot)
a,e,i,O,w,M_t0 = MathPhysicsPset8.orbitCalc(eclipticR2, eclipticR2dot, t0, t2)
print("r2 (cartesian ecliptic):", eclipticR2, " = ", mag(eclipticR2), "AU")
print("r2dot (cartesian ecliptic):", eclipticR2dot, " = ", k*mag(eclipticR2dot), "AU/day")
print("Semimajor axis (a):", a, "AU \nEccentricity (e):", e, "\nInclination (i):", i, "degrees \nLongitude of ascending node (O):", O, "degrees \nArgument of perihelion (w):", w, "degrees \nMean anomaly at epoch (M_t0):", M_t0, "degrees")
