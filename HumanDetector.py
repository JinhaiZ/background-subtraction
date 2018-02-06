import cv2
import math
import copy
import numpy as np
from Fuzzy import Fuzzy

class HumanDetector():

    def __init__(self, height=60, width=80, debug=False):
        self.height = height
        self.width = width
        self.debug = debug
        # normalized f1 value, f1 is the average of the background image
        self.f1 = 0.5
        # normalized f2 value, f2 is the sum of the difference between background and input image
        self.f2 = 0.5
        # the optimal threshold
        self.p = 0.5
        self.fuzzy = Fuzzy() # instantiate a Fuzzy System instance with hardcoded membership function
        self.image_diff = np.zeros(shape=(self.height,self.width)) # generated difference image based on optimal threshold p
        self.combined_diff_img = np.zeros(shape=(self.height,self.width)) # 

    def getTotalPixal(self):
        return self.height*self.width

    def setFValues(self, input_frame, generated_bg, T=80):
        # compute F1 value
        diff_frame = np.abs(input_frame - generated_bg)
        image_diff = input_frame - generated_bg
        image_diff[diff_frame <= T] = 0
        F1 = np.sum(generated_bg)/self.getTotalPixal()
        # normalize F1
        self.f1 = 1.039048-1.039048*math.exp(-3.2828/255*F1)
        # compute F2 value
        F2 = np.sum(image_diff)
        # normalize f2
        #print "F2=", 1-math.exp(-16.09438/122400*F2)
        #print "F1=", 1.039048-1.039048*math.exp(-3.2828/255*F1)
        
        self.f2 = 1-math.exp(-16.09438/122400*abs(F2))
        #print("F2=", F2, " f2=", self.f2)

    def getBinaryDiffImage(self, input_frame, generated_bg, p, alpha=25, beta=15):
        # alpha and beta parameters described in Equation(11)
        diff = input_frame - generated_bg
        diff[diff < alpha*p + beta] = 0
        diff[diff !=0 ] = 1
        return diff

    def humanRegionConfirmation(self, image_diff, min_size_ratio=0.05, max_size_ratio=0.4):
        
        # the kernel slides through the image
        kernel = np.ones((3,3),np.uint8)
        # morphological operations: Erosion, remove noise
        image_diff = cv2.erode(image_diff,kernel,iterations = 1)
        # morphological operations: dilation, recover size
        image_diff = cv2.dilate(image_diff,kernel,iterations = 1)
        image_diff = np.uint8(image_diff*255) # same ops for imgb
        self.image_diff = cv2.bitwise_not(image_diff)

        # remaining connected components
        remainings = []
        # find connected components (white blobs in the image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image_diff, connectivity=8)
        #just take size information
        sizes = stats[0:, -1]
        # minimum and maximum size of particles we want to keep (number of pixels)
        min_size = output.shape[0]*output.shape[1] * min_size_ratio
        max_size = output.shape[0]*output.shape[1] * max_size_ratio
        # prepare for the final image 
        combined_img = np.zeros((output.shape))
        #for every component in the image
        for i in range(1, nb_components):
            component = np.zeros((output.shape))
            component[output == i] = 1
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

    def generateBoudingBox(self, stats, input_img):
        for stat in stats:
            input_img[stat[1]:stat[1]+stat[3], stat[0]] = 255
            input_img[stat[1]:stat[1]+stat[3], stat[0]+stat[2] - 1] = 255
            input_img[stat[1], stat[0]:stat[0]+stat[2]] = 255
            input_img[stat[1]+stat[3] - 1, stat[0]:stat[0]+stat[2]] = 255
        return

    def returnValues(self, frame):
        if self.debug:
            return self.image_diff, self.combined_diff_img, frame
        else:
            return self.combined_diff_img

    def apply(self, frame, generated_bg):
        # resize frame, frame is (60, 80) float array
        frame = np.median(frame,axis=2)
        # compute F1 and F2 to get optimal threshold
        self.setFValues(frame, generated_bg)
        # get optimal threshold
        self.p = self.fuzzy.get_threshold(self.f1, self.f2)
        # generate difference image based on the optimal threshold
        self.image_diff = self.getBinaryDiffImage(frame, generated_bg, self.p) # same ops for imgb
        # Morphorlogical Operation with Connected Components Labeling
        if (self.debug):
            img_diff = copy.deepcopy(self.image_diff)
        else:
            img_diff = self.image_diff
        stats, combined_diff_img = self.humanRegionConfirmation(img_diff)
        self.generateBoudingBox(stats, frame)
        self.combined_diff_img = np.uint8(combined_diff_img*255)
        return self.returnValues(frame)