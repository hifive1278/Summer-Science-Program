import math
import numpy as np
import matplotlib
from astropy.io import fits
import sys

#Command line args:  python centroid.py 490 293 5 8 13

#Take input from command line; subtract one to change from pixel/image starting coordinates (1,1) to array coordinates (0,0) 
xValue = float(sys.argv[1]) - 1
yValue = float(sys.argv[2]) - 1
apertureRadius = float(sys.argv[3])
annulusIR = float(sys.argv[4])
annulusOR = float(sys.argv[5])

image = fits.getdata("centroidtest.fit")
imageArr = np.array(image)

#Prepare cropped array (representing zoomed in field of view)
leftbound = int(xValue) - int(apertureRadius) - 1
rightbound = int(xValue) + int(apertureRadius) + 1
downbound = int(yValue) - int(apertureRadius) - 1
upbound = int(yValue) + int(apertureRadius) + 1

#Using distance formula, compare all pixels' distance from estimated center (xValue,yValue) to see if center of pixel is within annulus ring 
numAnnulusPix = 0
annulusPixSum = 0
for row in range(1024):
    for column in range(1024):
        if annulusIR < math.sqrt((column - xValue)**2.0 + (row - yValue)**2.0) < annulusOR:
            #Based off middle of pixel
            annulusPixSum += imageArr[row, column]
            numAnnulusPix += 1
meanBackground = annulusPixSum / numAnnulusPix

#Create array of entirely zeros. Using distance formula, copy only pixels within the aperture that also do not become negative when meanBackground subtracted (because that made the numbers go to like 66,___)
pixAperture = np.zeros((1024,1024))
numAperturePix = 0
for row in range(1024):
    for column in range(1024):
        if math.sqrt((column - xValue)**2.0 + (row - yValue)**2.0) < apertureRadius:
            numAperturePix += 1 #Make sure number of pixels in range is same as told (69)
            if (imageArr[row,column] - meanBackground) > 0:
                pixAperture[row, column] = imageArr[row, column] - meanBackground

#Make cropped array, make a list of the sums of columns using axis=0 and sums of rows using axis=1                
pixApertureCrop = pixAperture[downbound:upbound, leftbound:rightbound].copy()
listOfColumns = pixApertureCrop.sum(axis=0)
listOfRows = pixApertureCrop.sum(axis=1)

unchangedColumnList = pixApertureCrop.sum(axis=0) #Make another two lists so that I retain these values, to be used in formula, after changing listOfColumns/Rows
unchangedRowList = pixApertureCrop.sum(axis=1)

for column in range(len(listOfColumns)):
    if (listOfColumns[column] > 0):
        listOfColumns[column] *= (column + (xValue - apertureRadius)) #Element 0 in this list is column 484 in original array (490 - 5 - 1);;; ACTUALLY, it's (489 - 5) because we subtracted one from X and Y at beginning

for row in range(len(listOfRows)):
    if (listOfRows[row] > 0): #Exclude empty rows
        listOfRows[row] *= (row + (yValue - apertureRadius)) #Element 0 in this list is row 287 in original array (293 - 5 - 1); subtract 1 because did so in lines 20-23 when establishing cropped FOV to make it larger

meanXPosition = listOfColumns.sum() / unchangedColumnList.sum()
meanYPosition = listOfRows.sum() / unchangedRowList.sum()
print("\nX coordinate:", meanXPosition, "\nY coordinate", meanYPosition)

#Find the numerator in the uncertainty formula for x-coordinate
numeratorX = 0
currTerm = 0
for i in range(len(unchangedColumnList)):
    currTerm = unchangedColumnList[i]*((i+(xValue - apertureRadius) - meanXPosition)**2) #Used to be ((i+484 - meanXPosition)**2), changed like in line 56 and 60
    numeratorX += currTerm

uncertaintyX =  math.sqrt((numeratorX)/(unchangedColumnList.sum()*(unchangedColumnList.sum() - 1)))  
print("SigmaX:", uncertaintyX)

#Find the numerator in the uncertainty formula for y-coordinate
numeratorY = 0
currTerm = 0
for i in range(len(unchangedRowList)):
    currTerm = unchangedRowList[i]*(i+(yValue - apertureRadius) - meanYPosition)**2 #Used to be ((i+287 - meanYPosition)**2), changed like in line 56 and 60
    numeratorY += currTerm
    
uncertaintyY =  math.sqrt((numeratorY)/(unchangedRowList.sum()*(unchangedRowList.sum() - 1))) 
print("SigmaY:", uncertaintyY, "\n")