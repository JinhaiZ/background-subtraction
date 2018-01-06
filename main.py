import cv2
import matplotlib.pyplot as plt
import numpy as np

#Initiate
cap = cv2.VideoCapture('output.avi')
median_frames = 10
images = np.zeros(shape=(60,80) + (median_frames,))
for i in xrange(median_frames):
    ret,frame = cap.read()
    frame = np.median(frame,axis=2)
    images[:,:,i] = frame

img = np.median(images, axis=2)
plt.imshow(img)
plt.show()

