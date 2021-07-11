# Working with stacked images

## About naming

The maps naming convention is different depending on the grabbing method:

- Maps obtained with traditional nulling method will be named with just a rolling number at the end (xxx_001.png, xxx_002.png, etc)
  - Not possible to distinguish delta maps from psi maps just from the file name.
  - Typically the even numbers will be delta maps and the odd numbers will be psi maps.

- Maps obtained with RCE method will be named as xxx_Delta_001.png, xxx_Psi_001.png, xxx_Delta_002.png, xxx_Psi_002.png
  - Much easier to handle, but the preprocessing of the images must be different.
    - this might be not so true after all, since the dstack will be divided in the delta and psi "blocks", which might need to be then "shuffled" to get a stack similar to what we get in the maps obtained with traditional nulling method. I need to test the results of the clustering in the "block" stack and see how valid it can be compared to the already tested "shuffled" mode.

THIS HAS BEEN HANDLED BY READING THE .dat FILE TO RETRIEVE WHICH FILES ARE DELTA AND WHICH FILES ARE PSI, INDEPENDENTLY OF THE MEASUREMENT TYPE.

## To-Do

- [x] ~~try segmentation on a stack of delta and psi maps combined~~
  - works just as fine as separating delta and psi maps manually
  - execution time for a stack of 6 maps, including two metrics and k estimation with yellowbrick, is about 1 minute. 
  
- [x] ~~try to improve the k estimation decreasing max number of clusters in the estimator~~
  - this does not have an effect with the distortion method (k still 4), but makes the Calinski_harabasz fail to find an optimum k. Keeping the max number of cluster at at least 10 give us the window of k 4 to 7
  - the silhouette method fails when used with a stack of maps, or at least it is too slow to be used. Had to interrupt the python kernel with every try.
  
- [x] ~~try segmentation after combining delta and psi maps in one using the math provided by MD~~
  - ~~this might be interesting in order to reduce the computing time of the clustering but will have other disadvantages:~~
    - ~~because of the math operation, the pixel of the combined map will have small values, in the range -1,1, which will likely need to be rescaled for proper plotting~~
    - ~~with or without rescaling, the labels obtained by this segmentation can't be directly used:~~
      - ~~of this combined map will be useful only for finding the shapes and contours of the clusters and export a mask to be applied in the original maps to extract the numeric values~~
      - ~~another option would by applying reversed math to get delta and psi values from the labels of the segmentation of C and S maps~~
  
