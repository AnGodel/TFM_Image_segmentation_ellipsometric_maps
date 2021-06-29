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
            
        self.getdatFile()  # will find the .ds.dat file in the folder. #
        # Instantiates self.datFile
        self.readdatFile()  # reads the .dat file using pandas, intantiating:
            #self.datatable: no further use
            #self.WLarray: numpy array with a list of wavelengths used in the measurement
            #self.WLIndices: list of indices of WLarray. Used later for the map index selector
            #self.WLdict: dict with indices as keys and WL as values. For later use as reference in plots
            #self.nWL: just for easy retrieving the number of WL (number of maps) in the measurement
            #self.DeltaFileList: a list of file paths of the delta maps for the measurement. 
            #self.PsiFileList: same, but for psi maps. 
            #self.AllFileList: a list of file paths alternating delta,psi files
            # The load function will iterate over them to create a stack of "shuffled" readable images (numpy arrays)
        self.loadAllMaps()  # transforms raw delta maps into readable images.
        #Also does some pre-processing, including smoothing and NaN removal by convolution of a 9x9 kernel
        #The NaN removal will fail if there are NaN areas larger than the kernel in the raw map.
        #Instantiates:
            # self.AllShuffledStack: the stack of shuffled maps
            # self.AllShuffledStackReshaped: the reshaped stack ready for being passed to KMeans algorithm
            # self.dim1all, self.dim2all, self.dim3all: dimensions of the stack, being dim3 nWL*2

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
        self.WLIndices = np.arange(len(self.WLarray))
        self.WLdict = dict(zip(self.WLIndices, self.WLarray))
        DeltaFiles = self.datatable['delta'].tolist()
        PsiFiles = self.datatable['psi'].tolist()
        self.nWL = len(self.WLarray)
        self.DeltaFileList = [os.path.join(self.path, elem) for elem in DeltaFiles]
        self.PsiFileList = [os.path.join(self.path, elem) for elem in PsiFiles]
        self.AllFileList = []
        for (item1, item2) in zip(self.DeltaFileList, self.PsiFileList):
            self.AllFileList.append(item1)
            self.AllFileList.append(item2)
        
    def loadAllMaps(self):
        
        AllMaps = list(map(at.loadmap_astroclean, self.AllFileList))
        self.AllShuffledStack = np.dstack(AllMaps)
        self.dim1all = self.AllShuffledStack.shape[0]
        self.dim2all = self.AllShuffledStack.shape[1]
        self.dim3all = self.AllShuffledStack.shape[2]
        self.AllShuffledStackReshaped = self.AllShuffledStack.reshape(self.dim1all*self.dim2all, self.dim3all)
        self.AllIndices = np.arange(self.dim3all)
        self.DeltaIndices = [x for x in self.AllIndices if x%2 == 0]
        self.PsiIndices = [x + 1 for x in self.AllIndices if x%2 == 0]
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.AllShuffledStackReshaped)
        
        visualizer.show()
    
    #Having the two estimator visualizers in the same function makes the second estimator fail, somehow
    
    def getEstimation2(self, k=(2,11), metric = 'calinski_harabasz'):
        
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.AllShuffledStackReshaped)
        
        visualizer.show()
        
    def clusterize(self, k = 5):
        
        self.n_clustersList_shuffled = np.arange(k) # List to serve as index for the clusters
        
        kmeans = KMeans(n_clusters = k, random_state = 0).fit(self.AllShuffledStackReshaped)
        
        segmented = kmeans.cluster_centers_[kmeans.labels_]
        
        segmentedShuffledStack = segmented.reshape(self.dim1all, self.dim2all, self.dim3all)
        
        self.segmented = segmented
        self.segmentedShuffledStack = segmentedShuffledStack
        self.cluster_centers_ = kmeans.cluster_centers_
        self.cluster_labels_ = kmeans.labels_
        
    def clustershot(self):
        self.firstSegmentedDeltamap = self.segmentedShuffledStack[:,:,0]
        #first segmented Deltamap is used to identify position of clustered pixels. 
        #It could be any map, as here in the shuffled stack all clusters will always overlap along the 3rd axis        
        
        delta_shot = [] # each row is a  cluster shot of delta values
        psi_shot = [] # each row is a cluster shot of psi values
        
        for cluster_idx in self.n_clustersList_shuffled:
            
            C_ = np.unique(self.firstSegmentedDeltamap)[cluster_idx] #selects one value from unique values in first map
            C_ys, C_xs = np.where(self.firstSegmentedDeltamap==C_) #identifies position of all pixels with that value in the map
        
            D_pixelshot = [] # single cluster shot in the delta maps of the stack
            P_pixelshot = [] # single cluster shot in the psi maps of the stack

            for ellimap in self.DeltaIndices:
                Dpxval = np.unique(self.segmentedShuffledStack[C_ys,C_xs,ellimap])
                D_pixelshot.append(Dpxval[0]) # the [0] here is just to append the float and not the array [float] that np.unique generates
            delta_shot.append(D_pixelshot)
            
            for ellimap in self.PsiIndices:
                Dpxval = np.unique(self.segmentedShuffledStack[C_ys,C_xs,ellimap])
                P_pixelshot.append(Dpxval[0]) # the [0] here is just to append the float and not the array [float] that np.unique generates
            psi_shot.append(P_pixelshot)
            
        self.delta_shot = delta_shot
        self.psi_shot = psi_shot
    
    def plotDeltaPsi(self, idxSelector = 0):
        
        imDelta = self.AllShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        imPsi = self.AllShuffledStack[:,:,self.PsiIndices[idxSelector]]
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,11))
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
        fig.suptitle('Map index: {}: Wavelength: {} nm'.format(idxSelector, self.WLdict[idxSelector]))
        ax2.clear
        arrR2 = ax2.imshow(imPsi, cmap = 'gray')
        ax2.grid(b=None)
        ax2.set_title('Psi')
        fig.colorbar(arrR2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')
    
    def plotSegmentedDeltaPsi(self, idxSelector = 0):
        
        imDelta = self.segmentedShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        imPsi = self.segmentedShuffledStack[:,:,self.PsiIndices[idxSelector]]
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,11))
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
        fig.suptitle('Map index: {}: Wavelength: {} nm'.format(idxSelector, self.WLdict[idxSelector]))
        ax2.clear
        arrC2 = ax2.imshow(imPsi, cmap = 'viridis')
        ax2.grid(b=None)
        ax2.set_title('Psi')
        fig.colorbar(arrC2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')
    
    def plotOneShot(self, C_Selector = 0):
        
        idx = self.n_clustersList[C_Selector]
        Deltas = self.all_DeltaShots[C_Selector]
        Psis = self.all_PsiShots[C_Selector]
        WL = self.WLarray
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        fig.tight_layout()
        
        
        ax1.clear
        ax1.plot(self.WLarray, Deltas, color = 'red')
        ax1.set_title('Delta')
        ax1.grid(b=None)
        
        fig.suptitle('Cluster index: {}'.format(C_Selector))
        ax2.clear
        ax2.plot(self.WLarray, Psis, color = 'blue')
        ax2.grid(b=None)
        ax2.set_title('Psi')

    def plotAllShots(self, C_Selector = 0):
            
        idx = self.n_clustersList[C_Selector]
        Deltas = self.all_DeltaShots
        Psis = self.all_PsiShots
        WL = self.WLarray
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,5))
        fig.tight_layout()
        
        
        ax1.clear
        for C_Selector in self.n_clustersList:
            ax1.plot(self.WLarray, Deltas[C_Selector], alpha=0.7)
        ax1.scatter(self.WLarray, Deltas[C_Selector], color='red')
        ax1.set_title('Delta')
        ax1.grid(b=None)
        
        fig.suptitle('Cluster index: {}'.format(C_Selector))
        for C_Selector in self.n_clustersList:
            ax2.plot(self.WLarray, Psis[C_Selector], alpha=0.7)
        ax2.scatter(self.WLarray, Psis[C_Selector], color='blue')
        ax2.grid(b=None)
        ax2.set_title('Psi')