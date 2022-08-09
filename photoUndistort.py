# This script is to undistort images taken by the Go Pro Hero Session 4 camera using the
# Results from the camera calibration script

import numpy as np
import csv 
import cv2 
import glob

# find images to undistort, this can be easily changed
file = "03.jpg"
imgDistort = cv2.imread('./images/' + file)
#imgDistort = cv2.imread("01.png")

# get dimensions of image
h, w, _ = imgDistort.shape

# loading camera matrix and distortion values from camera calibration program
camMatrix = np.genfromtxt("camMatrix_GoPro.txt", dtype = float, encoding = None, delimiter = ',')
distortion = np.genfromtxt("distortion_GoPro.txt", dtype = float, encoding = None, delimiter = ',')


#print("Camera Matrix: ", camMatrix)
#print("\nDistortion: ", distortion)

# get new camera matrix based on the distortion and image width and height
newCamMtx, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distortion, (w, h), 1, (w, h))

#print("Roi:", roi)

# undistort the image 
unDistortImg = cv2.undistort(imgDistort, camMatrix, distortion, None, newCamMtx)

# crop image to show only undistorted parts
# the undistort function creates black regions that show the unwarping
x, y, w1, h1 = roi

unDistortImg = unDistortImg[y:y+h1, x:x+w1]

# show undistorted image
cv2.imshow("Undistorted Img", unDistortImg)

k = cv2.waitKey(0)
if k == ord("s"):
    cv2.imwrite("undistortedImg.png", unDistortImg)
    cv2.destroyAllWindows
