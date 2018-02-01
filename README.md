# Background Subtraction for Thermal Image 

This is an implementation of the thermal image background subtraction algorithm described in [Human Detection Based on the Generation of a Background Image and Fuzzy System by Using a Thermal Camera](http://www.mdpi.com/1424-8220/16/4/453/htm)

## Background Generation

The demo below shows the first part of the algorithme, generating a background image.

- The top left image shows the preliminary background image obtained by median value from the sequence of images
- The top right image shows the binary image of extracted candidate human area
- The bottom left image shows the binary image of exteacted human areas by labeling, size filtering and morphological operations
- The bottom right image is the final generated background image

![demo](./demo.gif)

## Human Detection

The demo below shows the second part of the algorithme,human detection based on the generated background image.

- The top left image shows final generated background image
- The top right image shows the binary difference image between input image and generated background image, the threshold is determinded dynamically with a fuzzy system
- The bottom left image shows the binary difference image of detected human areas by labeling, size filtering and morphological operations
- The bottom right image shows the detected boxs containing of human areas on the orignal input image

![demo](./demo2.gif)


:warning: The following features have not yet been implemented

- Vertical and Horizontal Separation of Candidate Region
- Confirmation of Human Area Based on Camera Viewing Direction