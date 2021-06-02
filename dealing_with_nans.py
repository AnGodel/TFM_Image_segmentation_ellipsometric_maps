# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 14:12:24 2021

@author: Antonio
"""

import numpy as np
import numpy.ma as ma
from nanofilm.ndimage import imread
import matplotlib.pyplot as plt

from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans

# Until now the nan pixels had been masked and replaced by zeros or other values
# usin numpy.ma:
    
    # image = ma.fix_invalid(image,
                             # copy=True/False,
                             # fill_value=zero or np.mean(image) or similar)
                             
# This solution is suboptimal, since replacing with zeros will create false edges
# and other values will introduce noise within the different areas.

# Ideally the nans should be replaced by the mean value of other pixels surrounding it.
# This can be done only with convolutions and astropy library provides good method for it.

# Reference: https://docs.astropy.org/en/stable/convolution/index.html

####### SETTING PATHS TO TEST IMAGES ###########

graphene_path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'
RCE_delta_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'
RCE_psi_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Psi_0001.png'

################################################

def printing_img_details(image):
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


# OLD FUNCTION TO LOAD MAPS AND CLEAN NANS
def map_load_cleannans(image, fill_value=0, copy=False):
    #input diferent fill_value, like np.mean(image) or np.median(image)
    #overrides the values in input image. Returned image is only a masked array
    image = imread(image).T
    
    image = ma.fix_invalid(image,
                           copy=copy, 
                           fill_value=fill_value)
    return image

# FUNCTION TO AUTOMATIZE PLOTTING IMAGES WITH MATPLOTLIB

def plot_image(image, Title='title'):
    
    maxcontrast = np.max(image) 
    mincontrast = np.min(image) #this will work only for clean images with no nans
    
    fig, ax = plt.subplots(1, figsize=(10,10) )
    ax.set_axis_off()
    ax.set_title(Title)
    arrContrast = ax.imshow(image, 
                        vmin = mincontrast,
                        vmax = maxcontrast,
                        cmap = 'Blues')
    cbar = plt.colorbar(arrContrast)
    cbar.set_title(Title)
    
    return cbar

graphene = map_load_cleannans(graphene_path)

raw = imread(RCE_delta_path)


def map_load_astroclean (image, kernel = Gaussian2DKernel(x_stddev=1),  ):
    #9x9 kernel for smoothing
    image = imread(image).T
    
    imageclean = interpolate_replace_nans(image, kernel)
    
    return imageclean

test = map_load_astroclean(graphene_path)

plot_image(test, Title='astrocleaned') 

plot_image(graphene, Title='nans_byzeros')


    
    
    
