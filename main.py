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
def binarize(image):
    return  np.vectorize(f)(image)

img = binarize(img)

plt.imshow(img)
plt.show()

