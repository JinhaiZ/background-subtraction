#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import copy
import math
import matplotlib.pyplot as plt
import numpy as np

# define functions
class BackgroundGenerator(object):

    def __init__(self, height=60, width=80, debug=False):
        self.height = height
        self.width = width
        self.index_P = 1.5
        self.index_Q = 120.4
        self.median_frames = 10
        self.images = np.zeros(shape=(self.height,self.width) + (self.median_frames,))
        self.median_frames_count = 0
        # compared to median_frames
        # update_image_a_rate = n means the median frame updates every median_frames * n frames are consumed
        self.update_image_a_rate = 1
        self.update_image_a_count = 0
        # image_a, the temporal median image
        self.image_a = np.zeros(shape=(self.height,self.width))
        # image_b, the binarized image
        self.image_b = np.zeros(shape=(self.height,self.width))
        # image_c, the image after connected components labeling, morphological operations and size filtering
        self.image_c = np.zeros(shape=(self.height,self.width))
        # image_d, the final generated background image
        self.image_d = np.zeros(shape=(self.height,self.width))
        self.debug = debug

    def __f(self, pixel, avg, std, index_P, index_Q):
        # the Equation described in the paper
        if(pixel < avg - index_P*std and avg > index_Q) or (pixel > avg + index_P*std and avg <= index_Q):
            return 0
        else:
            return 1

    def binarization(self,image):
        # get binary image
        
        # get the standard deviation value
        std = np.std(image)
        # get the average value
        avg = np.mean(image)
        return np.vectorize(self.__f)(image, avg, std, self.index_P, self.index_Q)

    def conComWithMorpOps(self, img, min_size_ratio=0.005, max_size_ratio=0.25):
        # Connected Components Labeling with morphological operations

        # remaining connected components
        remainings = []
        # find connected components (white blobs in the image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
        #just take size information
        sizes = stats[0:, -1]
        # minimum and maximum size of particles we want to keep (number of pixels)
        min_size = output.shape[0]*output.shape[1] * min_size_ratio
        max_size = output.shape[0]*output.shape[1] * max_size_ratio
        # the kernel slides through the image
        kernel = np.ones((5,5),np.uint8)
        # prepare for the final image 
        combined_img = np.zeros((output.shape))
        #for every component in the image
        for i in range(1, nb_components):
            component = np.zeros((output.shape))
            component[output == i] = 1
            # morphological operations: Erosion, remove noise
            component = cv2.erode(component,np.ones((3,3),np.uint8),iterations = 2)
            # morphological operations: dilation, recover size
            component = cv2.dilate(component,kernel,iterations = 5)
            # size filtering
            if sizes[i] <= min_size or sizes[i] >= max_size:
                component[output == i] = 0
            else:
                remainings.append(i)
            # add to combined_img
            combined_img += component
        # reconvert to binary image
        combined_img[combined_img > 1] = 1
        combined_img = np.uint8(combined_img)
        return stats[remainings], combined_img

    def generateSolidBoudingBox(self, stats, combined_img):
        for stat in stats:
            combined_img[stat[1]:stat[1]+stat[3], stat[0]:stat[0]+stat[2]] = 1
        return

    def linearInterpolation(self, img, combined_img):

        img[combined_img==1] = np.nan
        def interp(col):
            indices = np.arange(len(col))
            not_nan = np.logical_not(np.isnan(col))
            return np.interp(indices, indices[not_nan], col[not_nan])
        return np.apply_along_axis(interp, 1, img)

    def returnValues(self):
        if self.debug:
            return self.image_a, self.image_b, self.image_c, self.image_d
        else:
            return self.image_diff

    def apply(self, frame):
        # resize frame, frame is (60, 80) float array
        frame = np.median(frame,axis=2)
        img = frame
        # add frame to images, images is (60, 80, median_frames) float array
        self.images[:,:,self.median_frames_count%self.median_frames] = frame
        self.median_frames_count += 1
        if (self.median_frames_count >= self.median_frames):
            self.median_frames_count = self.median_frames_count%self.median_frames
            self.update_image_a_count += 1
        if (self.update_image_a_count >= self.update_image_a_rate):
            self.update_image_a_count = self.update_image_a_count%self.update_image_a_rate
            # get temporal median img, img is (60, 80) float array
            img = np.median(self.images, axis=2)
            self.image_a = copy.deepcopy(img)
            # binarization
            imgb = self.binarization(img)
            # convert binary image to bw image and cast int to uint8
            imgb = np.uint8(imgb*255)
            # filp black and white becasue cv2.connectedComponents only works for white components
            imgb = cv2.bitwise_not(imgb)
            self.image_b = imgb

            # Connected Components Labeling with Morphorlogical Operation
            stats, combined_img = self.conComWithMorpOps(imgb)
            #np.set_printoptions(threshold='nan')
            self.image_c = np.uint8(combined_img*255)
            # Generate Bounding box
            self.generateSolidBoudingBox(stats, combined_img)

            # linear interpolation, and generate final background image image_d
            self.image_d = self.linearInterpolation(img, combined_img)
            
            return self.returnValues()
        return self.returnValues()

if __name__ == '__main__':
    #Initiate
    cap = cv2.VideoCapture('test.avi')
    # create 4 subplots
    fig = plt.figure()
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,2,3)
    ax4 = plt.subplot(2,2,4)

    frame = np.zeros(shape=(60,80))
    for i in xrange(150):
        ret,frame = cap.read()

    im1 = ax1.imshow(frame)
    im2 = ax2.imshow(frame)
    im3 = ax3.imshow(frame)
    im4 = ax4.imshow(frame)

    bgg = BackgroundGenerator(debug=True)
    
    plt.ion()
    for i in xrange(1000):
        # read a frame, frame is (60, 80, 3) unit8 array
        ret,frame = cap.read()
        median, binary, ccl, bg = bgg.apply(frame)
        im1.set_data(median)
        im2.set_data(binary)
        im3.set_data(ccl)
        im4.set_data(bg)
        plt.pause(0.0001)
    plt.ioff() # due to infinite loop, this gets never called.
    plt.show()
