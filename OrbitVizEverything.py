# Our calculated asteroid orbit, plus actual and Earth's orbit

from vpython import vector, sphere, curve, rate, color
from math import radians, sin, cos, sqrt, pi
import numpy as np

#Orbital elements
a = 2.1 #semimajor axis
e = 0.42 #eccentricity
M = radians(339) #mean anomaly
Oprime = radians(308.53) #longitude of ascending node
iprime = radians(5.47) #inclination
wprime = radians(52) #argument of periapsis

#Find E (eccentric anomaly) from M (mean anomaly)
def solveKep(M):
    Eguess = M
    Mguess = Eguess - e*sin(Eguess)
    while abs(Mguess - M) > 1e-004:
        Mguess = Eguess - e*sin(Eguess)
        Eguess = Eguess - (M - (Eguess - e*sin(Eguess))) / (e*cos(Eguess) - 1)
    return Eguess

#Further calculations (left untouched)
sqrtmu = 0.01720209894
mu = sqrtmu**2
time = 0
dt = .05
period = sqrt(4*pi**2*a**3/mu)
Mtrue = 2*pi/period*(time) + M
Etrue = solveKep(Mtrue)

# Establish position vector and rotation matrices w, O, i
wArray = np.array([[cos(wprime), -sin(wprime), 0], [sin(wprime), cos(wprime), 0], [0,0,1]])
OArray = np.array([[cos(Oprime), -sin(Oprime), 0], [sin(Oprime), cos(Oprime), 0], [0,0,1]])
iArray = np.array([[1, 0, 0], [0, cos(iprime), -sin(iprime)], [0,sin(iprime),cos(iprime)]])
positionVector = np.array([[a*cos(Etrue)-a*e], [a*sqrt(1-e**2)*sin(Etrue)], [0]])

#Multiply matrices together with position vector
tempArr1 = np.matmul(-wArray, positionVector)
tempArr2 = np.matmul(iArray, tempArr1)
rotatedVector = -np.matmul(OArray, tempArr2)

# Vpython orbit visualization
asteroid = sphere(pos=vector(rotatedVector[0], rotatedVector[1], rotatedVector[2])*150, radius=(15), color=color.white)
asteroid.trail = curve(color=color.white)
sun = sphere(pos=vector(0,0,0), radius=(50), color=color.yellow)

#JPL Asteroid (blue)
#Orbital elements
a2 = 2.336198 #semimajor axis
e2 = 0.4565950 #eccentricity
M2 = radians(337.026434) #mean anomaly
Oprime2 = radians(309.189844) #longitude of ascending node
iprime2 = radians(5.7365679) #inclination
wprime2 = radians(49.7911405) #argument of periapsis

#Find E (eccentric anomaly) from M (mean anomaly)
def solveKep(M):
    Eguess = M
    Mguess = Eguess - e*sin(Eguess)
    while abs(Mguess - M) > 1e-004:
        Mguess = Eguess - e*sin(Eguess)
        Eguess = Eguess - (M - (Eguess - e*sin(Eguess))) / (e*cos(Eguess) - 1)
    return Eguess

#Further calculations (left untouched)
sqrtmu2 = 0.01720209894
mu2 = sqrtmu2**2
time2 = 0
dt2 = .05
period2 = sqrt(4*pi**2*a2**3/mu2)
Mtrue2 = 2*pi/period2*(time2) + M2
Etrue2 = solveKep(Mtrue2)

# Establish position vector and rotation matrices w, O, i
wArray2 = np.array([[cos(wprime2), -sin(wprime2), 0], [sin(wprime2), cos(wprime2), 0], [0,0,1]])
OArray2 = np.array([[cos(Oprime2), -sin(Oprime2), 0], [sin(Oprime2), cos(Oprime2), 0], [0,0,1]])
iArray2 = np.array([[1, 0, 0], [0, cos(iprime2), -sin(iprime2)], [0,sin(iprime2),cos(iprime2)]])
positionVector2 = np.array([[a2*cos(Etrue2)-a2*e2], [a2*sqrt(1-e2**2)*sin(Etrue2)], [0]])

#Multiply matrices together with position vector
tempArr1_2 = np.matmul(-wArray2, positionVector2)
tempArr2_2 = np.matmul(iArray2, tempArr1_2)
rotatedVector2 = -np.matmul(OArray2, tempArr2_2)

# Vpython orbit visualization
asteroid2 = sphere(pos=vector(rotatedVector2[0], rotatedVector2[1], rotatedVector2[2])*150, radius=(15), color=color.blue)
asteroid2.trail = curve(color=color.blue)

#Earth from JPL
#Orbital elements
a3 = 0.9991001461665049 #semimajor axis
e3 = 0.01754791861884277 #eccentricity
M3 = radians(198.0613857532664) #mean anomaly
Oprime3 = radians(206.4860019885501) #longitude of ascending node
iprime3 = radians(0.002357538013462295) #inclination
wprime3 = radians(257.3841310548590) #argument of periapsis


