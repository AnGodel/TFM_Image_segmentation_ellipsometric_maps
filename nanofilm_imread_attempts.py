# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:25:52 2021

@author: ago
"""

import numpy as np
from nanofilm.ndimage import imread
import cv2

path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'

im_nano = imread(path)

#counting the number of nan values inside the image

nanpixels = np.count_nonzero(np.isnan(im_nano))
fullpixels = np.count_nonzero(~np.isnan(im_nano))
print('the map has {} empty pixels and {} not empty pixels'.format(nanpixels,fullpixels))

#finding max and min pixel value
pixelmax = np.nanmax(im_nano)
pixelmin = np.nanmin(im_nano)

#mask to hide all nan values
nanmask = (~np.isnan(im_nano)) 
#esto no funciona al aplicar la mascara al histograma. 
#Pero habrá que quitar los nan de alguna manera porque van a estorbar en otras operaciones seguro

hist = cv2.calcHist([im_nano], [0], nanmask, [360], [pixelmin, pixelmax])

blurred = cv2.GaussianBlur(im_nano, (5, 5), 0)

cv2.imshow('nanofilm read', im_nano)
cv2.imshow('blurred', blurred)
cv2.waitKey(0)

