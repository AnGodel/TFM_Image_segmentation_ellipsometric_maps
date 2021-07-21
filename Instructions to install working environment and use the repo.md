# Instructions

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

- Go back to the main repo folder and run the streamlit app:

  `$ cd ..`

  `$ streamlit run streamlit_ElliMaps_segmentation.py`


## Download ellipsometric map sets 

Download some ellipsometric maps and unzip them locally:

- https://www.dropbox.com/s/7s3kiadxt49fdwq/example_elli-maps_forTFM.zip?dl=0 or alternatively
- https://drive.google.com/file/d/1OvOFiQhxXsxIW5k2YObsLlB-FJMka9qB/view?usp=sharing

Copy a folder path, load it to the streamlit app and start playing with the data.