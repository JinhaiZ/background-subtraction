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
# convert binary image to bw image and cast int to uint8
img = np.uint8(img*255)
# filp black and white becasue cv2.connectedComponents only works for white components
img = cv2.bitwise_not(img)

# Connected Components Labeling


#find all your connected components (white blobs in your image)
nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
#connectedComponentswithStats yields every seperated component with information on each of them, such as size
#the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
sizes = stats[0:, -1]

# minimum size of particles we want to keep (number of pixels)
#here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
min_size = output.shape[0]*output.shape[1] * 0.0008
max_size = output.shape[0]*output.shape[1] * 0.25

kernel = np.ones((2,2),np.uint8)
# your answer image
combined_img = np.zeros((output.shape))
#for every component in the image
# you keep it only if it's above min_size
for i in range(1, nb_components):
    component = np.zeros((output.shape))
    component[output == i] = 1
    # morphological operations including dilation and erosion
    # Erosion, remove noise
    component = cv2.erode(component,kernel,iterations = 1)
    # dilation, recover size
    component = cv2.dilate(component,kernel,iterations = 1)
    # size filtering
    if sizes[i] >= min_size or sizes[i]<= max_size:
        component[output == 1] = 0
    # add to combined_img
    combined_img += component

combined_img[combined_img > 1] = 1
combined_img = np.uint8(combined_img)
#create two subplots
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

im1 = ax1.imshow(output)
im2 = ax2.imshow(combined_img)



plt.show()
