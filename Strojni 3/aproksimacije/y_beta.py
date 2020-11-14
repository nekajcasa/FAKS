# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:50:03 2020

@author: music
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

fig = plt.figure()
ax = fig.gca(projection='3d')

# Podatki odčitani iz diagrama 3(Stran 8 Strojni elementi 2- Vrednotenje valjastih zobnikov)
#Vrednosti F_betax
X = np.array([5,10,20,40])
#Vrednosti sigma_Hlim
Y = np.array([400,600,800,1000,1200])
#Vrednosti y_beta
Z = np.array([[4,2.5,2,1.5,1.2],\
              [6.8,5,4,3,2.8],\
              [15,10.3,8,6.5,5.2],\
              [32,21,16,13,11]])

Y1, X1 = np.meshgrid(Y, X)
xData=np.vstack([X1.flatten(),Y1.flatten()])
yData=Z.flatten()

          
def f(x, A,B,C,D,E,F,G,H,I,J):
        '''
        Aproksimacijska funkcija
        
        
        x[0] -- se nanaša na x os v tem primeru F_betaX\n
        x[1] -- se nanaša na y os v tem primeru sigam_Hlim
        '''
        return A+B*x[0]+C*x[0]**2+D*x[0]**3\
            +E*x[0]**2*x[1]+F*x[0]*x[1]**2+G*x[0]*x[1]\
            +H*x[1]+I*x[1]**2+J*x[1]**3

popt, pcov = curve_fit(f, xData, yData)
print(popt)

#plotanje odčitanih podatkov
ax.plot_wireframe(X1, Y1, Z,color="red")
#plotanje aproksimiranih podatkov
t=(0,1,1000)
Xap=np.linspace(3,40,1000)
Yap=np.linspace(400,1200,1000)
Xap,Yap=np.meshgrid(Xap,Yap)
Zap=f([Xap,Yap],*popt)
ax.plot_wireframe(Xap, Yap, Zap)
#dekoracija
ax.set_ylabel("$\sigma_{Hlim}$")
ax.set_xlabel("$F_{bx}$")
ax.set_zlabel("$y_b$")
ax.set_zlim3d(1, 40)                     
ax.set_ylim3d(300, 1300)                    
ax.set_xlim3d(3, 40)                    

