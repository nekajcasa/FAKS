# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 12:10:22 2022

@author: music
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from scipy.fft import fft
from scipy.signal import blackman


class Spektrogram:
    
    def __init__(self,file,dt,hitrost_vzbujanja):
        """file= ime datoteke/pot do doatoteke\n
        dt = časovno okno za DFT\n
        hitrost_vzbujanja = hitrost povečevanja obratov 1/(min s)"""
        
        self.dt = dt
        self.hitrost_vzbujanja = hitrost_vzbujanja
        
        #začne brati datoteko pri vrstici 22
        self.data = pd.read_csv(file, delimiter = "\t" , header = 22)
        #Če je drugačno poimenovanje stolpcov st to spremeni tukaj
        self.t = np.array(self.data["X_Value"])
        self.signal = np.array(self.data["Voltage"])
        self.frekvenca_vzorčenja = 1/self.t[1]
        
        #delitev signala v na manjše razdelke
        self.delitev_signala()
        
        #izvajanje dft na posameznih razdelkih
        self.s,self.f=self.dft(self.container)
    


    def delitev_signala(self):
        """Funkcija razdeli signal v bin-e, na katerih se pozneje izvede FFT"""
        #število vzorcev v binu
        self.bin_n = int(self.frekvenca_vzorčenja*dt)
        število_binov = int(len(self.t)/self.bin_n)
        container = []
        for i in range(število_binov):
            container.append(self.signal[self.bin_n*i:self.bin_n*(i+1)])
        self.container = np.array(container)
        self.bin_t = self.t[0:self.bin_n]
        
    def dft(self, signal):
        """DFT s pomočjo FFT, narejen na signalu"""
        
        y = signal*blackman(self.bin_n)#np.hamming(self.bin_n)
        
        s = np.abs(fft(y))
        #vzame se polovico (simetričen okoli 0) in se podvoji vrednost
        s_plot = 2*s[:,:int(self.bin_n/2)] / (self.bin_n / 2)
        f_plot = np.linspace(0, int(self.frekvenca_vzorčenja / 2), int(self.bin_n/2))
        
        return s_plot,f_plot
    
    def plot_spektrogram(self):
        """funkcija plota spektrogram"""
        
        #y limita
        lim = 400
        y_lim=int(lim*self.dt)
        plt.close()
        fig, ax = plt.subplots()
        x = np.linspace(60,
                        1800,
                        np.shape(self.s)[0])
        y = self.f[:y_lim]
        X,Y = np.meshgrid(x,y)
        Z = self.s.T[:y_lim,:]
        pcm = ax.pcolor(X, Y, Z,
                       norm=colors.LogNorm(vmin=Z.min()*500, vmax=Z.max()),
                       cmap='viridis', shading='auto')
        cbar = fig.colorbar(pcm, ax=ax, extend='max')
        cbar.set_label("amplituda [V]")
        ax.set_xlabel("Frekvenca motorja[1/min]")
        ax.set_ylabel("Frekvenca [Hz]")

        plt.show()
        
   
#=============================================================================    

if __name__ == '__main__':
    
    file = 'signal_kontinuiran.txt'     #ime datoteke
    dt = 1                              #velikost časovnega okna v s
    v = 2                               #povečevanje obratov motorja (1/min)/s 
    S1 = Spektrogram(file,dt,v)
    S1.plot_spektrogram()

