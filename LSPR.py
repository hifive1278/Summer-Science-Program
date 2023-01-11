import math
import numpy as np
import sys

# Test Case 1: python LSPR.py 484.35 382.62 LSPRtestinput1.txt
# Test Case 2: python LSPR.py 1403.6 1585.9 LSPRtestinput2.txt

#Inputs
xValue = float(sys.argv[1])
yValue = float(sys.argv[2])
textfile = sys.argv[3]
refStarX = np.loadtxt(textfile, usecols = (0))
refStarY = np.loadtxt(textfile, usecols = (1))
refStarRA = np.loadtxt(textfile, usecols = (2), dtype = np.str0)
refStarDec = np.loadtxt(textfile, usecols = (3), dtype = np.str0)

#Establish necessary arrays and sum values
xValueSum = np.sum(refStarX)
yValueSum = np.sum(refStarY)
xyArr = refStarX*refStarY
xySum = np.sum(xyArr)
xSqrArr = refStarX*refStarX
xSqrSum = np.sum(xSqrArr)
ySqrArr = refStarY*refStarY
ySqrSum = np.sum(ySqrArr)
numRefStars = refStarX.size

matA = np.array([[numRefStars, xValueSum, yValueSum], [xValueSum, xSqrSum, xySum], [yValueSum, xySum, ySqrSum]])
invMatA = np.linalg.inv(matA)

#Extract decimal value for right ascension
decimalValRA = np.zeros(refStarX.size)
for x in range(refStarRA.size):
    splitArr = refStarRA[x].split(":")
    decimalVal = float(splitArr[0]) + float(splitArr[1])/60 + float(splitArr[2])/3600
    decimalValRA[x] = decimalVal 

#Extract decimal value for declination
decimalValDec = np.zeros(refStarX.size)
for x in range(refStarDec.size):
    temp = refStarDec[x]
    splitArr = temp[1:].split(":")
    decimalVal = float(splitArr[0]) + float(splitArr[1])/60 + float(splitArr[2])/3600
    decimalValDec[x] = decimalVal
      
decimalValRA *= 15 #Convert to degrees from hours

#Ensure all dec values are positive 
#[THIS HAS NOT BEEN TESETED YET, AND EFFECTS ON CURRENT CODE ARE UNKNOWN]
for x in range(decimalValDec.size):
    if decimalValDec[x] < 0:
        while decimalValDec[x] < 0:
            decimalValDec[x] += 360

#Establish necessary arrays and sum values
RA_Sum = np.sum(decimalValRA)
Dec_Sum = np.sum(decimalValDec)
xRA_Arr = decimalValRA*refStarX
xRA_Sum = np.sum(xRA_Arr)
xDec_Arr = decimalValDec*refStarX
xDec_Sum = np.sum(xDec_Arr)
yRA_Arr = decimalValRA*refStarY
yRA_Sum = np.sum(yRA_Arr)
yDec_Arr = decimalValDec*refStarY
yDec_Sum = np.sum(yDec_Arr)

fullRA_Arr = np.array([[RA_Sum], [xRA_Sum], [yRA_Sum]])
fullDec_Arr = np.array([[Dec_Sum], [xDec_Sum], [yDec_Sum]])

b1_a11_a12 = np.matmul(invMatA, fullRA_Arr)
b2_a21_a22 = np.matmul(invMatA, fullDec_Arr)

print("\nb1:", b1_a11_a12[0], "deg")
print("b2:", b2_a21_a22[0], "deg")
print("a11:", b1_a11_a12[1], "deg/pix")
print("a12:", b1_a11_a12[2], "deg/pix")
print("a21:", b2_a21_a22[1], "deg/pix")
print("a22:", b2_a21_a22[2], "deg/pix\n")

#Begin finding uncertainty for RA
uncertaintyRA_Arr = np.zeros(refStarX.size)
for x in range(refStarRA.size):
    uncertaintyRA_Arr[x] = (decimalValRA[x] - b1_a11_a12[0] - b1_a11_a12[1]*refStarX[x] - b1_a11_a12[2]*refStarY[x])**2

uncertaintyRA_Sum = np.sum(uncertaintyRA_Arr)
uncertaintyRA = math.sqrt(uncertaintyRA_Sum / (refStarX.size - 3))
print(round(uncertaintyRA * 3600, 2), "arcsec")

#Begin finding uncertainty for Dec
uncertaintyDec_Arr = np.zeros(refStarX.size)
for x in range(refStarDec.size):
    uncertaintyDec_Arr[x] = (decimalValDec[x] - b2_a21_a22[0] - b2_a21_a22[1]*refStarX[x] - b2_a21_a22[2]*refStarY[x])**2

uncertaintyDec_Sum = np.sum(uncertaintyDec_Arr)
uncertaintyDec = math.sqrt(uncertaintyDec_Sum / (refStarX.size - 3))
print(round(uncertaintyDec * 3600, 2), "arcsec\n")

#Finding final RA
finalRA = float(b1_a11_a12[0] + b1_a11_a12[1]*xValue + b1_a11_a12[2]*yValue)
finalRA /= 15

#Converting to appropriate format
RAhour = int(finalRA)
RAminute = int(((finalRA - int(finalRA)) * 60))
RAsecond = (((finalRA - int(finalRA)) * 60) - int(((finalRA - int(finalRA)) * 60))) * 60
RAsecond = round(RAsecond, 2)

#Final dec and formatting
finalDec = float(b2_a21_a22[0] + b2_a21_a22[1]*xValue + b2_a21_a22[2]*yValue)
decDeg = int(finalDec)
decArcMin = int(((finalDec - int(finalDec)) * 60))
decArcSec = (((finalDec - int(finalDec)) * 60) - int(((finalDec - int(finalDec)) * 60))) * 60
decArcSec = round(decArcSec, 1)

print(RAhour, ":", RAminute, ":", RAsecond)
if (finalDec) > 0:
    print("+", decDeg, ":", decArcMin, ":", decArcSec)
elif (finalDec) < 0:
    print("-", decDeg, ":", decArcMin, ":", decArcSec)
