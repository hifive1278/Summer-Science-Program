import ephem
from sympy import Symbol, Derivative #Ended up not being used
import numpy as np
from MoG import *
import math
from MathPhysicsPset8 import orbitCalc

delta = 10**(-4)

# obs = ephem.Observer()
# obs.lon = '329:49:51.60'
# obs.lat = '289:11:37.32'
# obs.elev = 2207.
# obs.date = '2021/07/24 07:00:00' #Is this the right time??

# line = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M_t0) + ',' + '07/01.00/2021, 2000.0,,,'

# asteroid = ephem.readdb(line)
# asteroid.compute(obs)
# print(asteroid.a_ra, asteroid.a_dec)

# eclipticR2[0] += eclipticR2[0]*delta
# a,e,i,O,w,M_t0 = orbitCalc(eclipticR2, eclipticR2dot, t0, t2)
# line = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M_t0) + ',' + '07/01.00/2021, 2000.0,,,'
# asteroidPlus = ephem.readdb(line)
# asteroidPlus.compute(obs)
# (asteroidPlus.a_ra - asteroidMinus.a_ra)/(2*delta)

# for k in range(numObservations):
#     exec(f'obs{k} = np.zeros(6)')

obs1RA = np.zeros(6)
obs2RA = np.zeros(6)
obs3RA = np.zeros(6)
obs4RA = np.zeros(6)
obs5RA = np.zeros(6)

obs = ephem.Observer()
obs.lon = '329:49:51.60'
obs.lat = '289:11:37.32'
obs.elev = 2207.

a,e,i,O,w,M_t0 = orbitCalc(eclipticR2, eclipticR2dot, t0, t2)
line0 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'        
asteroidPos = ephem.readdb(line0)
asteroidPos.compute(obs)

sumDeltaSqr1 = 0
initRMS_RA = 0
for x in range(numObservations):
    sumDeltaSqr1 += (decimalValRA[x] - asteroidPos.a_ra * math.pi / 12)**2

initRMS_RA = math.sqrt(sumDeltaSqr1) / (numObservations*2 - 6)
print("initRMS for RA:", initRMS_RA)

sumDeltaSqr2 = 0
initRMS_Dec = 0
for x in range(numObservations):
    sumDeltaSqr2 += (decimalValDec[x] - np.radians(asteroidPos.a_dec))**2

initRMS_Dec = math.sqrt(sumDeltaSqr2) / (numObservations*2 - 6)
print("initRMS for Dec:", initRMS_Dec)

for x in range(numObservations):

    obs.date = str(arrYears[x]) + '/' + str(arrMonths[x]) + '/' + str(arrDays[x]) + " " + str(arrHours[x])

    for y in range(6):

        posAdjustedR2 = eclipticR2.copy()
        negAdjustedR2 = eclipticR2.copy()
        posAdjustedR2dot = eclipticR2dot.copy()
        negAdjustedR2dot = eclipticR2dot.copy()
        
        if (y < 3):
            posAdjustedR2[y] = eclipticR2[y] + eclipticR2[y]*delta
            negAdjustedR2[y] = eclipticR2[y] - eclipticR2[y]*delta

        else:
            posAdjustedR2dot[y-3] = eclipticR2dot[y-3] + eclipticR2dot[y-3]*delta
            negAdjustedR2dot[y-3] = eclipticR2dot[y-3] - eclipticR2dot[y-3]*delta

        # print("\nposAdjustedR2:", posAdjustedR2)
        # print("posAdjustedR2dot:", posAdjustedR2dot)
        # print("t0:", t0)
        # print("arrJulianDays[x]:", arrJulianDays[x])

        a,e,i,O,w,M_t0 = orbitCalc(posAdjustedR2, posAdjustedR2dot, t0, arrJulianDays[x])
        line1 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'        
        asteroidPos = ephem.readdb(line1)
        asteroidPos.compute(obs)

        a,e,i,O,w,M_t0 = orbitCalc(negAdjustedR2, negAdjustedR2dot, t0, arrJulianDays[x])
        line2 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'
        asteroidNeg = ephem.readdb(line2)
        asteroidNeg.compute(obs)
    
        if (x==1) and (y<3):
            obs1RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2[y]*delta)
        elif (x==2) and (y<3):
            obs2RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2[y]*delta)
        elif (x==3) and (y<3):
            obs3RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2[y]*delta)
        elif (x==4) and (y<3):
            obs4RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2[y]*delta)
        elif (x==5) and (y<3):
            obs5RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2[y]*delta)
        elif (x==1) and (y>=3):
            obs1RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2dot[y-3]*delta)
        elif (x==2) and (y>=3):
            obs2RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2dot[y-3]*delta)
        elif (x==3) and (y>=3):
            obs3RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2dot[y-3]*delta)
        elif (x==4) and (y>=3):
            obs4RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2dot[y-3]*delta)
        elif (x==5) and (y>=3):
            obs5RA[y] = (asteroidPos.a_ra - asteroidNeg.a_ra)/(2*eclipticR2dot[y-3]*delta)

