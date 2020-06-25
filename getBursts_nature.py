# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:43:17 2019

@author: Raphael Jacquat (University of Cambridge)
This version is translated from Matlab files provided by
Georg Krainer (University of Cambridge) & Andreas Hartmann (TU Dresden).
It has been further developed and modified by Raphael Jacquat.
In order to run the files you will need the dependencies:
readPTU.py, burstLoc.py, leeFilter.py
"""
# Load main packages
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os.path
# Load dependencies
from Leefilter import leeFilter1D_Add  # Load LeeFilter
from burstLoc import burstLoc  # Load the burst localisation code
from readPTU import readPTU  # Load script for transforming binary .ptu in .out

root = tk.Tk()
root.withdraw()

# % INPUT parameters
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
setLeeFilter = 4  # Lee filter window size parameter (for DEMO: 4)
threIT = 0.1  # (ms) maximum inter-photon time (for DEMO: 0.1)
minPhs = 7  # minimum number of photons per burst (for DEMO: 7)
boolShow = 1  # Add 1 to display the trace result or 0 to hide (for DEMO: 1)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %% LOAD PTU files, extract time stamps of detected photons in an array.
# The array is called "Photons".
print((f"Script for counting the number of molecules"+
      " passing through the confocal laser spot\n\n"))
print(f"Choose .ptu file to analyse. If no dialogue box pops up, it might be behind the other windows.")
filename = filedialog.askopenfilename(filetypes=(('ptu files', 'ptu'),))
root.withdraw()
outputfile_name = filename[:-3] + "out"

if not os.path.isfile(outputfile_name):
    print("PTU file is converted. It may take up to 10 sec.")
    readPTU(filename, outputfile_name)

print(f"Calculation in progress...")
Photons = np.fromfile(outputfile_name)  # time saved in ps
Photons = np.reshape(Photons, (-1, 2))
Photons[:, 1] = Photons[:, 1] / 1000  # time in ns : ps/1000 -> ns

# %% FINDING NUMBER OF BURSTS
macroT = Photons[:, 1]  # (ns)
channel = Photons[:, 0]

# Find inter-photon time
interPhT = np.diff(macroT)  # (ns)
# Smooth with Leefilter
interLee = leeFilter1D_Add(interPhT, setLeeFilter)

# 1st filter (ipt)
# threshold for inter photon time
indexSig = np.asarray(np.where(np.logical_and(0.4 < interLee,
                                              interLee < (threIT * 1000000))),
                      dtype=int)


if np.asarray(indexSig).size != 0:
    bStart, bLength = burstLoc(indexSig, 1)

    # 2nd filter (minimum number of photons)
    # minimum photons per bursts
    bStartLong = bStart[bLength >= minPhs]
    bLengthLong = np.asarray(bLength[bLength >= minPhs], dtype=int)

    #  % collect Photons
    Bursts = np.zeros((int(np.sum(bLengthLong)), 3))
    lInd = 0

    for i in range(0, np.size(bStartLong)):

        BurstNumber = (np.ones(bLengthLong[i]) * i)
        Photons2 = Photons[
                           bStartLong[i]:
                           (bStartLong[i] + bLengthLong[i])
                           ]

        Bursts[lInd:lInd+bLengthLong[i], :] = np.concatenate((
                                                BurstNumber[:, np.newaxis],
                                                Photons2), axis=1)
        lInd = lInd + bLengthLong[i]

    # separate all number of photons
    NI = np.zeros(np.size(bStartLong))
    TBurst = np.zeros(np.size(bStartLong))

    for i in range(0, np.size(bStartLong)):

        N = Bursts[Bursts[:, 0] == i, 2]
        NI[i] = np.size(N[:])

        TBurst[i] = np.sum(interPhT[bStartLong[i] - 1: bStartLong[i]
                           + bLengthLong[i] - 1] * 1e-6)  # (ms)

#%% DISPLAY the results

    if boolShow == 1:

        #  Show intensity time trace
        edges = np.arange(0, (np.round(macroT[-1] * 1e-6)))
        hI = np.histogram(macroT * 1e-6, edges)

        f1 = plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot((edges[:-1]+edges[0]/2) / 1000, hI[0])  # ps / 1000 = ns
        plt.xlim((0, 5))
        plt.xlabel('Time (s)')
        plt.ylabel('Count rate (kHz)')

        hight_crosses = np.nanmax(hI[0]) + np.nanmax(hI[0])/25
        for i in range(0, np.size(bStartLong)):
            masksup = macroT > macroT[bStartLong[i]]
            maskinf = macroT < macroT[bStartLong[i] + bLengthLong[i] + 1]
            mask = maskinf * masksup
            hI_red = np.histogram(macroT[mask] * 1e-6, edges)
            plt.plot((edges[:-1][hI_red[0] > 0] + edges[0]/2) / 1000,
                     np.full(len(hI_red[0][hI_red[0] > 0]), hight_crosses),
                     'ro-', clip_on=True)
        plt.subplot(2, 2, 2)
#      #% Show inter-photon time
        plt.plot(interPhT/1000000)
        plt.xlim((0, 1000))
        plt.xlabel('Photon$_{i+1->i}$')
        plt.ylabel('Inter-photon time (ms)')

        for i in range(0, np.size(bStartLong) - 1):

            plt.plot(np.arange(bStartLong[i] + 1,
                               bStartLong[i] + bLengthLong[i]),
                     interPhT[bStartLong[i] + 1: bStartLong[i] +
                              bLengthLong[i]] / 1000000,
                     'r')

#      #% Show burst duration histogram
        edgesT = np.arange(0, 6, 0.1)
        hT = np.histogram(TBurst, edgesT)

        plt.subplot(2, 2, 3)
        plt.bar(edgesT[0:-1] + edgesT[1]/2, hT[0], edgesT[1])
        plt.xlabel('$T_{\mathrm{B}} $(ms)')
        plt.ylabel('Number of molecules')

#      #% Show number of photons per burst (histogram)
        edgesN = np.arange(0, 200, 5)
        edgesN = edgesN + edgesN[0]/2
        hN = np.histogram(NI, edgesN)

        plt.subplot(2, 2, 4)
        plt.bar(edgesN[0:-1]+edgesN[1]/2, hN[0], edgesN[1])
        plt.xlabel("Number of photons per molecule")
        plt.ylabel('Number of molecules')

print(f"Number of bursts detected : {len(NI)}")
if boolShow == 1:
    print(("To end the script, close all figures " +
          "(if run outside an iPython console.)"))
    plt.show()
else:
    input("Press enter to end...")


