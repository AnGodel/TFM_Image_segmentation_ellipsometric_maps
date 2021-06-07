## Disadvantages and challenges:
   - application to a set of maps with dimension (rows, columns, [number of maps]
   - application to a set of combined delta and psi maps
   - the number of initial clusters must be set manually. Maybe this can be used as tunable parameter in the future front-end
   - loss of resolution on edges 

## To-Do:
   - ~~try Kmeans++~~ kmeans++ esta ya implementado dentro del kmeans normal
   - ~~try DBSCAN~~
   - ~~try segmentation by MeanShift~~ the result in the example looks awesome, but it can't be applied to our maps, since the imput image must be 8-bit 3 channel
   - apply canny (or other method) to detect edges in segmented image
   - ~~try also other example maps~~
   - explore how to get the metrics for the different number of clusters in the K-Means algorithm
   - ~~implement function to do the clustering directyly in MyPacket~~

