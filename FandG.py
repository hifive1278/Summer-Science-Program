import numpy as np
import math

#They all ran correct for test case 1, 2, 3
#tau1, tau3 = gaussian time intervals
#r2 = position vector for 2nd observation 
#r2dot = velocity vector for 2nd observation 

flag = "fourth"

def fg(tau,r2,r2dot,flag): 
    Ecurr = 0
    ELast = 0
    if (flag=="third"): #Use Taylor series approximation to third degree
        f = 1 - 1/(2*np.linalg.norm(r2)**3) * tau**2 + (np.dot(r2, r2dot))/(2*np.linalg.norm(r2)**5) * tau**3
        g = tau - 1/(6*np.linalg.norm(r2)**3) * tau**3
    
    elif (flag=="fourth"): #Use Taylor series approximation to fourth degree
        u = 1/np.linalg.norm(r2)**3
        z = np.dot(r2, r2dot) / np.linalg.norm(r2)**2
        q = np.dot(r2dot, r2dot) / np.linalg.norm(r2)**2 - u
        
        f = 1 - 1/(2*np.linalg.norm(r2)**3) * tau**2 + (np.dot(r2, r2dot))/(2*np.linalg.norm(r2)**5) * tau**3 + (3*u*q - 15*u*z**2 + u**2)*tau**4 / 24
        g = tau - 1/6 * u * tau**3 + (u*z*tau**4)/4

    elif(flag=="function"): #Iterate to refine delta E
        a = (2/np.linalg.norm(r2) - np.dot(r2dot, r2dot))**(-1)
        n = math.sqrt(1/a**3)
        Ecurr = n*tau
        
        while abs(Ecurr - ELast) > 1.e-12:
            ELast = Ecurr
            f = ELast - (1-np.linalg.norm(r2)/a)*math.sin(ELast) + np.dot(r2, r2dot)/(n*a**2) * (1-math.cos(ELast)) - n*tau
            fprime = 1 - (1-np.linalg.norm(r2)/a)*math.cos(ELast) + np.dot(r2, r2dot)/(n*a**2) * math.sin(ELast)
            Ecurr = ELast - f/fprime

        #Calculate refined values of f and g
        f = 1 - a/np.linalg.norm(r2) * (1-math.cos(Ecurr))
        g = tau + (1/n) * (math.sin(Ecurr) - Ecurr)
                
    else:
        print("Flag not recognized.")

    return(f,g)