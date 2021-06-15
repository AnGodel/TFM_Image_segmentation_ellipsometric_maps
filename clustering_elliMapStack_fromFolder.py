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


class lambdaVarEllimaps:
    
    def __init__(self, path = None):
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
        self.getFiles()
        self.loadAllMaps()

    def getFiles(self):
        
        self.all_files = glob.glob(self.path + '/*.png')
        
        return self.all_files
    
    def loadAllMaps(self):
        
        stack = list(map(at.loadmap_astroclean, self.all_files))
        self.all_maps = np.dstack(stack)
        
        return self.all_maps
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        
        dim1 = self.all_maps.shape[0]
        dim2 = self.all_maps.shape[1]
        dim3 = self.all_maps.shape[2]
        
        stackReshaped = self.all_maps.reshape(dim1*dim2, dim3)
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(stackReshaped)
        
        
        return visualizer.show()
    
    #Having the two estimator visualizer in the same function makes the second estimator fail
    
    def getEstimation2(self, k=(2,11), metric = 'distortion'):
        
        dim1 = self.all_maps.shape[0]
        dim2 = self.all_maps.shape[1]
        dim3 = self.all_maps.shape[2]
        
        stackReshaped = self.all_maps.reshape(dim1*dim2, dim3)
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k, 
                                      metric = metric)
        visualizer.fit(stackReshaped)
        
        return visualizer.show()
              
