# Working with stacked images

## About naming

The maps naming convention is different depending on the grabbing method:

- Maps obtained with traditional nulling method will be named with just a rolling number at the end (xxx_001.png, xxx_002.png, etc)
  - Not possible to distinguish delta maps from psi maps just from the file name.
  - Typically the even numbers will be delta maps and the odd numbers will be psi maps.

- Maps obtained with RCE method will be named as xxx_Delta_001.png, xxx_Psi_001.png, xxx_Delta_002.png, xxx_Psi_002.png
  - Much easier to handle, but the preprocessing algorithm must be different.

## To-Do

- try segmentation on a stack of delta and psi maps combined
- try to improve the k estimation decreasing max number of clusters in the estimator
- try segmentation after combining delta and psi maps in one using the math provided by MD
  - this might be interesting in order to reduce the computing time of the clustering but will have other disadvantages:
    - because of the math operation, the pixel of the combined map will have small values, in the range -1,1, which will likely need to be rescaled for proper plotting
    - with or without rescaling, the labels obtained by this segmentation can't be directly used:
      - of this combined map will be useful only for finding the shapes and contours of the clusters and export a mask to be applied in the original maps to extract the numeric values
      - another option would by applying reversed math to get delta and psi values from the labels of the segmentation of C and S maps
- test the computing time on small and large stacks for both the estimation with yellowbrick visualizers and the segmentation itself