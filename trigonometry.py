# SSP 2021 Python pset 2
# NAME
# DATE

from math import asin, acos, cos, pi, sin

# a function to determine the quadrant of an angle based on its sine and cosine (in radians)
# returns the angle in the correct quadrant (in radians)
def findQuadrant(sine, cosine):
    if cosine > 0 and sine > 0: #1
        return asin(sine)

    if cosine < 0 and sine > 0: #2
        return acos(cosine)

    if cosine < 0 and sine < 0: #3
        return pi - asin(sine)

    if cosine > 0 and sine < 0: #4
        return 2*pi + asin(sine)

# a function that given the values (in decimal degrees) of 
# two sides and the included angle of a spheical triangle
# returns the values of the remaining side and two angles (in decimal degrees)
def SAS(a, B, c):
    B = B * pi / 180
    a = a * pi / 180
    c = c * pi / 180

    # B = findQuadrant(sin(B),cos(B))

    b = acos(cos(c)*cos(a) + sin(c)*sin(a)*cos(B))
    A = asin(sin(a)*sin(B)/sin(b))
    C = asin(sin(A)*sin(c)/sin(a))

    A = findQuadrant(sin(A),cos(A)) * 180 / pi
    C = findQuadrant(sin(C),cos(C)) * 180 / pi
    b = findQuadrant(sin(b),cos(b)) * 180 / pi

    return b, A, C

# DO NOT REMOVE OR MODIFY THIS CODE
s3, a1, a2 = SAS(106, 114, 42)
if abs(s3 - 117.804) > 1e-3 or abs(a1 - 83.11) > 1e-3 or abs(a2 - 43.715) > 1e-3:
    print("SAS function INCORRECT, expected (117.804, 83.11, 43.715), but got", (s3, a1, a2))
else:
    print("SAS function CORRECT")
