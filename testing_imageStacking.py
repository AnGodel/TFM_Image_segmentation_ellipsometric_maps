# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:01:53 2021

@author: ago
"""

import numpy as np
from nanofilm.ndimage import imread
import numpy.ma as ma
import matplotlib.pyplot as plt
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans
from sklearn.cluster import KMeans
import MyPacket.mypacket as mp
from yellowbrick.cluster import KElbowVisualizer

#setting the paths to demo delta and psi maps

delta1 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00018.png'
delta2 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00020.png'
delta3 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00022.png'

psi1 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00019.png'
psi2 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00021.png'
psi3 = './data_demo/demofiles_flake/20150513_IMAGE_autosave_00023.png'

#transforming the raw maps into two lists of processed 'images'
#preprocessing includes bit transformation into single-channel images with nanofilm.imread 
#and smoothing/NaN removal using convolution kernel with astropy 

deltas = list(map(mp.loadmap_astroclean, [delta1, delta2, delta3]))
psis = list(map(mp.loadmap_astroclean, [psi1, psi2, psi3]))

#the images are stacked by type using np.dstack

deltaStack = np.dstack(deltas)
psiStack = np.dstack(psis)

#then they are reshaped and KMeans segmentation is applied. 

DStackReshaped = deltaStack.reshape(deltaStack.shape[0]*deltaStack.shape[1], deltaStack.shape[2])

#the yellowbrick library is used for the evaluation of the KMeans clustering
#the results of this evaluation will give an indication of the right number of clusters,
#but this results should not be taken literally 

model = KMeans(random_state=0)
visualizer = KElbowVisualizer(model, k=(2,13))

visualizer.fit(DStackReshaped)
visualizer.show()

#After segmentation, they are plotted


kmeans = KMeans(n_clusters=5, random_state=0).fit(DStackReshaped)

segmented = kmeans.cluster_centers_[kmeans.labels_]

segmentedStack = segmented.reshape(deltaStack.shape[0], deltaStack.shape[1], deltaStack.shape[2])

mp.plot_image_withCbar(np.dsplit(segmentedStack, deltaStack.shape[2])[0], 'delta1Cluster')
mp.plot_image_withCbar(np.dsplit(segmentedStack, deltaStack.shape[2])[1], 'delta2Cluster')
mp.plot_image_withCbar(np.dsplit(segmentedStack, deltaStack.shape[2])[2], 'delta3Cluster')

#same procedure for psi maps

PStackReshaped = psiStack.reshape(psiStack.shape[0]*psiStack.shape[1], psiStack.shape[2])

kmeans = KMeans(n_clusters=6, random_state=0).fit(PStackReshaped)

segmented = kmeans.cluster_centers_[kmeans.labels_]

segmentedStack = segmented.reshape(psiStack.shape[0], psiStack.shape[1], psiStack.shape[2])

mp.plot_image_withCbar(np.dsplit(segmentedStack, psiStack.shape[2])[0], 'psi1Cluster')
mp.plot_image_withCbar(np.dsplit(segmentedStack, psiStack.shape[2])[1], 'psi2Cluster')
mp.plot_image_withCbar(np.dsplit(segmentedStack, psiStack.shape[2])[2], 'psi3Cluster')