obs1Dec = np.zeros(6)
obs2Dec = np.zeros(6)
obs3Dec = np.zeros(6)
obs4Dec = np.zeros(6)
obs5Dec = np.zeros(6)

for x in range(numObservations):

    obs = ephem.Observer()
    obs.lon = '329:49:51.60'
    obs.lat = '289:11:37.32'
    obs.elev = 2207.
    obs.date = str(arrYears[x]) + '/' + str(arrMonths[x]) + '/' + str(arrDays[x]) + " " + str(arrHours[x])

    for y in range(6):

        posAdjustedR2 = eclipticR2.copy()
        negAdjustedR2 = eclipticR2.copy()
        posAdjustedR2dot = eclipticR2dot.copy()
        negAdjustedR2dot = eclipticR2dot.copy()

        if (y < 3):
            posAdjustedR2[y] = eclipticR2[y] + eclipticR2[y]*delta
            negAdjustedR2[y] = eclipticR2[y] - eclipticR2[y]*delta

        else:
            posAdjustedR2dot[y-3] = eclipticR2dot[y-3] + eclipticR2dot[y-3]*delta
            negAdjustedR2dot[y-3] = eclipticR2dot[y-3] - eclipticR2dot[y-3]*delta

        a,e,i,O,w,M_t0 = orbitCalc(posAdjustedR2, posAdjustedR2dot, t0, arrJulianDays[x])
        line1 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'
        asteroidPos = ephem.readdb(line1)
        asteroidPos.compute(obs)

        a,e,i,O,w,M_t0 = orbitCalc(negAdjustedR2, negAdjustedR2dot, t0, arrJulianDays[x])
        line2 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'
        asteroidNeg = ephem.readdb(line2)
        asteroidNeg.compute(obs)
        
        if (x==1) and (y<3):
            obs1Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2[y]*delta)
        elif (x==2) and (y<3):
            obs2Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2[y]*delta)
        elif (x==3) and (y<3):
            obs3Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2[y]*delta)
        elif (x==4) and (y<3):
            obs4Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2[y]*delta)
        elif (x==5) and (y<3):
            obs5Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2[y]*delta)
        elif (x==1) and (y>=3):
            obs1Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2dot[y-3]*delta)
        elif (x==2) and (y>=3):
            obs2Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2dot[y-3]*delta)
        elif (x==3) and (y>=3):
            obs3Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2dot[y-3]*delta)
        elif (x==4) and (y>=3):
            obs4Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2dot[y-3]*delta)
        elif (x==5) and (y>=3):
            obs5Dec[y] = (asteroidPos.a_dec - asteroidNeg.a_dec)/(2*eclipticR2dot[y-3]*delta)

