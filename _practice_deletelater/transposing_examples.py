# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 14:52:57 2021

@author: ago
"""

graphene_path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'
RCE_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0004.png'
RCE_psi_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Psi_0004.png'

import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
from nanofilm.ndimage import imread
import MyPacket.mypacket as mp

flake = mp.loadmap_astroclean(graphene_path)
flakeTransposed = mp.loadmap_T_astroclean(graphene_path)

delta = mp.loadmap_astroclean(RCE_path)
deltaTransposed = mp.loadmap_T_astroclean(RCE_path)



mp.plot_image_withCbar(flake, 'flake without transpose')
mp.plot_image_withCbar(flakeTransposed, 'flake transposed')

mp.plot_image_withCbar(delta, 'delta without transpose')
mp.plot_image_withCbar(deltaTransposed, 'delta transposed')

