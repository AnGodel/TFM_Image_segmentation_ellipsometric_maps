# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:25:52 2021

@author: ago
"""
# IMPORTS

import numpy as np
from nanofilm.ndimage import imread
import numpy.ma as ma
import cv2

# DEFINE IMAGE PATH -- WILL BE REWORKED USING ARGPARSE
    # WILL NEED ADAPTION TO WORK WITH ALL IMAGES IN ONE FOLDER
path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'
single_test_path = './data_demo/RCEvase/RCEvase_1zn_MapON_ScanON_AeON_FuE_2_Delta_0001.png'

# FUNCTIONS USED IN THE SCRIPT

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


def clean_nan(nparray):
    '''

    Parameters
    ----------
    nparray : an image transformed into numpy array.

    Returns
    -------
    nparray : same numpy array, where tne NaN pixels have been replaced by the mean value of all other pixels.
        This behavior can be changed. For example: .mean(axis=0) will do the mean of only the column where the NaN pixel is located.

    '''

    nparray = np.where(np.isnan(nparray), 
                       ma.array(nparray, 
                                mask=np.isnan(nparray)).mean(axis=0), 
                       nparray)
    return nparray

# function for automatic Canny edge detection
#   sigma is the only adjustable parameter
#       larger values makes wider threshold values for the hysteresis edge detection
#   upper limit is usually 255, but we need it larger, as our float32 pixel values can be larger

def auto_canny(image, sigma=0.8):

    # compute the median of the single channel pixel intensities
    v = np.nanmean(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

image = imread(single_test_path).T

printing_img_details(image)


# finding max and min pixel value
pixelmax = np.nanmax(image)
pixelmin = np.nanmin(image)
overalmean = np.nanmean(image)
overalmedian = np.nanmedian(image)

# cleaning nan from image

imageclean = clean_nan(image)
printing_img_details(imageclean)

# histogram needs to be worked on #######################################################

hist = cv2.calcHist([image], [0], None, [361], [0, 361])

######################################

# applying a gaussian blur to reduce low-level noise
#       # .astype uint8 is the only way for imshow to display the shades of gray in the image
            # needs further investigation
# will apply the blur to the image already clean of nans

blurred = cv2.GaussianBlur(imageclean, (5, 5), 0).astype('uint8')

dirty_blur = cv2.GaussianBlur(image, (5, 5), 0).astype('uint8')

dirty_edged = auto_canny(dirty_blur)

blur_edged = auto_canny(blurred)

cv2.imshow('nanofilm read', image)
cv2.imshow('blurred', blurred)
cv2.imshow('blurred edged', blur_edged)
cv2.imshow('dirty edged', dirty_edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

