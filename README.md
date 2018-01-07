# Background Subtraction for Thermal Image 

This is an implementation of the thermal image background subtraction algorithm described in [Human Detection Based on the Generation of a Background Image and Fuzzy System by Using a Thermal Camera](http://www.mdpi.com/1424-8220/16/4/453/htm)

## Background Generation

The demo below shows the first part of the algorithme, generating a background image.

- The top left image shows the preliminary background image obtained by median value from the sequence of images
- The top right image shows the binary image of extracted candidate human area
- The bottom left image shows the binary image of exteacted human areas by labeling, size filtering and morphological operations
- The bottom right image is the final generated background image

![demo](./demo.gif)
