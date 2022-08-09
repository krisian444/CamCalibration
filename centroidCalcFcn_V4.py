# This function is from the target localization aspect of the target detection system
# It is used to find the centroid of the target(s) in which the results are then used to
# calculate the approximate GPS coordinates relative to the aircraft from the time the 
# image was taken


import numpy as np
import cv2
import sys
import time

def centroid(img):

    # Image Undistortion First ========================

    # get dimensions of image
    h, w, _ = img.shape

    # loading camera matrix and distortion values from camera calibration program
    camMatrix = np.genfromtxt("camMatrix_GoPro.txt", dtype = float, encoding = None, delimiter = ',')
    distortion = np.genfromtxt("distortion_GoPro.txt", dtype = float, encoding = None, delimiter = ',')

    # get new camera matrix based on the distortion and image width and height
    newCamMtx, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distortion, (w, h), 1, (w, h))

    # undistort the image 
    unDistortImg = cv2.undistort(img, camMatrix, distortion, None, newCamMtx)

    # crop image to show only undistorted parts
    # the undistort function creates black regions that show the unwarping
    x, y, w1, h1 = roi

    unDistortImg = unDistortImg[y:y+h1, x:x+w1]

    #cv2.imshow("undistorted image", unDistortImg)

    # Undistortion FINISHED ========================
    # IF UNDISTORTION NOT NEEDED, comment out everything above
    # Change line 40 input into img instead of unDistortImg

    # Time for centroid calculation
    # convert image to HSV 
    hsvImg = cv2.cvtColor(unDistortImg, cv2.COLOR_BGR2HSV)

    while(1):
        # ask user for input - which target
        print("Centroid Calcuation Program \nSelect Target Color for Calculation\n")
        print("1 - Red \n2 - Yellow \n3 - Blue \n4 - Orange \n5 - Purple")
        num = input("\nSelect target color: ")
        num = int(num)

        # Selects color range for colors to be detected depending on user input
        # Color ranges in HSV
        # RED, red has 2 locations on the HSV spectrum in OpenCv
        if num == 1:
            colorRangeLo = np.array([165, 87, 111], np.uint8)
            colorRangeLo2 = np.array([0, 100, 120], np.uint8)

            colorRangeHi = np.array([180, 255, 255], np.uint8)
            colorRangeHi2 = np.array([8, 255, 255], np.uint8)

            mask1 = cv2.inRange(hsvImg, colorRangeLo, colorRangeHi)
            mask2 = cv2.inRange(hsvImg, colorRangeLo2, colorRangeHi2)
            Mask = mask1 + mask2
            break
        # YELLOW
        elif num == 2:
            colorRangeLo = np.array([24, 120, 180], np.uint8) 
            colorRangeHi = np.array([34, 255, 255], np.uint8)

            Mask = cv2.inRange(hsvImg, colorRangeLo, colorRangeHi)
            break
        # BLUE
        elif num == 3:
            colorRangeLo = np.array([100, 80, 80], np.uint8) 
            colorRangeHi = np.array([125, 255, 255], np.uint8)

            Mask = cv2.inRange(hsvImg, colorRangeLo, colorRangeHi)
            break
        # ORANGE
        elif num == 4:
            colorRangeLo = np.array([10, 200, 200])
            colorRangeHi = np.array([22, 255, 255])

            Mask = cv2.inRange(hsvImg, colorRangeLo, colorRangeHi)
            break
        # PURPLE
        elif num == 5:
            colorRangeLo = np.array([135, 220, 170])
            colorRangeHi = np.array([150, 255, 255])

            Mask = cv2.inRange(hsvImg, colorRangeLo, colorRangeHi)
            break
        else:
            print("\nNot valid target selection, please try again \n")
            time.sleep(1)

    # use contours for multiple targets / objects then iterate through to get moments
    # moments are then used to find the centroids of the objects
    contours, heirarchy = cv2.findContours(Mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get number of contours found
    cLen = len(contours)
    #print("# of contour", cLen)

    # GoPro camera is used for target localiation and object sizes at a distance will look small
    # This part we will calculate the ratio of object size in real life vs how the camera sees it
    # Find how much pixels the object takes up in the image space

    objSizeReal = 24 # 24 inches in real life target size, can conver to metric if desired
    FleightHeight = 600 # camera distance to object, LiDar reading, converted to inches first or metric if desired
    focal = 2.92 # 2.92 mm focal length of GoPro Hero4 camera
    pixSizeCamera = 1.90*10**-3 # 1.12 micrometers into millimeters

    objAreaPix = np.uint16((objSizeReal/FleightHeight * focal) / pixSizeCamera)
    #print("min target sizes", objAreaPix)

    # checks if there are any contours found
    if(cLen != 0):
        # initialize variables, X Y coords in image frame
        X, Y = 0,0
        targ = 1
        # same as in color detection but instead calculates moments 
        for c in contours:
            areaC = cv2.contourArea(c)
            #print(areaC)
            if(areaC > objAreaPix):
            # calculate the moments for each contour
                M = cv2.moments(c)
                
                if M["m00"] != 0:
                    # calculate the coordinates of each moment / contour
                    X = int(M["m10"] / M["m00"])
                    Y = int(M["m01"] / M["m00"])
                else:
                    X, Y = 0,0

                # draw circle in image where centroid is, put text 
                cv2.circle(unDistortImg, (X,Y), 4, (255,255,255), -1)
                cv2.putText(unDistortImg, "Centroid", (X - 20, Y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                cv2.putText(unDistortImg, str(targ), (X - 40, Y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
                cv2.putText(unDistortImg, str(X)+',', (X + 20, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)
                cv2.putText(unDistortImg, str(Y), (X + 50, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)
                targ += 1

                # print out where target centroid(s) are
                print("Target Centroid (X,Y) is at:", X, ",", Y)

            else:
                print("No valid targets detected.")
                X, Y = None, None
    else:
        print("No targets detected.")
        X, Y = None, None


    #display image, comment out if not needed
    # cv2.imshow("Image with centroid", unDistortImg)
    # k = cv2.waitKey(0)
    # if k == ord("s"):
    #     cv2.imwrite("centroidFinishField.png", img)
    #     # left commented just incase needed to output image
    #     cv2.destroyAllWindows

    return [X, Y], num

def main():

    img = cv2.imread("Selection_010.png")

    res, color = centroid(img)

    print(res)

if __name__ == '__main__':
    main()