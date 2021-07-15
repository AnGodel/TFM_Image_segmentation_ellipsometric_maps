# Instructions to install working environment

- Make sure you have [Anaconda](https://www.anaconda.com/products/individual) (or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)) installed in your system. 

- Download or clone the repo from GitHub and place it in a local folder in your computer.

- Open a terminal and activate the base conda environment.

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

- Download some ellipsometric maps and unzip them locally:
  - (link or links to file downloads in dropbox)