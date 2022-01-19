# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 10:54:40 2022

@author: music
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.signal import blackman
from scipy.fft import fft
from time import sleep

class Signal:

    def __init__(self, frekvenca_vzorčenja, bit, okno, šum, prekrivanje, digat):
        self.bits = bit

        self.Vmin = -1000
        self.Vmax = 1000

        self.A = 20  # amplituda
        self.f = 23  # frekvenca
        self.phi = 0.8  # kotni zamik

        self.T = 10  # čas opazovanja
        self.N_signala = 100000  # diskretuzacija, število točk
        self.frekvenca_vzorčenja = frekvenca_vzorčenja
        self.N = int(self.T * self.frekvenca_vzorčenja)

        #"previ signal"
        self.t0 = np.linspace(0, self.T, self.N_signala)
        self.y0 = self.pripravi_signal(self.t0, šum, False)
        self.dist = np.linspace(self.Vmin, self.Vmax, 2**self.bits)
        # generiranje signala
        self.t = np.linspace(0, self.T, self.N)
        self.signal = self.pripravi_signal(self.t, šum, digat)

        # filtriranje

        # dft
        self.delitev_signala(1, prekrivanje)  # delitev signala na 1s segmente
        self.s, self.f = self.dft(self.container, okno)
        # povprešenje signala
        self.povprečenje()

    def pripravi_signal(self, t, A_sum, diskritizacija):
        for i in range(5):
            if i == 0:
                y = (6 - i + 1) * self.A * np.cos((i + 1) * 2 * np.pi * self.f * t + self.phi)
            else:
                y += (6 - i + 1) * self.A * np.cos((i + 1) * 2 * np.pi * self.f * t + self.phi)
        self.šum = A_sum * (np.random.rand(len(t)) - 0.5)
        y = y + self.šum
        if diskritizacija:
            d = (self.Vmax - self.Vmin) / (2**self.bits - 1)
            y = np.sign(y) * (d / 2 + d * np.floor(np.abs(y) / d))
        # print(f"SNR = {10*np.log10(np.std(y)**2/np.std(šum)**2):.2f} dB")
        return y

    def delitev_signala(self, t_bin, prekrivanje):
        """razdeli signal v bine, signal se lahko prekriva za prekrivanje [%]"""

        število_binov = int(self.T / (t_bin * (1 - prekrivanje)))
        self.bin_n = int(self.frekvenca_vzorčenja * t_bin)

        container = []
        prvi = 0
        for i in range(število_binov):
            zadnji = prvi + self.bin_n
            sig = self.signal[prvi:zadnji]
            if len(sig) == self.bin_n:
                container.append(sig)
            prvi = zadnji - int(self.bin_n * prekrivanje)
        self.container = np.array(container)

    def dft(self, signal, okno):
        """DFT s pomočjo FFT, narejen na signalu"""
        if okno == 'None':
            y = signal
        elif okno == 'Hann':
            y = signal * np.hanning(self.bin_n)
        elif okno == 'Hamming':
            y = signal * np.hamming(self.bin_n)
        elif okno == 'Blackman':
            y = signal * blackman(self.bin_n)
        s = np.abs(fft(y))
        # vzame se polovico (simetričen okoli 0) in se podvoji vrednost
        s_plot = 2 * s[:, :int(self.bin_n / 2)] / (self.bin_n / 2)
        f_plot = np.linspace(0, int(self.frekvenca_vzorčenja / 2), int(self.bin_n / 2))

        return s_plot, f_plot

    def povprečenje(self):
        self.s_povp = 0
        for i in self.s:
            self.s_povp += 1 / len(self.s) * i

    def plot_signal(self):
        plt.clf()
        plt.plot(self.t, self.signal)
        plt.xlim(0, 0.3)
        plt.show()

    def plot_fft(self):
        # plt.clf()
        # plt.semilogy(self.f,self.s[0])
        plt.semilogy(self.f, self.s_povp)
        plt.xlim(0, 150)
        plt.show()

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.title("DFT-obdelava signalov demo")
        self.master.bind('<Return>', self.func)
        # frejmi
        frame_plot = tk.Frame(self.master)
        frame_plot.grid(row=0, column=0, rowspan=4)
        frame_info = tk.LabelFrame(
            master=self.master, relief=tk.RAISED, borderwidth=1, text="INFO")
        frame_info.grid(row=0, column=1)
        frame_kontrola_signala = tk.LabelFrame(
            master=self.master, relief=tk.RAISED, borderwidth=1, text="Nastavive signala")
        frame_kontrola_signala.grid(row=1, column=1)
        # frame_kontrola_filtrov = tk.LabelFrame(
        #    master=self.master, relief=tk.RAISED, borderwidth=1, text="Nastavive filtrov")
        #frame_kontrola_filtrov.grid(row=2, column=1)
        frame_kontrola_dft = tk.LabelFrame(
            master=self.master, relief=tk.RAISED, borderwidth=1, text="Nastavive zajema")
        frame_kontrola_dft.grid(row=2, column=1)

        # definiranje plota
        self.fig, self.axes = plt.subplots(
            nrows=2, ncols=1, figsize=(10, 7))

        # opremljanje grafa za signal
        self.axes[0].set_title("Signal")
        self.axes[0].set_xlabel("Čas [s]")
        self.axes[0].set_ylabel("Vrednost")
        self.axes[0].grid()

        # opremljanje grafa za DFT
        self.axes[1].set_title("DFT")
        self.axes[1].set_xlabel("Frekvenca [Hz]")
        self.axes[1].set_ylabel("Amplituda")
        self.axes[1].grid()

        # self.fig.tight_layout()

        self.graph = FigureCanvasTkAgg(
            self.fig, master=frame_plot)
        self.graph.get_tk_widget().pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(
            self.graph, frame_plot)
        self.toolbar.update()
        self.graph._tkcanvas.pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # INFO
        label_info = tk.Label(frame_info, text="Simulacije se izvajajo na siglau, ki je definiran kot:")
        label_info.grid(row=0, column=0)
        #label_enacba = tk.Label(frame_info, text=r"$\sum_{n=1}^{\infty}$")
        #label_enacba.grid(row=1, column=0)
        # nastavitve signala
        fig1 = matplotlib.figure.Figure(figsize=(3.6, 1.5), dpi=100)
        ax1 = fig1.add_subplot(111)

        frame_eq = tk.Frame(frame_info)
        frame_eq.grid(row=1, column=0)
        canvas1 = FigureCanvasTkAgg(fig1, master=frame_eq)
        canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)
        canvas1._tkcanvas.pack(side="top", fill="both", expand=True)

        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)

        enačba = "$\sum_{n=1}^{5}(6-n)\cdot cos(n \cdot A\cdot 2\pi \cdot f \cdot t + \phi )+u(t)$"
        spremenljivke = " A = 20\n f = 23 Hz\n $\phi$ = 0.8 rad "
        ax1.text(0.03, 0.2, enačba, fontsize=10)
        ax1.text(0.05, 0.65, spremenljivke, fontsize=8)
        canvas1.draw()

        label_signal = tk.Label(
            frame_kontrola_signala, text="Amplituda šuma")
        label_signal.grid(row=0, column=0)

        self.entry_A_sum = tk.Entry(frame_kontrola_signala)
        self.entry_A_sum.grid(row=0, column=1)
        self.entry_A_sum.insert(0, "2")

        label_SNR = tk.Label(
            frame_kontrola_signala, text="SNR")
        label_SNR.grid(row=2, column=0)

        self.snr_var = tk.StringVar()
        self.label_SNR_reading = tk.Label(
            frame_kontrola_signala, textvariable=self.snr_var)
        self.label_SNR_reading.grid(row=2, column=1)

        # nasavitve filtrov
        #label_filtri = tk.Label(frame_kontrola_filtrov, text="Uproabimo filter")
        #label_filtri.grid(row=0, column=1, columnspan=2)

        # nastaviteve DFT
        label_frekvenca_vzorcenja = tk.Label(frame_kontrola_dft, text="Frekvenca vzorčenja [Hz]")
        label_frekvenca_vzorcenja.grid(row=0, column=0)

        self.entry_f = tk.Entry(frame_kontrola_dft)
        self.entry_f.grid(row=0, column=1)
        self.entry_f.insert(0, "1000")

        label_diskritizacija = tk.Label(frame_kontrola_dft, text="Diskritizacija [bit]")
        label_diskritizacija.grid(row=1, column=0)

        self.entry_dis = tk.Entry(frame_kontrola_dft)
        self.entry_dis.grid(row=1, column=1)
        self.entry_dis.insert(0, "4")

        label_vmin = tk.Label(frame_kontrola_dft, text="Vmin")
        label_vmin.grid(row=2, column=0)

        label_vmax = tk.Label(frame_kontrola_dft, text="Vmax")
        label_vmax.grid(row=3, column=0)

        self.var_dis = tk.BooleanVar()
        self.var_dis.set(False)
        self.cb_dis = tk.Checkbutton(frame_kontrola_dft, text='Digatilizacija (samo za <SNR)', variable=self.var_dis, command=self.update_grafe)
        self.cb_dis.grid(row=4, column=0, columnspan=2)

        label_okno = tk.Label(frame_kontrola_dft, text="Okno")
        label_okno.grid(row=5, column=0)

        self.okna = ['None', 'Hann', 'Hamming', 'Blackman']
        self.variable_okno = tk.StringVar(self.master)
        self.om_okno = tk.OptionMenu(
            frame_kontrola_dft, self.variable_okno, *self.okna, command=self.okno_update)
        self.om_okno.grid(row=5, column=1)
        self.variable_okno.set(self.okna[0])
        self.okno = self.okna[0]

        self.var_avg = tk.BooleanVar()
        self.var_avg.set(False)
        self.cb_avg = tk.Checkbutton(frame_kontrola_dft, text='povprečenje signala (1s)', variable=self.var_avg, command=self.update_grafe)
        self.cb_avg.grid(row=6, column=0, columnspan=2)

        label_prekrivanje = tk.Label(frame_kontrola_dft, text="Prekrivanje signalov [0-40%]")
        label_prekrivanje.grid(row=7, column=0)

        self.entry_prekrivanje = tk.Entry(frame_kontrola_dft,)
        self.entry_prekrivanje.grid(row=7, column=1)
        self.entry_prekrivanje.insert(0, "10")

        self.update_grafe()

