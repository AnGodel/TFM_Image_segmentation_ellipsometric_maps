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
            
        self.getdatFile() #will find the .ds.dat file in the folder. #
        #Instantiates self.datFile
        self.readdatFile() #reads the .dat file using pandas, intantiating:
            #self.datatable: no further use
            #self.WLarray: numpy array with a list of wavelengths used in the measurement
            #self.indices: list of indices of WLarray. Used later for the map index selector
            #self.WLdict: dict with indices as keys and WL as values. For later use as reference in plots
            #self.nWL: just for easy retrieving the number of WL (number of maps) in the measurement
            #self.DeltaFileList: a list of file paths of the delta maps for the measurement. 
            #self.PsiFileList: same, but for psi maps. The load function will iterate over them to create readable images (numpy arrays)
        self.loadDeltaMaps() # transforms raw delta maps into readable images.
        #Also does some pre-processing, including smoothing and NaN removal by convolution of a 9x9 kernel
        #The NaN removal will fail if there are NaN areas larger than the kernel in the raw map.
        #Instantiates:
            #self.DeltaStack: a 'pile' of processed maps, with dimensions (rows,cols,nWL)
            #self.DeltaStackReshaped: reshaped stack to (rows*cols, nWL) which can then be clusterized with KMeans
            #self.dim1, self.dim2, self.dim3: rows, cols, nWL, for easy retrieval/later use in other functions
        self.loadPsiMaps() #same as loadDeltaMaps but for psi maps. The dimensions are the same, so they are not instantiated again       
        #Instantiates:
            #self.PsiStack
            #self.PsiStackReshaped
        
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
        self.indices = np.arange(len(self.WLarray))
        self.WLdict = dict(zip(self.indices, self.WLarray))
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
        
        self.n_clustersList = np.arange(k)
        
        kmeansDelta = KMeans(n_clusters = k, random_state = 0).fit(self.DeltaStackReshaped)
        
        segmentedDelta = kmeansDelta.cluster_centers_[kmeansDelta.labels_]
        
        segmentedDeltaStack = segmentedDelta.reshape(self.dim1, self.dim2, self.dim3)
        
        self.segmentedDelta = segmentedDelta
        self.segmentedDeltaStack = segmentedDeltaStack
        self.Dcluster_centers_ = kmeansDelta.cluster_centers_
        self.Dcluster_labels_ = kmeansDelta.labels_
        
        kmeansPsi = KMeans(n_clusters = k, random_state = 0).fit(self.PsiStackReshaped)
        
        segmentedPsi = kmeansPsi.cluster_centers_[kmeansPsi.labels_]
        
        segmentedPsiStack = segmentedPsi.reshape(self.dim1, self.dim2, self.dim3)
        
        self.segmentedPsi = segmentedPsi
        self.segmentedPsiStack = segmentedPsiStack
        self.Pcluster_centers_ = kmeansPsi.cluster_centers_
        self.Pcluster_labels_ = kmeansPsi.labels_
    
    def clustershot(self):
        self.firstSegmentedDeltamap = self.segmentedDeltaStack[:,:,0]
        self.firstSegmentedPsimap = self.segmentedPsiStack[:,:,0] #not used at all? remove?
        #first segmented Deltamap is used to identify position of clustered pixels. 
        #It must be tested how that overlaps in psi maps, as chances are that len(pval) is then > 1
        
        all_DeltaShots = []
        all_PsiShots = []
        
        for cluster_idx in self.n_clustersList:
            
            C_ = np.unique(self.firstSegmentedDeltamap)[cluster_idx] #select one value from unique values in first map
            C_ys, C_xs = np.where(self.firstSegmentedDeltamap==C_) #identify position of all pixels with that value in the map
        
            C_Deltapixelshot = []
            C_Psipixelshot = []

            for wl in self.indices:
                Dpxval = np.unique(self.segmentedDeltaStack[C_ys,C_xs,wl])
                C_Deltapixelshot.append(Dpxval[0]) # the [0] here is just to append the float and not the array [float]
                #raise error if len(pxval)>1??
                Ppxval = np.unique(self.segmentedPsiStack[C_ys,C_xs,wl])
                C_Psipixelshot.append(Ppxval[0])
        
            all_DeltaShots.append(C_Deltapixelshot)
            all_PsiShots.append(C_Psipixelshot)
        self.all_DeltaShots = all_DeltaShots
        self.all_PsiShots = all_PsiShots
    
    def pickonefromstack(self, imstack, idxSelector = 0):
        #probably unnecessary, as it can be replaced by imstack[:,:,idxSelector]
        selected = np.dsplit(imstack, imstack.shape[2])[idxSelector]
        
        return selected
    
    def plotDeltaPsi(self, idxSelector = 0):
        
        idx = self.indices[idxSelector]
        imDelta = self.pickonefromstack(self.DeltaStack, idx)
        imPsi = self.pickonefromstack(self.PsiStack, idx)
        
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
        
        idx = self.indices[idxSelector]
        imDelta = self.pickonefromstack(self.segmentedDeltaStack, idx)
        imPsi = self.pickonefromstack(self.segmentedPsiStack, idx)
        
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