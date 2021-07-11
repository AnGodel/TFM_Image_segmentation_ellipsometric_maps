# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 11:10:45 2021

@author: Antonio
"""

import streamlit as st
from streamlit_yellowbrick import st_yellowbrick
import numpy as np
import pandas as pd
from yellowbrick.cluster.elbow import kelbow_visualizer, KElbowVisualizer
from sklearn.cluster import KMeans
from clusteringDeltaPsi_shuffled import lambdaVarEllimaps as lve
import os

st.title('Ellipsometric Maps Segmentation Tool')

folderinput = st.text_input('Please enter a path to folder containing the ellipsometric maps:')

if folderinput:
    
    @st.cache(allow_output_mutation=True)
    def instantiate(folder):
        Exp = lve(folder)
        WL_max = int(Exp.WLIndices[-1])
        return Exp, WL_max
    currentExp, WL_max = instantiate(folderinput) 
    
    #Box to select estimation method
    estimator = st.sidebar.selectbox('Select estimation to display',
                             options=(None, 'Distortion', 'Calinski-Harabasz'))
    
    
    if estimator == 'Distortion':
        st_yellowbrick(currentExp.getEstimation())
    elif estimator == 'Calinski-Harabasz':
        st_yellowbrick(currentExp.getEstimation2())
    else:
        pass
    
    
    #@st.cache(allow_output_mutation=True)
    def runSegmentation(exp, k):
        expClusterized = exp.clusterize(k)
        return expClusterized
    k = 5
    if st.sidebar.button('Run segmentation', on_click=runSegmentation(currentExp, k)):
        runSegmentation(currentExp, k)
    #Slider to select the number of clusters for the segmentation (k in clusterize())
        k = st.sidebar.number_input('Select the number of clusters for the segmentation of your maps:',
                      min_value=2,
                      max_value=15,
                      step=1,
                      value=5)
    
    #Slider to select the cluster idx to be displayed in the plots
    C_max = int(k - 1)
    C_Selector = st.sidebar.slider('Select the cluster to display',
                      min_value=0,
                      max_value=C_max,
                      value=0)
    #Slider to select the WL idx to be displayed in the plots
    if WL_max:
        idxSelector = st.sidebar.slider('Select the WL idx to display',
                                        min_value=0,
                                        max_value=WL_max,
                                        value=0)
    
    #Box to select type of plot to be displayed
    plotdisplaytype = st.sidebar.selectbox('Select the plot to be displayed',
                                           options=('Raw Delta-Psi Maps',
                                                    'Segmented Delta-Psi Maps',
                                                    'Cluster over Raw and Segmented Maps'))
    
    
    if plotdisplaytype == 'Raw Delta-Psi Maps':
        st.write(currentExp.plotDeltaPsi(idxSelector))
    elif plotdisplaytype == 'Segmented Delta-Psi Maps':
        st.write(currentExp.plotSegmentedDeltaPsi(idxSelector))
    elif plotdisplaytype == 'Cluster over Raw and Segmented Maps':
        st.write(currentExp.plotClusterOverMaps(C_Selector, idxSelector))
    
    #Button to display the clusters bar plot
    if st.sidebar.checkbox('Show cluster bar plot'):
       st.write(currentExp.plotBarSegmentedMap(C_Selector, idxSelector))
    else:
        pass
    
    #Button to display the clustershot Delta-Psi curves
    if st.sidebar.checkbox('Show Delta-Psi curves from clustershot'):
        st.write(currentExp.plotAllShots(C_Selector))
    else:
        pass    
else:
    st.write('Waiting for folder path...')
    
