#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:21:18 2021

@author: antonio
"""
import numpy as np
from nanofilm.ndimage import imread
import cv2

path = './data_demo/Flakesearch_Graphene_20180214175340935_087.png'


im_cv = cv2.imread(path)

blurred = cv2.GaussianBlur(im_cv, (5, 5), 0)

cv2.imshow('cv read', im_cv)
cv2.imshow('blurred', blurred)
cv2.waitKey(0)


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


auto = auto_canny(blurred)

# show the images
cv2.imshow("Original", im_cv)
cv2.imshow("Edges", auto)
cv2.waitKey(0)
