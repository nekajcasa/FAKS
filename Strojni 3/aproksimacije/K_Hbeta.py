# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:37:43 2020

@author: music
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Diagram 4 (stan 9 Strojni elementi 2, vrednotenje valjastih zobnikov)

#odčitane vrednosti b_cal/b
x=np.array([0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10])
#odčitana vrednost K_Hbeta
y=[4,3.4,2.9,2.55,2.3,2,1.34,1.2,1.14,1.11,1.09,1.078,1.066,1.058,1.05]

def f(x,A,B,C,D,E,F):
    return A*1/x**3+B*1/x**2+C*1/x+D+E*x+F*x**2

popt, pcov = curve_fit(f,x,y)
print(popt)

plt.plot(x,y)
t=np.linspace(0.4,10,1000)
plt.plot(t,f(t,*popt))
plt.show()