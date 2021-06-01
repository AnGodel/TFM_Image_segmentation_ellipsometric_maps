# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:27:43 2021

@author: ago
"""

from nanofilm.ndimage import imread
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from skimage.exposure import histogram
import skimage
from skimage.feature import canny

path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'
single_test_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'

def map_load_cleannans(image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    image = imread(image).T
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image

graphene = map_load_cleannans(path)

hist_graphene, hist_graphene_centers = histogram(graphene)

#plt.plot(hist_graphene)
# plt.imshow(graphene)

'''

arrBinsToCalcate =np.arange(162., 210., 0.05)
arrHisto, bins = np.histogram(arrMap, bins = arrBinsToCalcate)
figHisto, axHisto = plt.subplots(1)
axHisto.plot(bins[1:], arrHisto)

'''



arrHisto, bins = np.histogram(graphene, bins=int(np.max(graphene)))


mincontrast = np.min(np.where(arrHisto[1:]>=100))
maxcontrast = np.max(np.where(arrHisto[1:]>=100))

BinsToCalcate = np.arange(mincontrast, maxcontrast, 0.01)

correctedHisto, correctedBins = np.histogram(graphene, bins=BinsToCalcate)


#plt.plot(correctedBins[1:], correctedHisto)

edges = canny(graphene)

plt.imshow(edges)
