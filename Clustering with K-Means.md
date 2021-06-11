## Disadvantages and challenges:
   - application to a set of maps with dimension (rows, columns, [number of maps]
        - This has been tested. It works fine although it takes a few seconds to process. Tested with stack of three delta maps
   - application to a set of combined delta and psi maps
   - the number of initial clusters must be set manually. Maybe this can be used as tunable parameter in the future front-end
        - initial number of clusters can be evaluated with yellowbrick visualizers
        - it is slower than desirable and the results (estimated optimal number of clusters) are not reliable
             - this can be probably improved by decreasing the max number of clusters for the estimation
   - loss of resolution on edges 

## To-Do:
   - ~~try Kmeans++~~ kmeans++ esta ya implementado dentro del kmeans normal
   - ~~try DBSCAN~~
   - ~~try segmentation by MeanShift~~ the result in the example looks awesome, but it can't be applied to our maps, since the imput image must be 8-bit 3 channel
   - apply canny (or other method) to detect edges in segmented image
   - ~~try also other example maps~~
   - ~~explore how to get the metrics for the different number of clusters in the K-Means algorithm~~ The yellowbrick library provides a nice and easy solution for implementing the elbow method. However, the results obtained should be taken with care. They are sometimes not reproducible, vary depending on the metics used (distortion or other) and the optimal k number found does not always match the optimal value of clusters found manually by try and error.
   - ~~implement function to do the clustering directyly in MyPacket~~

