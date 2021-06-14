# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 11:02:14 2021

@author: ago
"""

import glob
import numpy as np
from nanofilm.ndimage import imread
import elliPack.astroclean as at

class lambdaVarEllimaps:
    
    def __init__(self, path = None):
        if path is None:
            raise ValueError('Please enter a valid path to folder containing maps from lambda variation measurement')
        else:
            self.path = path
        self.getFiles()

    def getFiles(self):
        
        self.all_files = glob.glob(self.path + '/*.png')
        
        return self.all_files
    
    def loadAllMaps(self):
        
        stack = list(map(at.loadmap_astroclean, self.all_files))
        self.all_maps = np.dstack(stack)
        
        return self.all_maps
        
