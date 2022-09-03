# CamCalibration
The UAV carries a separate camera (Go Pro Hero 4 Session) to take HD photos of the desired target. Due to the fish eye lens of the camera, the resulting image is distorted resulting in straight lines appearing curved which will cause errors when finding the centroid (in reference to the image frame) of the desired target. To counter this, the camera characteristics and distortion coefficients had to be found in order to undistort the captured image for further processing.

Python with OpenCV was used to calibrate the camera and as well as perform the image undistrtion. The image undistortion script was further implemented into the centroid calculation program which calculates the centroid of the desired target by taking in user input and outputting the centroid of the target in pixels in reference to the image frame.

Link to all checkerboard images for the Go Pro Hero 4 Sessions if you would like to calibrate it yourself and [try it out](https://drive.google.com/file/d/1QHobKReNjtnhk5orVABr_ouo015HflFj/view?usp=sharing)
