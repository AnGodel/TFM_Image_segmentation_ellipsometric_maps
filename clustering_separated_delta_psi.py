# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 11:02:14 2021

@author: ago
"""

import glob
import os
import numpy as np
from nanofilm.ndimage import imread
import elliPack.astroclean as at
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import matplotlib.pyplot as plt
import pandas as pd


class lambdaVarEllimaps:
    
    def __init__(self, path = None, ):
        
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
            
        self.getdatFile()
        self.readdatFile()
        self.loadDeltaMaps()
        self.loadPsiMaps()        
        #self.n_wl = np.arange(int(self.dim3/2))
        #self.Dindexes = [x for x in self.n_wl*2 if x%2 == 0]
        #self.Pindexes = [x+1 for x in self.n_wl*2 if x%2 == 0]
        
        #self.stackReshaped = self.all_maps.reshape(self.dim1*self.dim2, self.dim3)
        #self.segmentedStack = []

    def getdatFile(self):

        datFile = glob.glob(self.path + '/*.ds.dat')
        if len(datFile) >= 2:
            raise ValueError('The instantiated folder contains data from more than one experiment. The folder must contain only one .ds.dat file. Please clean the files in the folder and try again')
        else:
            self.datFile = str(datFile[0])
    
    def readdatFile(self):
        
        df = pd.read_csv(self.datFile, 
                              sep='\t', 
                              skiprows=[1])
        df.columns = df.columns.str.replace('#', '').str.lower()
        
        self.datatable = df
        self.WLarray = self.datatable['lambda'].to_numpy()
        DeltaFiles = self.datatable['delta'].tolist()
        PsiFiles = self.datatable['psi'].tolist()
        self.nWL = len(self.WLarray)
        self.DeltaFileList = [os.path.join(self.path, elem) for elem in DeltaFiles]
        self.PsiFileList = [os.path.join(self.path, elem) for elem in PsiFiles]
    
    def loadDeltaMaps(self):
        
        DeltaMaps = list(map(at.loadmap_astroclean, self.DeltaFileList))
        self.DeltaStack = np.dstack(DeltaMaps)
        self.dim1 = self.DeltaStack.shape[0]
        self.dim2 = self.DeltaStack.shape[1]
        self.dim3 = self.DeltaStack.shape[2]
        self.DeltaStackReshaped = self.DeltaStack.reshape(self.dim1*self.dim2, self.dim3)
    
    def loadPsiMaps(self):
        
        PsiMaps = list(map(at.loadmap_astroclean, self.PsiFileList))
        self.PsiStack = np.dstack(PsiMaps)
        self.PsiStackReshaped = self.PsiStack.reshape(self.dim1*self.dim2, self.dim3)
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        
        model = KMeans(random_state=0)
        
        visualizerDelta = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizerDelta.fit(self.DeltaStackReshaped)
        
        visualizerPsi = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizerPsi.fit(self.PsiStackReshaped)
        
        
        visualizerDelta.show(), visualizerPsi.show()
    
    #Having the two estimator visualizers in the same function makes the second estimator fail, somehow
    
    def getEstimation2(self, k=(2,11), metric = 'calinski_harabasz'):
        
        model = KMeans(random_state=0)
        
        visualizerDelta = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizerDelta.fit(self.DeltaStackReshaped)
        
        visualizerPsi = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizerPsi.fit(self.PsiStackReshaped)
        
        
        visualizerDelta.show(), visualizerPsi.show()
    
    def clusterize(self, k = 5):
        
        kmeansDelta = KMeans(n_clusters = k, random_state = 0).fit(self.DeltaStackReshaped)
        
        segmentedDelta = kmeansDelta.cluster_centers_[kmeansDelta.labels_]
        
        segmentedDeltaStack = segmentedDelta.reshape(self.dim1, self.dim2, self.dim3)
        
        kmeansPsi = KMeans(n_clusters = k, random_state = 0).fit(self.PsiStackReshaped)
        
        segmentedPsi = kmeansPsi.cluster_centers_[kmeansPsi.labels_]
        
        segmentedPsiStack = segmentedPsi.reshape(self.dim1, self.dim2, self.dim3)
        
        self.segmentedDeltaStack = segmentedDeltaStack
        self.segmentedPsiStack = segmentedPsiStack
        
        return segmentedDeltaStack, segmentedPsiStack
    
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
