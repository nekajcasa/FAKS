# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:06:56 2022

@author: music
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def komprimiranje(zgodovina, indeksi=[]):
    """funkcija komplimira array zgodovina, tako da ostanjelo le lokalni ekstremi"""
    i=0
    while i <= (len(zgodovina)-3):
        vzorec=zgodovina[i:i+3]
        if (vzorec[1]-vzorec[0])*(vzorec[1]-vzorec[2])>0:
            i+=1
        else:
            zgodovina=np.delete(zgodovina,[i+1])
            if len(indeksi) != 0:
                indeksi=np.delete(indeksi,[i+1])
    if len(indeksi) != 0:
        return zgodovina, indeksi
    else:
        return zgodovina

def rainflow(zgodovina,cikli=[],štetje_ostanka=True,debug=False):
    """funkcija prešteje cikle po metodi rainflow in vrne amplitude in srednje
    vrednosti ciklov [iz,v,amplituda,srednja vrednost]"""
    i=0
    
    while i<=(len(zgodovina)-4):
        vzorec=zgodovina[i:i+4]
        if (vzorec[1]>vzorec[0])and(vzorec[2]>=vzorec[0])and(vzorec[3]>=vzorec[1])or(vzorec[1]<vzorec[0])and(vzorec[2]<=vzorec[0])and(vzorec[3]<=vzorec[1]):
            if debug==True: 
                cikli.append([vzorec[1],vzorec[2],(vzorec[2]-vzorec[1])/2,(vzorec[1]+vzorec[2])/2])
            else:
                cikli.append([np.abs((vzorec[1]-vzorec[2])/2),(vzorec[1]+vzorec[2])/2])
            zgodovina = np.delete(zgodovina,[i+1,i+2])
            if i-2<0:
                i=0
            else:
                i -= 2
        else:
            i += 1
    
    #štetje ostanka
    if štetje_ostanka==True:
        zgodovina=np.append(zgodovina,zgodovina)
        zgodovina=komprimiranje(zgodovina)
        rainflow(zgodovina,cikli=cikli,štetje_ostanka=False)
        
    return np.array(cikli)

def izračun_ekvivalentnih_ciklov(amplituda, srednja_vrednost, sigma_utrip, sigma_nihaj):
    """obremenitve se pretvori v ekvivalente cikle za R=-1
    amplituda - velikost amplitude cikla
    srednja_vrednost - velikost srednje verdnosti cikla
    sigma_utrip - sigma za trajno dinamično trdnost za R=0
    sigma_nihaj - sigma za trajno dinamično trdnost za R=-1
    
    """
    
    #računanje naklona premice
    M2 = (2*sigma_nihaj)/sigma_utrip-1
    
    if amplituda+srednja_vrednost>=0:
        sigma_eq=amplituda+M2*srednja_vrednost
    else:
        sigma_eq=(1-M2)*amplituda
   
    
    return sigma_eq
    
def izračun_poškodbe(ekvivalentna_napetost,k,A,N_D,debug=False):
    """funkcija vrne vrednost poškodbe po med 0 in 1, 
    k in B sta parametra wohlwrjeve krivuje, N_D je število ciklov za trajno dinamično trdnost""" 
    
    sigma_D=10**((np.log10(N_D)-A)/-k)   #napetost trajne dinamične trdnosti
    D=0                                  #poškodba
    if debug==True:
        print(sigma_D)
    #računanje poškodbe
    for i in ekvivalentna_napetost:
        if i >= sigma_D:
            Ni=N_D*(i/sigma_D)**-k
        else:
            Ni=N_D*(i/sigma_D)**(-2*k+1)
        if debug==True:
            print(f"{i:.2f} MPa -> {Ni:.2f} ciklov")
        D += 1/Ni
    
    return D
    
#=============================RAČUNANJE_PROBLEMA===============================

if __name__=="__main__":
    #podatki iz prejšnjega sklopa
    k = 9.152         #naklon wohlerjeve krivulje v log log
    B = 25.698        #prosti člen w. krivulje
    N_D = 2e6         #število ciklov trajne dinamične trdnosti
    #strojniški priročnik stran 610
    sigma_d_utrip = 45
    sigma_d_nihaj = 30
    
    #izbira podatkov
    meritev=48
    
    #branje podatkov iz datoteke
    file = "Zgodovine_obremenitve/Zgodovina_"+str(meritev)+".txt"
    data = pd.read_csv(file,delimiter = "\t" , header = 1)
    indeksi = np.array(data["[/]"])
    napetost= np.array(data["[MPa]"])
    test_podatki=[0,-54,230,-36,86,-205,57,-197,229,-134,191,-62,0]
    
    #komprimiranje
    komprimirana_napetost,komprimirani_indeksi = komprimiranje(napetost,indeksi)
    
    
    #štetje ciklov po metodi rainflow
    cikli_D1=rainflow(komprimirana_napetost,cikli=[],štetje_ostanka=False)
    cikli_D2=rainflow(komprimirana_napetost,cikli=[],štetje_ostanka=True)

    #določanje ekvivalentnih ciklov za R=-1
    ekvivalentni_cikli_D1=[]
    ekvivalentni_cikli_D2=[]
    for i in cikli_D1:
        ekvivalentni_cikli_D1.append(izračun_ekvivalentnih_ciklov(i[0], i[1],
                                                              sigma_d_utrip,
                                                              sigma_d_nihaj))
    for i in cikli_D2:
        ekvivalentni_cikli_D2.append(izračun_ekvivalentnih_ciklov(i[0], i[1],
                                                              sigma_d_utrip,
                                                              sigma_d_nihaj))
        
    #izračun poškodbe
    D1 = izračun_poškodbe(ekvivalentni_cikli_D1, k, B, N_D)
    D2 = izračun_poškodbe(ekvivalentni_cikli_D2, k, B, N_D)
    #Izračun dobe trajanja (števila blokov obremenitev)
    doba_trajanja = 1+(1-D1)/(D2)
    print(f"Podatki: {meritev}")
    print(f"komprimiranje: {len(napetost)} => {len(komprimirana_napetost)}")
    print(f"Poškodba po enem ciklu obremenitev je {D2}.")
    print(f"Število blokov obremenitev do odpovedi {doba_trajanja}.")
    


#plotanje
plt.clf()
plt.plot(indeksi,napetost,label="Nekompremirani podatki")
plt.plot(komprimirani_indeksi,komprimirana_napetost,label="Kompremirani podatki")
plt.legend(loc="upper right")
plt.xlim(0,50)
plt.ylabel("$\sigma$ [MPa]")
plt.xlabel("Obremenitev")
plt.grid()
plt.tight_layout()
plt.show()
