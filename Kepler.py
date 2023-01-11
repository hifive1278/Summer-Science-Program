import math
import numpy as np
import sys

M = float(sys.argv[1])
e = float(sys.argv[2])
maxError = float(sys.argv[3])

currE = M
lastE = 0
count = 0
while abs(currE - lastE) > maxError:
    # print(currE-lastE, maxError)
    lastE = currE
    currE = M + e*math.sin(lastE)
    count += 1
    if (count > 1000000):
        print("No convergence")
        break
    
print(currE)
print(count)
