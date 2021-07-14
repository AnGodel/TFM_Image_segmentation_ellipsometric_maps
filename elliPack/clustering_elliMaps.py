# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 11:02:14 2021

@author: ago
"""

import glob
import os
import time
import numpy as np
from nanofilm.ndimage import imread
import elliPack.astroclean as at
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import matplotlib.pyplot as plt
import pandas as pd


class lambdaVarEllimaps:
    
    def __init__(self, path = None):
        
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
        self.getdatFile()  
        self.readdatFile()  
        self.loadAllMaps()  
        
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
        start = time.perf_counter()
        print('Loading and preprocessing maps...')
        AllMaps = list(map(at.loadmap_T_astroclean, self.AllFileList))
        self.AllShuffledStack = np.dstack(AllMaps)
        self.dim1all, self.dim2all, self.dim3all = self.AllShuffledStack.shape
        self.AllShuffledStackReshaped = self.AllShuffledStack.reshape(self.dim1all*self.dim2all, self.dim3all)
        self.AllIndices = np.arange(self.dim3all)
        self.DeltaIndices = [x for x in self.AllIndices if x%2 == 0]
        self.PsiIndices = [x + 1 for x in self.AllIndices if x%2 == 0]
        
        stop = time.perf_counter()
        print(f'{self.dim3all} maps loaded in {stop - start:0.4f} seconds')
    
    def getEstimation(self, k=(2,11), metric = 'distortion'):
        start = time.perf_counter()
        print('Getting estimation and metrics with Distortion method')
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.AllShuffledStackReshaped)
        
        basefilename = os.path.basename(self.datFile).split('.')[0]
        distortionFigPath = os.path.join(self.path, basefilename + '_distortionEstimation.png')
        
        visualizer.show(outpath=distortionFigPath)
        stop = time.perf_counter()
        print(f'Finished estimation in {stop - start:0.4f} seconds')
        return visualizer
    
    #Having the two estimator visualizers in the same function makes the second estimator fail, somehow

    
    def getEstimation2(self, k=(2,11), metric = 'calinski_harabasz'):
        start = time.perf_counter()
        print('Getting estimation and metrics with Calinski-Harabasz method')
        model = KMeans(random_state=0)
        
        visualizer = KElbowVisualizer(model, 
                                      k=k,
                                      metric = metric)
        visualizer.fit(self.AllShuffledStackReshaped)
        
        basefilename = os.path.basename(self.datFile).split('.')[0]
        calinskiFigPath = os.path.join(self.path, basefilename + '_calinskiEstimation.jpg')
        
        visualizer.show(outpath=calinskiFigPath)
        stop = time.perf_counter()
        print(f'Finished estimation in {stop - start:0.4f} seconds')
        return visualizer
        
    def clusterize(self, k = 5):
        start = time.perf_counter()
        print('Segmenting maps into {} clusters'.format(k))
        
        self.cluster_list = np.arange(k) # List to serve as index for the clusters
        
        kmeans = KMeans(n_clusters = k, random_state = 0).fit(self.AllShuffledStackReshaped)
        
        segmented = kmeans.cluster_centers_[kmeans.labels_]
        
        segmentedShuffledStack = segmented.reshape(self.dim1all, self.dim2all, self.dim3all)
        
        self.segmented = segmented
        self.segmentedShuffledStack = segmentedShuffledStack
        self.cluster_centers_ = kmeans.cluster_centers_
        self.cluster_labels_ = kmeans.labels_
        print('Extracting numerical values for each cluster along map stacks...')
        self.clustershot()
        stop = time.perf_counter()
        print(f'Finished segmentation in {stop - start:0.4f} seconds')
        
    def clustershot(self):
        self.firstSegmentedDeltamap = self.segmentedShuffledStack[:,:,0]
        #  first segmented Deltamap is used to identify position of clustered pixels. 
        #  It could be any map, as here in the shuffled stack all clusters will always overlap along the 3rd axis        
        
        delta_shot = [] #  each row is a  cluster shot of delta values
        psi_shot = [] #  each row is a cluster shot of psi values
        cluster_coordinates = []
        for cluster_idx in self.cluster_list:
            
            C_ = np.unique(self.firstSegmentedDeltamap)[cluster_idx] #  selects one value from unique values in first map
            C_ys, C_xs = np.where(self.firstSegmentedDeltamap == C_) #  identifies position of all pixels with that value in the map
            cluster_coordinates.append((C_ys, C_xs))
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
        self.cluster_coordinates = cluster_coordinates
    
    def plotDeltaPsi(self, idxSelector = 0):
        
        imDelta = self.AllShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        imPsi = self.AllShuffledStack[:,:,self.PsiIndices[idxSelector]]
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(25,12))
        fig.tight_layout()
        
        
        ax1.clear
        arrR1 = ax1.imshow(imDelta, cmap = 'gray')
        ax1.set_title('Delta', fontsize='xx-large')
        ax1.grid(b=None)
        ax1.set_axis_off()
        fig.colorbar(arrR1, 
                     ax=ax1, 
                     shrink=0.5, 
                     location='left',
                     pad=0.048)
        fig.suptitle('Map index: {} -- Wavelength: {} nm'.format(idxSelector, 
                                                                 self.WLdict[idxSelector]), 
                     y=0.90,
                     fontsize='xx-large')
        ax2.clear
        arrR2 = ax2.imshow(imPsi, cmap = 'gray')
        ax2.grid(b=None)
        ax2.set_axis_off()
        ax2.set_title('Psi', fontsize='xx-large')
        fig.colorbar(arrR2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')
        
        return fig
    
    def plotSegmentedDeltaPsi(self, idxSelector = 0):
        
        imDelta = self.segmentedShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        imPsi = self.segmentedShuffledStack[:,:,self.PsiIndices[idxSelector]]
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(25,12))
        fig.tight_layout()
        
        ax1.clear
        arrC1 = ax1.imshow(imDelta, cmap = 'viridis')
        ax1.set_title('Delta', fontsize='xx-large')
        ax1.grid(b=None)
        ax1.set_axis_off()
        fig.colorbar(arrC1, 
                     ax=ax1, 
                     shrink=0.5, 
                     location='left',
                     pad=0.048)
        fig.suptitle('Map index: {} -- Wavelength: {} nm'.format(idxSelector, self.WLdict[idxSelector]), 
                     y=0.9,
                     fontsize='xx-large')
        ax2.clear
        arrC2 = ax2.imshow(imPsi, cmap = 'viridis')
        ax2.grid(b=None)
        ax2.set_axis_off()
        ax2.set_title('Psi', fontsize='xx-large')
        fig.colorbar(arrC2, 
                     ax=ax2, 
                     shrink=0.5, 
                     location='right')
        
        return fig
    
    def plotClusterOverMaps(self, C_Selector = 0, idxSelector = 0):
        
        Dmap = self.AllShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        Pmap = self.AllShuffledStack[:,:,self.PsiIndices[idxSelector]]
        DSegmap = self.segmentedShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        PSegmap = self.segmentedShuffledStack[:,:,self.PsiIndices[idxSelector]]
        
        C_ys, C_xs = self.cluster_coordinates[C_Selector]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2,ncols=2, figsize=(23,15))
        fig.tight_layout(pad=3)
        
        plt.ylim(ymin=self.dim1all, ymax=0)
        plt.xlim(xmin=0, xmax=self.dim2all)
        ax1.clear
        ax1.imshow(Dmap, cmap='gray')
        ax1.set_title('Raw Delta map', fontsize='xx-large')
        ax1.scatter(C_xs, C_ys, s=5, color='pink')
        ax1.grid(False)
        ax1.set_axis_off()
        
        ax2.clear
        ax2.imshow(Pmap, cmap='gray')
        ax2.set_title('Raw Psi map', fontsize='xx-large')
        ax2.scatter(C_xs, C_ys, s=5, color='pink')
        ax2.grid(False)
        ax2.set_axis_off()
        fig.suptitle('Cluster {} at Wavelength {}, {} nm'.format(C_Selector, 
                                                                 idxSelector,
                                                                 self.WLdict[idxSelector]),
                    y = 1.02,
                    fontsize='xx-large')
        ax3.clear
        ax3.grid(False)
        ax3.set_axis_off()
        ax3.imshow(DSegmap, cmap='viridis')
        ax3.set_title('Segmented Delta map', fontsize='xx-large')
        ax3.scatter(C_xs, C_ys, s=5, color='pink')
        
        ax4.clear
        ax4.imshow(PSegmap, cmap='viridis')
        ax4.set_title('Segmented Psi map', fontsize='xx-large')
        ax4.scatter(C_xs, C_ys, s=5, color='pink')
        ax4.grid(False)
        ax4.set_axis_off()
        
        return fig
    
    def plotOneShot(self, C_Selector = 0):
        
        idx = self.cluster_list[C_Selector]
        Deltas = self.delta_shot[C_Selector]
        Psis = self.psi_shot[C_Selector]
        WL = self.WLarray
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        fig.tight_layout()
        
        ax1.clear
        ax1.plot(self.WLarray, Deltas, color = 'red')
        ax1.set_title('Delta')
        fig.suptitle('Cluster index: {}'.format(C_Selector), y=1.05)
        ax2.clear
        ax2.plot(self.WLarray, Psis, color = 'blue')
        ax2.set_title('Psi')
        
        return fig

    def plotAllShots(self, C_Selector = 0):
            
        idx = self.cluster_list[C_Selector]
        Deltas = self.delta_shot
        Psis = self.psi_shot
        WL = self.WLarray
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,10))
        fig.tight_layout(pad=4)
        
        ax1.clear
        ax1.scatter(self.WLarray, Deltas[C_Selector], color='red')
        ax1.set_title('Delta', fontsize='xx-large')
        ax1.set_xticklabels(self.WLarray,
                            fontsize='xx-large')
        ax1.set_yticklabels(Deltas[C_Selector],
                            fontsize='xx-large')
        ax1.set_xlabel('Wavelength (nm)', fontsize='xx-large')
        ax1.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        ax1.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        fig.suptitle('Cluster index: {}'.format(C_Selector),
                     y=1.05,
                     fontsize='xx-large')
        ax2.clear
        ax2.scatter(self.WLarray, Psis[C_Selector], color='blue')
        ax2.set_title('Psi', fontsize='xx-large')
        ax2.set_xticklabels(self.WLarray,
                            fontsize='xx-large')
        ax2.set_yticklabels(Psis[C_Selector],
                            fontsize='xx-large')
        ax2.set_xlabel('Wavelength (nm)', fontsize='xx-large')
        ax2.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        ax2.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        for C_Selector in self.cluster_list:
            ax1.plot(self.WLarray, Deltas[C_Selector], alpha=0.7)
            ax2.plot(self.WLarray, Psis[C_Selector], alpha=0.7)
        
        return fig
    
    def plotBarSegmentedMap(self, C_Selector = 0, idxSelector = 0):
        Dmap = self.segmentedShuffledStack[:,:,self.DeltaIndices[idxSelector]]
        Pmap = self.segmentedShuffledStack[:,:,self.PsiIndices[idxSelector]]

        D_Cvalues, D_Ccounts = np.unique(Dmap, return_counts = True)
        P_Cvalues, P_Ccounts = np.unique(Pmap, return_counts = True)

        D_varwidth = (D_Cvalues.max() - D_Cvalues.min())/20
        P_varwidth = (P_Cvalues.max() - P_Cvalues.min())/20
        SelectedDval = self.delta_shot[C_Selector][self.WLIndices[idxSelector]]
        SelectedPVal = self.psi_shot[C_Selector][self.WLIndices[idxSelector]]

        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,10))
        fig.tight_layout(pad=4)

        ax1.clear
        ax1.bar(D_Cvalues, D_Ccounts, 
                edgecolor='green',
                linewidth=2.5, 
                width=D_varwidth,
                color='red')
        ax1.axvline(x=SelectedDval,
                    color='black',
                    label='cluster {} at {}'.format(C_Selector, SelectedDval))
        ax1.legend(fontsize='xx-large')
        ax1.set_title('Delta clusters values and their pixel counts', fontsize='xx-large')
        ax1.set_xticklabels(D_Cvalues,
                            fontsize='xx-large')
        ax1.xaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        ax1.set_yticklabels(D_Ccounts,
                            fontsize='xx-large')
        ax1.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        fig.suptitle('Map index: {} -- Wavelength: {} nm'.format(idxSelector,
                                                                 self.WLdict[idxSelector]
                                                                 ), 
                     y = 1.05,
                     fontsize='xx-large')
        ax2.clear
        ax2.bar(P_Cvalues, P_Ccounts, 
                edgecolor='green', 
                linewidth=2.5, 
                width=P_varwidth,
                color='blue')
        ax2.axvline(x=SelectedPVal, 
                    color='black', 
                    label='cluster {} at {}'.format(C_Selector, SelectedPVal))
        ax2.legend(fontsize='xx-large')
        ax2.set_title('Psi clusters values and their pixel counts', fontsize='xx-large')
        ax2.set_xticklabels(P_Cvalues,
                            fontsize='xx-large')
        ax2.xaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        ax2.set_yticklabels(P_Ccounts,
                            fontsize='xx-large')
        ax2.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        
        return fig
    
    def plotClusterRawValues(self, C_Selector = 0, idxSelector = 0):
        
        C_ys, C_xs = self.cluster_coordinates[C_Selector]
        Dmap = self.AllShuffledStack[C_ys,C_xs,self.DeltaIndices[idxSelector]]
        Pmap = self.AllShuffledStack[C_ys,C_xs,self.PsiIndices[idxSelector]]
        bins = int(len(Dmap)/10)
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,10))
        fig.tight_layout(pad=4)

        ax1.clear
        ax1.hist(Dmap, 
                 bins = bins,
                 color='red')
        ax1.set_title('Not segmented Delta values on cluster {}'.format(C_Selector), 
                      fontsize='xx-large')
        ax1.set_xticklabels(Dmap,
                            fontsize='xx-large')
        ax1.xaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        ax1.set_yticklabels(np.histogram(Dmap)[0],
                            fontsize='xx-large')
        ax1.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        fig.suptitle('Map index: {} -- Wavelength: {} nm'.format(idxSelector,
                                                                 self.WLdict[idxSelector]
                                                                 ), 
                     y = 1.05,
                     fontsize='xx-large')
        ax2.clear
        ax2.hist(Pmap, 
                 bins = bins,
                 color='blue')
        ax2.set_title('Not segmented Psi values on cluster {}'.format(C_Selector), 
                      fontsize='xx-large')
        ax2.set_xticklabels(Pmap, fontsize='xx-large')
        ax2.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        ax2.set_yticklabels(np.histogram(Pmap)[0],
                            fontsize='xx-large')
        ax2.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        
        return fig
        
    def createDFfromClustershot(self):
        
        df = pd.DataFrame(list(zip(self.WLIndices,self.WLarray)))
        df.columns = ['WL_idx','WL']
        for i, inlist in enumerate(self.delta_shot):
            columnname = 'delta_cluster_{}'.format(i)
            Dcolumn = pd.Series(inlist, name=columnname)
            df = df.join(Dcolumn)
        for i, inlist in enumerate(self.psi_shot):
            columnname = 'psi_cluster_{}'.format(i)
            Pcolumn = pd.Series(inlist, name=columnname)
            df = df.join(Pcolumn)
            
        self.DFshot = df
    
    def createDFcoordinates(self):
        
        df = pd.DataFrame(np.arange(len(self.cluster_coordinates[0][0])))
        df.columns = ['pixel_idx']
        #if df is empty it is not possible to add Series as columns using join
        for i, tupla in enumerate(self.cluster_coordinates):
            colItem0 = 'Cys_cluster_{}'.format(i)
            colItem1 = 'Cxs_cluster_{}'.format(i)
            Ycolumn = pd.Series(tupla[0],name=colItem0)
            df = df.join(Ycolumn)
            Xcolumn = pd.Series(tupla[1],name=colItem1)
            df = df.join(Xcolumn)
        
        self.DFcoordinates = df
        
    def exportDFs(self):
        
        self.createDFcoordinates()
        self.createDFfromClustershot()
        
        basefilename = os.path.basename(self.datFile).split('.')[0]
        coordFile = os.path.join(self.path, basefilename + '_coordinates.dat')
        clustershotFile = os.path.join(self.path, basefilename + '_clustershot.dat')
        
        self.DFcoordinates.to_csv(coordFile)
        self.DFshot.to_csv(clustershotFile)