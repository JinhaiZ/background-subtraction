import cv2
import matplotlib.pyplot as plt
import numpy as np

#Initiate
cap = cv2.VideoCapture('test.avi')
median_frames = 10
index_P = 1.5
index_Q = 120.4
for i in xrange(400):
    ret,frame = cap.read()
images = np.zeros(shape=(60,80) + (median_frames,))
for i in xrange(median_frames):
    # read a frame, frame is (60, 80, 3) unit8 array
    ret,frame = cap.read()
    # resize frame, frame is (60, 80) float array
    frame = np.median(frame,axis=2)
    # add frame to images, images is (60, 80, median_frames) float array
    images[:,:,i] = frame

# get temporal median img, img is (60, 80) float array
img = np.median(images, axis=2)
# get the standard deviation value
std = np.std(img)
# get the average value
avg = np.mean(img)
# get binary image
def f(pixel):
    if(pixel < avg - index_P*std and avg > index_Q) or (pixel > avg + index_P*std and avg <= index_Q):
        return 0
    else:
        return 1
def binarization(image):
    return  np.vectorize(f)(image)
# binarization
img = binarization(img)
# component labeling
# convert binary image to bw image
img = np.uint8(img*255)
# filp black and white becasue cv2.connectedComponents only works for white components
img = cv2.bitwise_not(img)

ret, labels = cv2.connectedComponents(img)

# Map component labels to hue val
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR for display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

# set bg label to black
labeled_img[label_hue==0] = 0

plt.imshow(labeled_img)
plt.show()

# orphological operations including dilation and erosion