- [x] ~~test the computing time on small and large stacks for both the estimation with yellowbrick visualizers and the segmentation itself~~
  - with sets of 22 and 63 maps it goes relatively fast. But the test with a set of 140 maps took about 10 minutes to just load all files into the class. 
  - further testing is required in order to check whether the required time icreases exponentially with the number of maps or the tested large dataset was containing larger images with more pixels.
    - if this is the case, it will worth a try the resizing of the images during preprocessing, as described [here](https://datascience.stackexchange.com/questions/42125/rgb-image-segmentation-using-clustering)
  
- [x] ~~try reading the ds.dat file to catch indexes of delta and psi maps? would this be necessary at all?~~
  - ~~probably it will work just fine considering that:~~
    - ~~in traditional nulling maps the maps are identified by only a rolling number which starts with 001, being the first delta always the 001 and the first psi always the 002. That means that in our map stacsk, the deltas will have even idexes (0, 2, 4...) and psis will have odd idexes (1,3,5...)~~
    - ~~in RCE the files will be identified with either "Delta" or "Psi" but there will be only one rolling number for each pair. We need to see how this will affect the script but for now we will focus in the traditional nulling maps.~~
  - Done. Now the class has an attribute which is an array the wavelengths of the experiment. 
    - ~~Error handling included: an error message will raise in case the number of wavelengths from the .dat file does not match the number of maps in the folder or in case there is more than one .dat file in the folder~~ Obsolete. Now error raises in case there is more than one .dat file in the folder.
  
- [x] ~~extract the delta and psi vs. wavelength from the segmented stack. This will be one of the final goals of the project, since those data will be already "fittable" with Accurion's model software to extract more accurate thickness map (in a single map) than the current interpolation mode.~~ 
  - Done
  
- [ ] <u>Optional, if there is time:</u> apply canny edge detection or any other image method to extract the contours of the map segments.
  - the goal here is to somehow apply a "mask" in the original map stack before segmenting, so that an  area if interest can be "cropped" and selected for a traditional pixel by pixel fitting. 
    - This is something that can be done manually with DataStudio, which is quite tedious.
  
- [x] Plotting To-Do´s:
  - [x] include bar plot of the segmented maps, as in the test notebook. It gives a fast visualization of how much the cluster values are overlapping, which might be an indication that the clustering would work also with less clusters.
  - [x] include plot of selected cluster overlapped with plot of standard map (imshow())
  - [x] correct position of fig title in cluster shot
  - [x] ~~include legend in cluster shot plot~~ Not really necessary, as cluster index is already shown in fig title.
  - [x] change map plotting functions to remove axis labels and make them more attractive in streamlit
  - [x] change size of bar plots
  - [x] change size of clustershot plots
  - [x] add x-axis label to clustershot plot to display 'Wavelength'
  
- [x] ~~empaquetar el modo "manual" de sacar el "cluster pixel shot" encontrado en el notebook usando np.where and np.unique~~

- [x] ~~IMPORTANT: check if there are more than one psi values retrieved when doing the cluster shot taking the Cy, Cx positions from the first delta map. Probably good to double-check this also in delta maps and using other example datasets.~~

  - ~~OK... As expected, there are more than one value in the Psi maps when doing the cluster shot with the coordinates of a Delta map. Funny thing is that the values for the Delta shot are single values. Which means I just need to figure out how to match the (Delta,Psi) values for each cluster and then run the psi shot with coordinates from the first Psi map. Maybe running the clustering in a "shuffled" Delta-Psi stack would solve this problem?~~

    - INDEED! I had to figure out how to "shuffle" the delta and psi maps in the right order from the file lists given by the .dat file. But from there on, everything was easier. Running the clustering in the shuffled stack makes the trick, as all labels (pixel coordinates) for the clusters will match and the cluster shot retrieves single values from each map. 

  - ~~Another option could be to append just the mean when multiple values are found.~~

    - ~~This could be implemented using np.unique(return_counts=True), as done in the test notebook:~~

      - ```python
        u, counts = np.unique(testtest, return_counts=True)
        np.mean(np.repeat(u,counts))
        ```

      ~~It is probably the easiest way to continue at this point, since everything is already working as needed. With this weighted mean the error introduced will be minimized. A test with the "shuffled" stack is probably mandatory too before proceeding, despite it can be time consuming.~~ 

- [x] export cluster shot data to pandas dataframe and then to a file which is loadable into Accurion's DataStudio. 
  - This should include Cy, Cx for each cluster, so that a "thickness" image can be rebuilt when the data for each cluster are fitted into the model. (this is a post-project idea, of course)

- [x] add histogram or bar-plot of pixel value distribution of raw maps for selected cluster. This would be a nice visual indication of how good or bad the selected number of clusters for the segmentation was
- [x] change preprocessing function used. Use transposed output to comply with the visual coordinates and not to introduce confusion on the user when comparing with the raw .png maps are displayed directly from the file explorer

- [x] EXPLORE FRONT-END OPTIONS WITH STREAM-LIT!!

  - [x] wait for input folder before anything continues?
  - [x] .getEstimation will not show. Introduce param. to export estimation graph as .png and then load it into the streamlit app? -- SOLVED WITH CUSTOM LIBRARY FROM GITHUB ([link](https://github.com/snehankekre/streamlit-yellowbrick))
  - [x] define selector sliders in the sidebar: 
    - [x] C_Selector
    - [x] idx_selector for WL
    - [x] define what happens when selected value in the slider changes
  - [x] define buttons or other kind of selector box for the image to display
  - [ ] add info texts at the sidebar (?) with .dat file name (experiment name), number of maps and their size, number of WL, and time taken for the preprocessing
  - [ ] add balloons or progress bar to show time consumed in the executions, specially when instantiating the class and loading the maps and when running the clustering
  - [ ] add button to export clustershot data
  - [x] solve error of 'WL_max' is not defined at the startup of streamlit app
  - [x] explore caching options to speed up the whole front-end. In the current status, any changes in any slider or button in the interface will re-instantiate the whole folder, which is not bearable if the folder contains more than a few maps -- SOLVED: .clusterize() has been removed from init in class. Now only the instantiation of the class is cached and clusterize() will launch only when pressing a button in streamlit

# LAST THINGS TO DO, in order

1. Test all data sets which will be linked to use the app
2. Include small set in the repo to be used directly without downloading any extra data
3. Check other TFMs in order to have a reference for the extension and structure of the memory
4. Finish pending to-dos in plotting functions and other extras and details in the frontend 
5. Create .yam file with the environment modules and dependancies and test how that will be installed in a fresh system
6. Pack streamlit app so that it can be executed with a double-click
7. Write memory
8. Expand Readme.md to fit the required format
