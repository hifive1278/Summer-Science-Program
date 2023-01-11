import numpy as np
import numpy.polynomial.polynomial as poly

def SEL(tau,sun2,rhohat2,Ds): 
    realRoots = [] #for up to three real, positive roots
    rhos = [] #range values for each real, positive root  

    #Find A, B, E, F values from A1, A3, B1, B3
    A1 = tau[1] / tau[2]
    A3 = -tau[0] / tau[2]
    B1 = A1/6 * (tau[2]**2 - tau[1]**2)
    B3 = A3/6 * (tau[2]**2 - tau[0]**2)
    
    A = (A1*Ds[1] - Ds[2] + A3*Ds[3]) / -Ds[0]
    B = (B1*Ds[1] + B3*Ds[3]) / -Ds[0]
    E = -2*(np.dot(rhohat2, sun2))
    F = np.linalg.norm(sun2)**2

    #Find coefficients for polynomial
    a = -(A**2 + A*E + F)
    b = -(2*A*B + B*E)
    c = -B**2

    #Establish polynomial, find roots, and cycle through to identify real, positive ones
    polynomialArr = [c, 0, 0, b, 0, 0, a, 0, 1]
    rootArr = poly.polyroots(polynomialArr)
    count = 0
    for x in range(len(rootArr)):
        if np.isreal(rootArr[x]) and np.real(rootArr[x]) > 0:
            realRoots.append(rootArr[x])
            count += 1

    #For each real root find the corresponding rho
    for x in range(len(realRoots)):
        rhos.append(A + B/realRoots[x]**3)

    #Check root and rho pairs to ensure BOTH are positive and real
    finalRoots = []
    finalRhos = []
    for x in range(len(rhos)):
        if np.real(rhos[x]) > 0:
            finalRoots.append(np.real(realRoots[x]))
            finalRhos.append(np.real(rhos[x]))

    return(finalRoots,finalRhos) 
