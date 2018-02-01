#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import copy
import math
import matplotlib.pyplot as plt
import numpy as np
from BackgroundGenerator import BackgroundGenerator
from HumanDetector import HumanDetector

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
    for i in xrange(90):
        ret,frame = cap.read()

    im1 = ax1.imshow(frame)
    im2 = ax2.imshow(frame)
    im3 = ax3.imshow(frame)
    im4 = ax4.imshow(frame)

    bgg = BackgroundGenerator(debug=True)
    hd = HumanDetector(debug=True)
    
    plt.ion()
    for i in xrange(500):
        # read a frame, frame is (60, 80, 3) unit8 array
        ret,frame = cap.read()
        median, binary, ccl, bg = bgg.apply(frame)
        diff, combined_diff, frame = hd.apply(frame, bg)
        # fig.savefig('./fig/fig-{!s}.png'.format(i)) and ffmpeg -r 30 -i fig-%d.png output.gif
        im1.set_data(bg)
        im2.set_data(diff)
        im3.set_data(combined_diff)
        im4.set_data(frame)
        plt.pause(0.0001)
    plt.ioff() # due to infinite loop, this gets never called.
    plt.show()
