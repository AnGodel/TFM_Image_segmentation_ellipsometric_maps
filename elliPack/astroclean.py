# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:36:31 2021

@author: Antonio
"""

from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans
from nanofilm.ndimage import imread
import numpy.ma as ma
import numpy as np


def loadmap_T_astroclean (image, x_stddev = 1, x_size = 8, y_size = 8):
    #9x9 kernel for smoothing
    kernel = Gaussian2DKernel(x_stddev, x_size, y_size)
    image = imread(image).T
    
    imageclean = interpolate_replace_nans(image, kernel)
    
    return imageclean

def loadmap_astroclean (image, x_stddev = 1, x_size = 8, y_size = 8):
    #9x9 kernel for smoothing
    kernel = Gaussian2DKernel(x_stddev, x_size, y_size)
    image = imread(image)
    
    imageclean = interpolate_replace_nans(image, kernel)
    
    return imageclean

def loadmap_T_nansAsZeros(image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    image = imread(image).T
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image

def loadmap_nansAsZeros(image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    image = imread(image)
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image


def loadmap_T_nansAsMean(image):
    
    image = imread(image).T
    
    imageclean = np.where(np.isnan(image), 
                       ma.array(image, 
                                mask=np.isnan(image)).mean(), 
                       image)
    return imageclean

def loadmap_nansAsMean(image):
    
    image = imread(image)
    
    imageclean = np.where(np.isnan(image), 
                       ma.array(image, 
                                mask=np.isnan(image)).mean(), 
                       image)
    return imageclean