# -*- coding: utf-8 -*-

import cv2
from nanofilm.ndimage import imread
import matplotlib.pyplot as plt

path = '.\data_demo\Flakesearch_Graphene_20180214175340935_087.png'
colormap = 'jet'

original = imread(path)

img_origin = cv2.imread(path, 1)

img_cv = cv2.resize(original,(200,200))

img = cv2.bitwise_not(img_origin)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img_binary = cv2.threshold(img_gray, 35, 1, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
img_contour = cv2.drawContours(img_origin, contours, -1, (0, 255, 0), 5)

fig2=plt.figure()  
plt.title('image')
plt.xlabel('X-axis(pixel)')
plt.ylabel('Y-axis(pixel)')
nMappable = plt.imshow(img_origin, cmap = colormap)
plt.colorbar(nMappable)