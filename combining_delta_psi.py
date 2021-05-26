# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:46:03 2021

@author: ago
"""

import numpy as np
from nanofilm.ndimage import imread
import cv2
import numpy.ma as ma


def CmatTransform (delta, psi):
    
    Cmat = np.sin(2*psi)*np.cos(delta)
    
    return Cmat

def SmatTransform (delta, psi):
    
    Smat = np.sin(2*psi)*np.sin(delta)
    
    return Smat

deltaraw = 'C:/Users/ago/SynologyDrive/GIT_projects/laptop-praktikum/TFM_Image_segmentation_ellipsometric_maps/data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'

psiraw = 'C:/Users/ago/SynologyDrive/GIT_projects/laptop-praktikum/TFM_Image_segmentation_ellipsometric_maps/data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Psi_0001.png'

# we need to transpose to keep Accurion's coordinate convention

delta = imread(deltaraw).T
psi = imread(psiraw).T


testC = CmatTransform(delta, psi)
testS = SmatTransform(delta, psi)

cv2.imshow('rawC', testC)
cv2.imshow('rawS', testS)
cv2.waitKey(0)
#cv2.destroyAllWindows()

# cleaning nans

def nan_by_value (image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image

cleanC = nan_by_value(testC)
cleanS = nan_by_value(testS)

cv2.imshow('cleanC', cleanC)
cv2.imshow('cleanS', cleanS)
cv2.imshow('cleanrawC', testC)
cv2.imshow('cleanrawS', testS)

cv2.waitKey(0)
cv2.destroyAllWindows()

# blurring





