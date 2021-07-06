# Methods at '__init__' when instantiating the class

- self.getdatFile()   

  will find the .ds.dat file in the folder. 
  Instantiates 

  - self.datFile

- self.readdatFile()  

  reads the .dat file using pandas, instantiating:
     - self.datatable: no further use
     - self.WLarray: numpy array with a list of wavelengths used in the measurement
     - self.WLIndices: list of indices of WLarray. Used later for the map index selector
     - self.WLdict: dict with indices as keys and WL as values. For later use as reference in plots
     - self.nWL: just for easy retrieving the number of WL (number of maps) in the measurement
     - self.DeltaFileList: a list of file paths of the delta maps for the measurement. 
     - self.PsiFileList: same, but for psi maps
     - self.AllFileList: a list of file paths alternating delta,psi files. The load function will iterate over them to create a stack of "shuffled" readable images (numpy arrays)

- self.loadAllMaps() 
  - transforms raw delta maps into readable images. Also does some pre-processing, including smoothing and NaN removal by convolution of a 9x9 kernel
  - The NaN removal will fail if there are NaN areas larger than the kernel in the raw map
  - Instantiates:
    - self.AllShuffledStack: the stack of shuffled maps
    - self.AllShuffledStackReshaped: the reshaped stack ready for being passed to KMeans algorithm
    - self.dim1all, self.dim2all, self.dim3all: dimensions of the stack, being dim3 nWL*2
    - self.AllIndices: a list (np.arange) of all indices in AllShuffledStack. From 0 to dim3all-1
    - self.DeltaIndices: all even indices in self.AllIndices
    - self.PsiIndices: all odd indices in self.AllIndices

# Clusterize method: the key point of the class

- self.clusterize()  -- runs first sementation with k=5 automatically -- REMOVE FROM INIT FOR CHACHING AT STREAMLIT???
  - Performs segmentation on the stack of maps. Instatiates:
  - self.cluster_list: np.arange(k). List to use to select the C_Selector
  - self.segmented
  - self.segmentedShuffledStack
  - self.cluster_centers_
  - self.cluster_labels_
  - launches self.clustershot()
- self.clustershot() -- extract the coordinates of the pixels of each cluster and the numerical data (delta and psi) from each map along the third axis of self.segmentedShuffledStack. Instantiates:
  - self.firstSegmentedDeltamap -- reference used to identify position of clustered pixels. Any map could be used. First of the stack chosen randomly
  - self.delta_shot -- each row is a list of delta values from one cluster
  - self.psi_shot -- each row is a list of psi values from one cluster
  - self.cluster_coordinates -- list of tuples (Cys, Cxs), each tuple contains the coordinates for one cluster pixels

​	

# Other methods of the class

#### Estimators for the number of clusters and the segmentation processing time

- self.getEstimation()

- self.getEstimation2()

  These are the estimators from yellowbrick library. They return an internal class object called "visualizer", which cannot be displayed in streamlit. 

  They need to be modified in order to export the visualizer as an image in .png format, which can be then displayed in streamlit

#### Image plotters

- self.plotDeltaPsi(idxSelector)
- self.plotSegmentedDeltaPsi(idxSelector)
- self.plotClusterOverMaps(C_Selector, idxSelector)

#### Numeric data plotters

- self.plotOneShot(C_Selector)
- self.plotAllShots(C_Selector)
- self.plotBarSegmentedMap(C_Selector, idxSelector)

#### Numeric data collection and export

- self.createDFfromClustershot()
- self.createDFcoordinates()
- self.exportDFs()