# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:36:31 2021

@author: Antonio
"""

from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans
from nanofilm.ndimage import imread


def map_load_astroclean (image, kernel = Gaussian2DKernel(x_stddev=1)):
    #9x9 kernel for smoothing
    image = imread(image).T
    
    imageclean = interpolate_replace_nans(image, kernel)
    
    return imageclean