#Further calculations (left untouched)
sqrtmu3 = 0.01720209894
mu3 = sqrtmu3**2
time3 = 0
dt3 = .05
period3 = sqrt(4*pi**2*a3**3/mu3)
Mtrue3 = 2*pi/period3*(time3) + M3
Etrue3 = solveKep(Mtrue3)

# Establish position vector and rotation matrices w, O, i
wArray3 = np.array([[cos(wprime3), -sin(wprime3), 0], [sin(wprime3), cos(wprime3), 0], [0,0,1]])
OArray3 = np.array([[cos(Oprime3), -sin(Oprime3), 0], [sin(Oprime3), cos(Oprime3), 0], [0,0,1]])
iArray3 = np.array([[1, 0, 0], [0, cos(iprime3), -sin(iprime3)], [0,sin(iprime3),cos(iprime3)]])
positionVector3 = np.array([[a3*cos(Etrue3)-a3*e3], [a3*sqrt(1-e3**2)*sin(Etrue3)], [0]])

#Multiply matrices together with position vector
tempArr1_3 = np.matmul(-wArray3, positionVector3)
tempArr2_3 = np.matmul(iArray3, tempArr1_3)
rotatedVector3 = -np.matmul(OArray3, tempArr2_3)

# Vpython orbit visualization
asteroid3 = sphere(pos=vector(rotatedVector3[0], rotatedVector3[1], rotatedVector3[2])*150, radius=(15), color=color.green)
asteroid3.trail = curve(color=color.green)


#Orbit movement
while (1==1):
    if time < 10:
        print("v:", rotatedVector)
        print("v2:", rotatedVector2)
    rate(200)
    time = time + 1
    Mtrue = 2*pi/period*(time) + M
    Etrue = solveKep(Mtrue)
    
    wArray = np.array([[cos(wprime), -sin(wprime), 0], [sin(wprime), cos(wprime), 0], [0,0,1]])
    OArray = np.array([[cos(Oprime), -sin(Oprime), 0], [sin(Oprime), cos(Oprime), 0], [0,0,1]])
    iArray = np.array([[1, 0, 0], [0, cos(iprime), -sin(iprime)], [0,sin(iprime),cos(iprime)]])
    positionVector = np.array([[a*cos(Etrue)-a*e], [a*sqrt(1-e**2)*sin(Etrue)], [0]])

    tempArr1 = np.matmul(-wArray, positionVector)
    tempArr2 = np.matmul(iArray, tempArr1)
    rotatedVector = -np.matmul(OArray, tempArr2)
    asteroid.pos = vector(rotatedVector[0], rotatedVector[1], rotatedVector[2])*150
    asteroid.trail.append(pos=asteroid.pos)  

    #JPL data asteroid (blue)
    time2 = time2 + 1
    Mtrue2 = 2*pi/period2*(time2) + M2
    Etrue2 = solveKep(Mtrue2)
    
    wArray2 = np.array([[cos(wprime2), -sin(wprime2), 0], [sin(wprime2), cos(wprime2), 0], [0,0,1]])
    OArray2 = np.array([[cos(Oprime2), -sin(Oprime2), 0], [sin(Oprime2), cos(Oprime2), 0], [0,0,1]])
    iArray2 = np.array([[1, 0, 0], [0, cos(iprime2), -sin(iprime2)], [0,sin(iprime2),cos(iprime2)]])
    positionVector2 = np.array([[a2*cos(Etrue2)-a2*e2], [a2*sqrt(1-e2**2)*sin(Etrue2)], [0]])

    tempArr1_2 = np.matmul(-wArray2, positionVector2)
    tempArr2_2 = np.matmul(iArray2, tempArr1_2)
    rotatedVector2 = -np.matmul(OArray2, tempArr2_2)
    asteroid2.pos = vector(rotatedVector2[0], rotatedVector2[1], rotatedVector2[2])*150
    asteroid2.trail.append(pos=asteroid2.pos)  

    #Earth JPL
    time3 = time3 + 1
    Mtrue3 = 2*pi/period3*(time3) + M3
    Etrue3 = solveKep(Mtrue3)

    wArray3 = np.array([[cos(wprime3), -sin(wprime3), 0], [sin(wprime3), cos(wprime3), 0], [0,0,1]])
    OArray3 = np.array([[cos(Oprime3), -sin(Oprime3), 0], [sin(Oprime3), cos(Oprime3), 0], [0,0,1]])
    iArray3 = np.array([[1, 0, 0], [0, cos(iprime3), -sin(iprime3)], [0,sin(iprime3),cos(iprime3)]])
    positionVector3 = np.array([[a3*cos(Etrue3)-a3*e3], [a3*sqrt(1-e3**2)*sin(Etrue3)], [0]])

    tempArr1_3 = np.matmul(-wArray3, positionVector3)
    tempArr2_3 = np.matmul(iArray3, tempArr1_3)
    rotatedVector3 = -np.matmul(OArray3, tempArr2_3)
    asteroid3.pos = vector(rotatedVector3[0], rotatedVector3[1], rotatedVector3[2])*150
    asteroid3.trail.append(pos=asteroid3.pos) 
