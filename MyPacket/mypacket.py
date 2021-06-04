# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:44:28 2021

@author: Antonio
"""

import numpy as np
import numpy.ma as ma
from nanofilm.ndimage import imread
import matplotlib.pyplot as plt
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans

def printImageData(image_path):
    #function to quickly print relevant image details

    print('image name: {}'.format(image_path.split('/')[-1]))
    #for this to work 'image' has to be a path in str format
    image = imread(image_path).T
    #so this function will show always the information of 'raw' image
    #probably building a class where all de below info are attributes would be better
    print('type: {}'.format(type(image)))
    print('shape: {}'.format(image.shape))
    print('data type: {}'.format(image.dtype))
    print('width: {}'.format(image.shape[1]))
    print('height: {}'.format(image.shape[0]))
    fullpixels = np.count_nonzero(~np.isnan(image))
    nanpixels = np.count_nonzero(np.isnan(image))
    print('image size: {} pixels'.format(image.size))
    print('empty pixels: {}'.format(nanpixels))
    print('full pixels: {}'.format(fullpixels))
    print('\n')
    
    
def loadmap_astroclean (image, x_stddev = 1, x_size = 8, y_size = 8):
    #9x9 kernel for smoothing
    kernel = Gaussian2DKernel(x_stddev, x_size, y_size)
    image = imread(image).T
    
    imageclean = interpolate_replace_nans(image, kernel)
    
    return imageclean

def loadmap_nansAsZeros(image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    image = imread(image).T
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image

def loadmap_nansAsMean(image):
    
    image = imread(image).T
    
    imageclean = np.where(np.isnan(image), 
                       ma.array(image, 
                                mask=np.isnan(image)).mean(), 
                       image)
    return imageclean

def plot_image_withCbar(image, Title='title'):
    
    maxcontrast = np.max(image) 
    mincontrast = np.min(image) #this will work only for clean images with no nans
    
    fig, ax = plt.subplots(1, figsize=(10,10) )
    ax.set_axis_off()
    ax.set_title(Title)
    arrContrast = ax.imshow(image, 
                        vmin = mincontrast,
                        vmax = maxcontrast,
                        cmap = 'viridis')
    cbar = plt.colorbar(arrContrast, shrink=0.5)
    
    return cbar

def loadmap (path):
    image = imread(path).T
    
    return image

def printImageData(image):
    #function to quickly print relevant image details

    print('image name: {}'.format(' '))
    print('type: {}'.format(type(image)))
    print('shape: {}'.format(image.shape))
    print('data type: {}'.format(image.dtype))
    print('width: {}'.format(image.shape[1]))
    print('height: {}'.format(image.shape[0]))
    fullpixels = np.count_nonzero(~np.isnan(image))
    nanpixels = np.count_nonzero(np.isnan(image))
    print('image size: {} pixels'.format(image.size))
    print('empty pixels: {}'.format(nanpixels))
    print('full pixels: {}'.format(fullpixels))
    print('\n')