obs1RA *= 15
obs1RA = np.radians(obs1RA)
obs2RA *= 15
obs2RA = np.radians(obs2RA)
obs3RA *= 15
obs3RA = np.radians(obs3RA)
obs1Dec = np.radians(obs1Dec)
obs2Dec = np.radians(obs2Dec)
obs3Dec = np.radians(obs3Dec)

print("\nObs1RA:", obs1RA)
print("Obs2RA:", obs2RA)
print("Obs3RA:", obs3RA)
print("Obs1Dec:", obs1Dec)
print("Obs2Dec:", obs2Dec)
print("Obs3Dec:", obs3Dec)

arrJ = np.zeros((6,6))        
for x in range(6):
    if (x==0):
        for y in range(6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum

    elif (x==1):
        for y in range(1,6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum

    elif (x==2):
        for y in range(2,6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum
            
    elif (x==3):
        for y in range(3,6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum

    elif (x==4):
        for y in range(4,6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum

    elif(x==5):
        for y in range(5,6):
            sum = 0
            for z in range(1, numObservations + 1):
                if (z==1):
                    sum += obs1RA[x] * obs1RA[y]
                    sum += obs1Dec[x] * obs1Dec[y]
                elif (z==2):
                    sum += obs2RA[x] * obs2RA[y]
                    sum += obs2Dec[x] * obs2Dec[y]
                elif (z==3):
                    sum += obs3RA[x] * obs3RA[y]
                    sum += obs3Dec[x] * obs3Dec[y]
                elif (z==4):
                    sum += obs4RA[x] * obs4RA[y]
                    sum += obs4Dec[x] * obs4Dec[y]
                elif (z==5):
                    sum += obs5RA[x] * obs5RA[y]
                    sum += obs5Dec[x] * obs5Dec[y]
            arrJ[x][y] = sum
            arrJ[y][x] = sum

print("\n", arrJ)

a,e,i,O,w,M_t0 = orbitCalc(eclipticR2, eclipticR2dot, t0, t2)
line1 = '2000YJ66,e,' + str(i) + ',' + str(O) + ',' + str(w) + ',' + str(a) + ',,' + str(e) + ',' + str(M) + ',' + '07/24.29/2021, 2000.0,,,'        
asteroidPos = ephem.readdb(line1)
asteroidPos.compute(obs)
sumDelta = 0
for x in range(numObservations):
    sumDelta += (decimalValDec[x] - np.radians(asteroidPos.a_dec))
    print("sumDelta:", sumDelta)
    sumDelta += (decimalValRA[x] - asteroidPos.a_ra * math.pi / 12)
    print("sumDelta:", sumDelta)


aArr = np.zeros((6,1))
for x in range(6):
    sum = 0
    for z in range(1, numObservations + 1):
        if (z==1):
            sum += obs1RA[x] + obs1Dec[x]
        elif (z==2):
            sum += obs2RA[x] + obs2Dec[x]
        elif (z==3):
            sum += obs3RA[x] + obs3Dec[x]
        elif (z==4):
            sum += obs4RA[x] + obs4Dec[x]
        elif (z==5):
            sum += obs5RA[x] + obs5Dec[x]
    aArr[x,0] = sum * sumDelta

invJArr = np.linalg.inv(arrJ)
xArr = np.matmul(invJArr, aArr)

print(xArr)

sumDeltaSqr = 0
for x in range(numObservations):
    sumDeltaSqr += (decimalValRA[x] - asteroidPos.a_ra * math.pi / 12)**2

finalRMS = math.sqrt(sumDeltaSqr) / (numObservations*2 - 6)
print("finalRMS for RA:", finalRMS)

sumDeltaSqr = 0
for x in range(numObservations):
    sumDeltaSqr += (decimalValDec[x] - np.radians(asteroidPos.a_dec))**2

finalRMS = math.sqrt(sumDeltaSqr) / (numObservations*2 - 6)
print("finalRMS for Dec:", finalRMS)
