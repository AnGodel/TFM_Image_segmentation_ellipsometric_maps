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

im_cv_gray = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(im_cv, (5, 5), 0)

cv2.imshow('cv read', im_cv)
#cv2.imshow('cv gray', im_cv_gray)
cv2.imshow('blurred', blurred)
cv2.waitKey(0)


# compute a "wide", "mid-range", and "tight" threshold for the edges
# using the Canny edge detector
wide = cv2.Canny(blurred, 10, 200)
mid = cv2.Canny(blurred, 30, 150)
tight = cv2.Canny(blurred, 240, 250)

# show the output Canny edge maps
cv2.imshow("Wide Edge Map", wide)
cv2.imshow("Mid Edge Map", mid)
cv2.imshow("Tight Edge Map", tight)
cv2.waitKey(0)