# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:41:53 2020

@author: music 
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

fig = plt.figure()
ax = fig.gca(projection='3d')
# Podatki odčitani iz diagrama 4(Stran 9 Strojni elementi 2- Vrednotenje valjastih zobnikov)
#Vrednosti F_by
x=np.array([5,10,20,30,40,50,60])
#Vrednosti Fm/b
y=np.array([100,150,200,300,400,500,750])
#vrednosti b_cal/b
z=np.array([    [1.5,2,2.5,3.5,4.5,5.5,8],\
            	[1,1.4,1.6,2,2.6,3,4.3],\
                [0.7,0.9,1.05,1.4,1.65,1.9,2.5],\
                [0.58,0.71,0.84,1.02,1.3,1.5,1.8],\
                [0.5,0.6,0.7,0.9,1.02,1.2,1.5],\
                [.45,0.55,0.65,0.8,0.9,1.02,1.3],\
                [0.4,.5,.6,.7,.83,.95,1.1]])

    
Y1, X1 = np.meshgrid(y, x)
xData=np.vstack([X1.flatten(),Y1.flatten()])
yData=z.flatten()
def f(x, A0,A1,A2,A3,B0,B1,A0B0,A1B0,A2B0,A3B0,H):
        return  A0*np.log(x[0])+A1*x[0]+A2*x[0]**2+A3*x[0]**3+\
                B0*x[1]+B1*x[1]**2+\
                A0B0*np.log(x[0])*x[1]+A1B0*x[0]*x[1]+A2B0*x[0]**2*x[1]+A3B0*x[0]**3*x[1]+H   

# =============================================================================
# def f(x, A0,A1,A2,A3,A4):
#     return A0+A1*np.log(x)+A2*x+A3*x**2+A4*x**3
# popt, pcov = curve_fit(f,x,z[:,0])
# print(popt)
# plt.clf()
# plt.plot(x,z[:,0],"red")
# Xap=np.linspace(5,60,100)
# plt.plot(Xap,f(Xap,*popt))
# =============================================================================

popt, pcov = curve_fit(f, xData, yData)
print(popt)
print(f([15,150],*popt))


#plotanje odčitanih podatkov
ax.plot_wireframe(X1, Y1, z,color="red")
#plotanje aproksimiranih podatkov
Xap=np.linspace(5,60,100)
Yap=np.linspace(100,750,100)
Xap,Yap=np.meshgrid(Xap,Yap)
Zap=f([Xap,Yap],*popt)
ax.plot_wireframe(Xap, Yap, Zap)
#dekoracija
ax.set_xlabel("$F_{by}$")
ax.set_ylabel("$F/b$")
ax.set_zlabel("$b_{cal}/b$")
