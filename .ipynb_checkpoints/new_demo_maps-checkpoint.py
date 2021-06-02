# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:49:23 2021

@author: ago
"""

import numpy as np
import numpy.ma as ma
from nanofilm.ndimage import imread
import cv2



folder_path = './data_demo/RCEvase/'

def printing_img_details(image):

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
    
single_test_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'
single_test = imread(single_test_path)

printing_img_details(single_test)

cv2.imshow('raw',single_test)
cv2.waitKey(0)
cv2.destroyAllWindows()

maskednan = ma.masked_array(single_test, mask=np.isnan(single_test), )
fixednan = ma.fix_invalid(single_test, copy=False, fill_value=0) #this overwrites the image passed, replacing nans with 0

printing_img_details(maskednan)

cv2.imshow('fixed?', single_test)
cv2.waitKey(0)
cv2.destroyAllWindows()
