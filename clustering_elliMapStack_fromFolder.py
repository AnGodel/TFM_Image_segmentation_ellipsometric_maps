# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 11:02:14 2021

@author: ago
"""

import glob
import numpy as np
from nanofilm.ndimage import imread
import elliPack.astroclean as at
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import matplotlib.pyplot as plt



class lambdaVarEllimaps:
    
    def __init__(self, path = None):
        
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
            
        self.getFiles()
        self.loadAllMaps()
        self.dim1 = self.all_maps.shape[0]
        self.dim2 = self.all_maps.shape[1]
        self.dim3 = self.all_maps.shape[2]
        
        self.stackReshaped = self.all_maps.reshape(self.dim1*self.dim2, self.dim3)
        self.segmentedStack = []

    def getFiles(self):
        
        self.all_files = glob.glob(self.path + '/*.png')
        
    
    def loadAllMaps(self):
        
        stack = list(map(at.loadmap_astroclean, self.all_files))
        self.all_maps = np.dstack(stack)
        
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.stackReshaped)
        
        
        visualizer.show()
    
    #Having the two estimator visualizer in the same function makes the second estimator fail
    
    def getEstimation2(self, k=(2,11), metric = 'calinski_harabasz'):
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k, 
                                      metric = metric)
        visualizer.fit(self.stackReshaped)
        
        visualizer.show()
    
    def clusterize(self, k = 5):
        
        kmeans = KMeans(n_clusters = k, random_state = 0).fit(self.stackReshaped)
        
        segmented = kmeans.cluster_centers_[kmeans.labels_]
        
        segmentedStack = segmented.reshape(self.dim1, self.dim2, self.dim3)
        
        self.segmentedStack = segmentedStack
        
        return segmentedStack
    
    def plotDeltaPsi(self, idxDelta = 0, idxPsi = 1):
        
        idxDelta = idxDelta
        idxPsi = idxPsi
        imDelta = np.dsplit(self.segmentedStack, self.dim3)[idxDelta]
        imPsi = np.dsplit(self.segmentedStack, self.dim3)[idxPsi]
        
        fig, ax = plt.subplots(1,2, figsize=(15,8))
        plt.subplot(121)
        plt.imshow(imDelta, cmap = 'viridis')
        plt.set_title('Delta')
        plt.subplot(122)
        plt.imshow(imPsi, cmap = 'viridis')
        plt.set_title('Psi')
        # ax1 = plt.imshow(imDelta, cmap = 'viridis')
        # ax1.set_title('Delta')
        # ax2 = plt.imshow(imPsi, cmap = 'viridis')
        # ax2.set_title('Psi')
