# -*- coding: utf-8 -*-
"""
Created on Fri May 28 19:33:04 2021

@author: music


ipor projekt pot serviserja
"""

import numpy as np


def minnonzero(lista):
    """funkcija vrne indeks minimalnega neničelnega elementa"""
    kazalo = np.transpose(np.nonzero(lista))
    indeks = kazalo[np.argmin(lista[np.nonzero(lista)])]

    return int(indeks[0])


def Prim(A, začetna_točka):
    """Funkcija vrne minimalno vpeto dervo za dani graf, po Primovem algoritmu,
    v funkcijo se poda matriko povezav """

    velikost = len(A)
    A = np.delete(A, začetna_točka, 0)
    porabljene = [začetna_točka]
    ostaja = np.arange(0, velikost, 1)
    ostaja = np.delete(ostaja, začetna_točka)
    drevo = []

    for i in range(velikost - 1):

        # stolpec v katerem se išče najkrajšo povezavo
        stolpci = A[:, porabljene]
        # poišče se vese povezave - vse ne neičelne člene
        povezave = np.nonzero(stolpci)
        kazalo = np.transpose(np.nonzero(stolpci))
        indeks = kazalo[np.argmin(stolpci[povezave])]
        vrstica_nakrajše = ostaja[indeks[0]]
        drevo.append([porabljene[indeks[1]], vrstica_nakrajše])
        porabljene = np.append(porabljene, vrstica_nakrajše)
        porabljene = np.sort(porabljene)
        ostaja = np.delete(ostaja, indeks[0])
        začetna_točka = vrstica_nakrajše
        A = np.delete(A, indeks[0], 0)

    return drevo


def razdalja(A, začetek, konec):
    """Funkcija vrne [min razdaljo, zemljevid razdalje] med točkama (začetek, konec), v grafu A"""

    # tvorjenje bfs drevesa
    velikost = np.shape(A)[1]
    BFS = [[začetek]]
    porabljeno = np.array([začetek])
    while len(porabljeno) < velikost:
        nivo = []
        for i in BFS[-1]:
            pogled = np.nonzero(A[i])[0]
            pn = np.setdiff1d(pogled, porabljeno)
            porabljeno = np.append(porabljeno, pn)
            if len(pn) > 0:
                nivo.append(pn)
        nnivo = []
        for prvi in nivo:
            for drugi in prvi:
                nnivo.append(drugi)

        BFS.append(nnivo)
    BFShist = []
    for i in BFS:
        for j in i:
            BFShist.append(j)
    # iskanje minimalne poti
    začetek = BFS[0][0]

    matrika_reševanja = np.zeros([velikost, velikost])
    delo = 1
    pot = [začetek]

    # priprava prvih vrstic matrike reševanja
    matrika_reševanja[0, ] += A[začetek, ]
    del BFS[0]
    for i in range(len(BFS[0])):
        matrika_reševanja[i + 1, BFS[0][i]] += matrika_reševanja[0, BFS[0][i]]

    # iskanje povezav
    for i in range(len(BFS[0])):
        dodatek = []
        for j in A[BFS[0][i], ]:
            pot = 0
            if j > 0:
                pot = j + matrika_reševanja[0, BFS[0][i]]
            dodatek.append(pot)
        matrika_reševanja[i + 1, ] += dodatek
    delo += len(BFS[0])
    del BFS[0]

    # splošno naprej
    while len(BFS) > 0:
        for i in range(len(BFS[0])):
            povezave = np.nonzero(matrika_reševanja[0:delo, BFS[0][i]])
            kazalo = np.transpose(np.nonzero(matrika_reševanja[0:delo, BFS[0][i]]))
            indeks = kazalo[np.argmin(matrika_reševanja[0:delo, BFS[0][i]][povezave])]
            matrika_reševanja[delo + i, BFS[0][i]] += matrika_reševanja[indeks[0], BFS[0][i]]
            dodatek = []
            for j in A[BFS[0][i], ]:
                pot = 0
                if j > 0:
                    pot = j + matrika_reševanja[delo + i, BFS[0][i]]
                dodatek.append(pot)
            matrika_reševanja[i + delo, ] += dodatek
        delo += len(BFS[0])
        del BFS[0]
    # konstrukcija minimalne poti
    zemljevid = [konec]
    pozicija = konec
    indeks_BFS = np.where(np.array(BFShist) == konec)[0][0]

    # iskanje minimuma vrstice (ne ničelnega)
    vrstica = matrika_reševanja[indeks_BFS, ]
    dolžina_min_poti = matrika_reševanja[indeks_BFS, minnonzero(vrstica)]

    while pozicija != začetek:
        # iskanje minimuma stolpca nad to vrstico
        kandidati = matrika_reševanja[:, pozicija]
        pozicija = BFShist[minnonzero(kandidati)]
        # tvorjenje poti
        zemljevid.insert(0, pozicija)

    return dolžina_min_poti, zemljevid


