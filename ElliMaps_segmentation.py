# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 11:10:45 2021

@author: Antonio
"""

import streamlit as st
import numpy as np
import pandas as pd
from clusteringDeltaPsi_shuffled import lambdaVarEllimaps as lve
import time

st.title('Ellipsometric Maps Segmentation Tool')

folderinput = st.text_input('Please enter a path to folder containing the ellipsometric maps:')

if folderinput:

    currentExp = lve('F:\example_elli-maps_forTFM\Garching-wednesday-hBN__smallset-withNaNs-goodforquicktest')
    
st.markdown('Estimation with Distortion method')
st.write(currentExp.getEstimation())

st.markdown('Segmented maps:')
    
st.write(currentExp.plotSegmentedDeltaPsi(idxSelector=4))