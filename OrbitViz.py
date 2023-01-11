from vpython import vector, sphere, curve, rate, color
from math import radians, sin, cos, sqrt, pi
import numpy as np

#Orbital elements
a = 2.773017979589484 #semimajor axis
e = 0.1750074901308245 #eccentricity
M = radians(336.0050001501443) #mean anomaly
Oprime = radians(108.032597191534) #longitude of ascending node
iprime = radians(16.34548466739393) #inclination
wprime = radians(74.95130563682554) #argument of periapsis

#Find E (eccentric anomaly) from M (mean anomaly)
def solveKep(M):
    Eguess = M
    Mguess = Eguess - e*sin(Eguess)
    while abs(Mguess - M) > 1e-004:
        Mguess = Eguess - e*sin(Eguess)
        Eguess = Eguess - (M - (Eguess - e*sin(Eguess))) / (e*cos(Eguess) - 1)
    return Eguess

sqrtmu = 0.01720209894
mu = sqrtmu**2
time = 0
dt = .05
period = sqrt(4*pi**2*a**3/mu)
r1ecliptic = [0, 0, 0]
Mtrue = 2*pi/period*(time) + M
Etrue = solveKep(Mtrue)
r1ecliptic[0] = (cos(wprime)*cos(Oprime) - sin(wprime)*cos(iprime)*sin(Oprime))*(a*cos(Etrue)-a*e) - (cos(wprime)*cos(iprime)*sin(Oprime) + sin(wprime)*cos(Oprime))*(a*sqrt(1-e**2)*sin(Etrue))
r1ecliptic[1] = (cos(wprime)*sin(Oprime) + sin(wprime)*cos(iprime)*cos(Oprime))*(a*cos(Etrue)-a*e) + (cos(wprime)*cos(iprime)*cos(Oprime) - sin(wprime)*sin(Oprime))*(a*sqrt(1-e**2)*sin(Etrue))
r1ecliptic[2] = sin(wprime)*sin(iprime)*(a*cos(Etrue)-a*e) + cos(wprime)*sin(iprime)*(a*sqrt(1-e**2)*sin(Etrue))
asteroid = sphere(pos=vector(r1ecliptic[0], r1ecliptic[1], r1ecliptic[2])*150, radius=(15), color=color.white)
asteroid.trail = curve(color=color.white)
sun = sphere(pos=vector(0,0,0), radius=(50), color=color.yellow)

while (1==1):
    if time < 10:
        print(r1ecliptic)
    rate(200)
    time = time + 1
    Mtrue = 2*pi/period*(time) + M
    Etrue = solveKep(Mtrue)
    r1ecliptic[0] = (cos(wprime)*cos(Oprime) - sin(wprime)*cos(iprime)*sin(Oprime))*(a*cos(Etrue)-a*e) - (cos(wprime)*cos(iprime)*sin(Oprime) + sin(wprime)*cos(Oprime))*(a*sqrt(1-e**2)*sin(Etrue))
    r1ecliptic[1] = ((cos(wprime)*sin(Oprime) + sin(wprime)*cos(iprime)*cos(Oprime))*(a*cos(Etrue)-a*e)) + (cos(wprime)*cos(iprime)*cos(Oprime) - sin(wprime)*sin(Oprime))*(a*sqrt(1-e**2)*sin(Etrue))
    r1ecliptic[2] = sin(wprime)*sin(iprime)*(a*cos(Etrue)-a*e) + cos(wprime)*sin(iprime)*(a*sqrt(1-e**2)*sin(Etrue))
    asteroid.pos = vector(r1ecliptic[0], r1ecliptic[1], r1ecliptic[2])*150
    asteroid.trail.append(pos=asteroid.pos)  