def DvA(A, drevo):
    """funkcija naredi matriko povezav na podliagi drevesa"""

    Adrevesa = np.zeros([len(A), len(A)])
    for i in drevo:
        Adrevesa[i[0], i[1]] += A[i[0], i[1]]

    return Adrevesa + np.transpose(Adrevesa)



def TSP(A, začetek):
    """funkcija vrne rešitev TSP, in vrednost poti za dani graf A"""


    pozicija = začetek
    pot = [začetek]
    obiskani = [začetek]
    neobiskani = np.arange(0, len(A), 1)
    neobiskani = np.setdiff1d(neobiskani, obiskani)

    drevo = Prim(A, začetek)
    Adrev = DvA(A, drevo)
    Adrev[:, pozicija] = np.zeros(len(A))

    while len(neobiskani) > 0:
        # for steve in range(2):
        while np.sum(Adrev[pozicija, ]) > 0:
            vrstica = Adrev[pozicija, ]
            pozicija = minnonzero(vrstica)
            Adrev[:, pozicija] = np.zeros(len(A))
            obiskani.append(pozicija)
            neobiskani = np.setdiff1d(neobiskani, obiskani)
            pot.append(pozicija)

        if len(neobiskani) > 0:
            # iskanje najkrajše poti med neobiskanimi točkami (izven drevesa)
            start_iskanja = pot[-1]
            dolžine = []
            zemljevidi = []
            for i in neobiskani:
                steza = razdalja(A, start_iskanja, i)
                dolžine.append(steza[0])
                zemljevidi.append(steza[1])
            pot = pot + zemljevidi[np.argmin(dolžine)][1:]
            neobiskani = np.setdiff1d(neobiskani, pot)
            pozicija = pot[-1]
            Adrev[:, pozicija] = np.zeros(len(A))

    # iskanje najkrajše poti domov
    domov = razdalja(A, pot[-1], pot[0])
    pot = pot + domov[1][1:]
    dolžina_poti = 0
    for i in range(len(pot) - 1):
        dolžina_poti += A[pot[i], pot[i + 1]]
    return pot, dolžina_poti


# Matrike grafov
G2 = np.array([[0, 3, 0, 0, 0, 1, 4],
              [3, 0, 1, 0, 0, 1, 1],
              [0, 1, 0, 3, 0, 0, 0],
              [0, 0, 3, 0, 1, 1, 0],
              [0, 0, 0, 1, 0, 2, 0],
              [1, 1, 0, 1, 2, 0, 3],
              [4, 1, 0, 0, 0, 3, 0]])

G3 = np.array([[0,1,1,0,0,1,0,0,0,2],
               [1,0,2,0,0,0,0,0,4,0],
               [1,2,0,3,0,0,0,0,0,0],
               [0,0,3,0,5,0,0,0,0,0],
               [0,0,0,5,0,1,0,0,0,0],
               [1,0,0,0,1,0,5,0,0,0],
               [0,0,0,0,0,5,0,1,0,0],
               [0,0,0,0,0,0,1,0,1,2],
               [0,4,0,0,0,0,0,1,0,0],
               [2,0,0,0,0,0,0,2,0,0]])

G4 = np.array([[0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0],
               [6,0,1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,2,0,0],
               [0,1,0,1,0,0,0,0,0,0,0,0,0,0,4,1,0,0,0,0,0],
               [0,0,1,0,2,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
               [0,0,0,2,0,8,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
               [0,0,0,0,8,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
               [0,0,0,0,0,1,0,1,2,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,2,0,0,4,1,0,0,0,0,0,0,0,0,0,5],
               [0,0,0,0,0,0,0,0,4,0,9,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,1,9,0,1,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,1,0,10,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,10,0,1,0,0,0,0,0,6,0],
               [0,0,0,1,1,0,0,0,0,0,0,0,1,0,2,0,0,0,0,3,0],
               [0,0,4,1,0,0,0,0,0,0,0,0,0,2,0,1,4,0,0,0,0],
               [0,4,1,0,0,0,0,0,0,0,0,0,0,0,1,0,2,0,3,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,0,6,1,0,0],
               [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,1,0,0],
               [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,1,0,0,0],
               [0,0,0,0,0,2,0,0,0,0,0,0,6,3,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,1,0,5,0,1,0,0,0,0,0,0,0,0,0,0]])

print(f"Rešitev grafa G1 je {TSP(G2, 0)}")
print(f"Rešitev grafa G2 je {TSP(G3, 1)}")
print(f"Rešitev grafa G3 je {TSP(G4, 13)}")

