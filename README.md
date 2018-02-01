# Human Detection with Thermal Imagery

## Introduction

This is the final year project at IMT Atlantique (a French engineering school) for students majored in computer systems and networks. The aim of the project is to detect human presence with thermal image captured from a thermal camera of an embedded linux system. Since thermal camera has less intrusion to privacy (thermal camera has no color information and it has low resolution) compared to commerical WebCams with high-resolution, we can develop services for elders and people with disabilities based on this project.

Basically, what stored at this repository is an implementation of the thermal image background subtraction algorithm described in [Human Detection Based on the Generation of a Background Image and Fuzzy System by Using a Thermal Camera](http://www.mdpi.com/1424-8220/16/4/453/htm). Since the method described in this paper has the state-of-the-art performance of human presence detection with thermal imagery, this project choose to implement this algorithm as the core part for presence detection.

The method described in the paper has two main steps, namely, the Background Generation and the Human Detection. The demo of the implemention are shown below. 

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

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.