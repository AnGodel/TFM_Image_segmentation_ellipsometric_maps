# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:25:36 2021

@author: Antonio
"""
import numpy as np


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