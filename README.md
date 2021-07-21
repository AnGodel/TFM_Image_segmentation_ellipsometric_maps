# TFM_Image_segmentation_ellipsometric_maps

Repository containing my project for the master's degree in Data Science from KSchool. 

## Overview

The project consist in aplying ML image segmentation techniques to ellipsometric maps. This micro-maps are images with particular characteristics, obtained when applying the imaging ellipsometry technique for the analysis of ultra-thin layers of materials. The goal is to facilitate the object and zone detection in a set of maps with varying contrast, so that the user of the ellipsometer can decide which zones should be forwarded to the model-fitting software. This tool can be used to get a coarse fit of a whole map fast, applicable to all kind of samples and map sizes, with minimal intervention from the user.
More detailed information about the nature of the data, the goals of the project and the used methodology can be found in the memory PDF file. 
The project has been developed using only python scripts. A python package containing all the modules and classes is the base for a front-end built with streamlit. The front-end will provide all the tools and graphs for the user to extract meaningful information from the data. 

## Install working environment

- Make sure you have [Anaconda](https://www.anaconda.com/products/individual) (or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)) installed in your system. 

- Open a terminal and activate the base conda environment. More information on how to work with conda environments [here](https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/aio/index.html).

- In the terminal, navigate to the folder where the repo is located:

  `$ cd <YOURPATHTOREPO>/TFM_Image_segmentation_ellipsometric_maps`

- Build the conda environment using the provided .yml file and activate it:

  `$ conda env create --file ellimaps_env.yml`

  `$ conda activate ellimaps`

- Manually install the nanofilm_package:

  `$ cd nanofilm_package_installer`

  `$ pip install nanofilm-ep4-0.7.10.tar.gz`

## Run streamlit app

- Go back to the main repo folder and run the streamlit app:

  `$ cd ..`

  `$ streamlit run streamlit_ElliMaps_segmentation.py`



<img src="https://drive.google.com/uc?export=view&id=1bRoh65NIkkSG1NidMy2r-X3D04rn5Yqn" style="zoom: 60%;"/>


## Download ellipsometric map sets 

A small dataset for a quick demo has been included in the repository, in the folder *data_example*. 
More datasets to use the tool can be downloaded from here:

- https://www.dropbox.com/s/7s3kiadxt49fdwq/example_elli-maps_forTFM.zip?dl=0 or alternatively
- https://drive.google.com/file/d/1OvOFiQhxXsxIW5k2YObsLlB-FJMka9qB/view?usp=sharing

## Workflow

After download,  unzip the file in a local folder of your computer. Copy a folder path, load it to the streamlit app and start playing with the data.



<img src="https://drive.google.com/uc?export=view&id=141VeHChZ-SGohv2sHiouNANmNaTK0_1V" style="zoom: 40%;"/>



The folder is instantiated and the dataset it contains pre-processed. A number of tools for the data exploration and segmentation is offered in the side panel. From here on, the suggested workflow is:

1. Use the estimator tool to get the optimal number of clusters for the segmentation. More detailed information about how this estimators have been implemented can be found in the memory. Once you decide the number of clusters you are going to use, <u>set the estimator selector box back to **None** before proceeding to the next step</u>. Otherwise the estimation will re-run each time other parameters are set, slowing down the rest of the data visualizations.

<img src="https://drive.google.com/uc?export=view&id=1ARfjW-_GIwsQAdaJS_Xk3FQyiQHZ2GEQ" style="zoom: 40%;"/> <img src="https://drive.google.com/uc?export=view&id=1RHUP7iFunOC7hhzQXPmPWFRdZ4b1By5-" style="zoom: 50%;"/>

2. Set the desired number of clusters and click on *Run Segmentation* button. The background scripts will do the magic, segmenting your dataset and creating the clustershot data which can be visualized in the graphs below.



<img src="https://drive.google.com/uc?export=view&id=108TxW8LKekzjdTCEBoRNKrdN0YeubROQ" style="zoom: 60%;"/> 



3. Select the type of map graph and the additional info plots to be displayed. Then use the sliders to explore the dataset selecting the wavelength and cluster indexes. 



<img src="https://drive.google.com/uc?export=view&id=1p81kDKi1ueYyNtAQfE35AfmOoG4VZgrP" style="zoom: 60%;"/><img src="https://drive.google.com/uc?export=view&id=1X277AVvtRKhEsg1JglyAPMAlmroQVn95" style="zoom: 40%;"/><img src="https://drive.google.com/uc?export=view&id=1gn67ERqYUevTxua7-eDxrEzX9yjB8tDx" style="zoom: 30%;"/>



4. After data exploration you can decide whether you want to try refining the segmentation increasing or decreasing the number of clusters or export the clustershot data to .dat files using the *Export clustershot data* button. In the first case go back to step 2, enter a new number of clusters and run the segmentation again. 
