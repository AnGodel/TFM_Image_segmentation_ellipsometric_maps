# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:48:30 2021

@author: Antonio
"""

import MyPacket.mypacket as mp

path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'
path2 = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'
path3 = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Psi_0001.png'

graphene = mp.loadmap(path)

grapheneclean = mp.loadmap_astroclean(path)

grapheneZeros = mp.loadmap_nansAsZeros(path)

mp.plot_image(grapheneclean, Title='clean')

mp.plot_image(graphene, Title='raw')

mp.plot_image(grapheneZeros, Title='NaNs as Zeros')

delta = mp.loadmap_nansAsMean(path2) 
#we need to use en mean replacement here because the convolution with astropy 
#does not work here due to the large NaN areas in these maps
psi = mp.loadmap_nansAsMean(path3)

mp.plot_image(delta, Title='Delta')
mp.plot_image(psi, Title='Psi')

