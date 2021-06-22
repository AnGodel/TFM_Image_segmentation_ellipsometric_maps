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
    
    def __init__(self, path = None, ):
        
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
            
        self.getmapFiles()
        self.loadAllMaps()
        self.getdatFile()
        
        
        self.n_wl = np.arange(int(self.dim3/2))
        self.Dindexes = [x for x in self.n_wl*2 if x%2 == 0]
        self.Pindexes = [x+1 for x in self.n_wl*2 if x%2 == 0]
        
        self.stackReshaped = self.all_maps.reshape(self.dim1*self.dim2, self.dim3)
        self.segmentedStack = []

    def getmapFiles(self):
        
        self.all_files = glob.glob(self.path + '/*.png')
    
    def getdatFile(self):
        
        datFile = glob.glob(self.path + '/*.ds.dat')
        if len(datFile) >= 2:
            raise ValueError('The instatiated folder contains data from more than one experiment. The folder must contain only one .ds.dat file. Please clean the files in the folder and try again')
        else:
            self.datFile = str(datFile[0])
    
    def getWavelengths(self):
        
        WLarray = np.loadtxt(self.datFile,
                             usecols=0,
                             skiprows=2)
        
        if len(WLarray) != self.n_wl:
            raise ValueError('The number of wavelength in the .dat file does not match the number of maps in the instantiated folder. The folder should have {} .png files, not more and not less'.format(self.n_wl))
        else:
            self.WLarray = WLarray
        
    
    def loadAllMaps(self):
        
        stack = list(map(at.loadmap_astroclean, self.all_files))
        self.all_maps = np.dstack(stack)
        self.dim1 = self.all_maps.shape[0]
        self.dim2 = self.all_maps.shape[1]
        self.dim3 = self.all_maps.shape[2]
        
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.stackReshaped)
        
        
        visualizer.show()
    
    #Having the two estimator visualizers in the same function makes the second estimator fail, somehow
    
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
    
    def pickonefromstack(self, imstack, idxSelector = 0):
        
        selected = np.dsplit(imstack, imstack.shape[2])[idxSelector]
        
        return selected
    
    def plotDeltaPsi(self, idxSelector = 0):
        
        idxDelta = self.Dindexes[idxSelector]
        idxPsi = self.Pindexes[idxSelector]
        imDelta = self.pickonefromstack(self.all_maps, idxDelta)
        imPsi = self.pickonefromstack(self.all_maps, idxPsi)
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,8))
        fig.tight_layout()
        
        ax1.clear
        arrR1 = ax1.imshow(imDelta, cmap = 'gray')
        ax1.set_title('Delta')
        ax1.grid(b=None)
        fig.colorbar(arrR1, 
                     ax=ax1, 
                     shrink=0.5, 
                     location='left',
                     pad=0.048)
        
        ax2.clear
        arrR2 = ax2.imshow(imPsi, cmap = 'gray')
        ax2.grid(b=None)
        ax2.set_title('Psi')
        fig.colorbar(arrR2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')
    
    def plotSegmentedDeltaPsi(self, idxSelector = 0):
        
        idxDelta = self.Dindexes[idxSelector]
        idxPsi = self.Pindexes[idxSelector]
        imDelta = self.pickonefromstack(self.segmentedStack, idxDelta)
        imPsi = self.pickonefromstack(self.segmentedStack, idxPsi)
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,8))
        fig.tight_layout()
        
        ax1.clear
        arrC1 = ax1.imshow(imDelta, cmap = 'viridis')
        ax1.set_title('Delta')
        ax1.grid(b=None)
        fig.colorbar(arrC1, 
                     ax=ax1, 
                     shrink=0.5, 
                     location='left',
                     pad=0.048)
        
        ax2.clear
        arrC2 = ax2.imshow(imPsi, cmap = 'viridis')
        ax2.grid(b=None)
        ax2.set_title('Psi')
        fig.colorbar(arrC2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')