#=============================================================================

    def okno_update(self, okno):
        self.okno = okno
        self.update_grafe()

    def func(self, event):
        self.update_grafe()

    def pridobi_podatke(self):

        # podatki signala
        try:
            self.šum = int(self.entry_A_sum.get())
        except:
            self.entry_A_sum.delete(0, 'end')
            self.entry_A_sum.insert(0, "2")
            self.šum = 2

        # branje dft
        try:
            self.frekvenca_vzorčenja = float(self.entry_f.get())
        except:
            self.entry_A_sum.delete(0, 'end')
            self.entry_A_sum.insert(0, "1000")
            self.frekvenca_vzorčenja = 1000

        try:
            self.dis = int(self.entry_dis.get())
        except:
            self.entry_dis.delete(0, 'end')
            self.entry_dis.insert(0, "4")
            self.dis = 4

        try:
            self.prekrivanje = int(self.entry_prekrivanje.get())
            if self.prekrivanje < 0:
                self.prekrivanje = 0
            elif self.prekrivanje > 60:
                self.prekrivanje = 60
        except:
            self.entry_prekrivanje.delete(0, 'end')
            self.entry_prekrivanje.insert(0, "10")
            self.prekrivanje = 10

    def update_grafe(self):
        # branje parametrov
        self.pridobi_podatke()

        signal = Signal(self.frekvenca_vzorčenja, self.dis, self.okno, self.šum, self.prekrivanje / 100, self.var_dis.get())
        # signal = Signal(self.sum, 0)
        # graf za signal
        self.axes[0].cla()
        self.axes[0].plot(signal.t0, signal.y0)
        self.axes[0].plot(signal.t, signal.signal, "o")
        if (self.var_dis.get()) == True:
            for i in signal.dist:
                self.axes[0].plot([0, signal.T], [i, i], "g", linewidth=0.2)
        self.axes[0].set_title("Signal")
        self.axes[0].set_xlabel("Čas [s]")
        self.axes[0].set_ylabel("Vrednost")
        self.axes[0].set_xlim(0, 0.25)
        # self.axes[0].grid()
        # graf za DFT
        self.axes[1].set_title("DFT")
        self.axes[1].cla()
        if (self.var_avg.get()) == True:
            for i in signal.s:
                self.axes[1].semilogy(signal.f, i, c='C0', alpha=0.3, label='_nolegend_')
            self.axes[1].semilogy(signal.f, signal.s_povp, c='C3', label='$X_{avg}$')
        else:
            self.axes[1].semilogy(signal.f, signal.s[0])
        self.axes[1].set_xlabel("Frekvenca [Hz]")
        self.axes[1].set_ylabel("Amplituda")
        self.axes[1].set_xlim(0, 200)
        self.axes[1].set_ylim(0.01, 1000)
        self.axes[1].legend()
        self.axes[1].grid()

        self.snr_var.set(f"{10*np.log10(np.std(signal.y0)**2/np.std(signal.šum)**2):.2f} dB")

        self.graph.draw()


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = GUI(root)
    root.mainloop()
