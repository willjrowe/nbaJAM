import numpy as np
import cv2

img1 = cv2.imread("statTest3.png",cv2.IMREAD_UNCHANGED)
img2 = cv2.imread("statTest2.png",cv2.IMREAD_UNCHANGED)
img3 = cv2.subtract(img1,img2)
(b, g, r) = cv2.split(img3)
img5 = cv2.threshold(b, 100, 255, cv2.THRESH_BINARY)[1]
img4 = cv2.threshold(img3, 150, 255, cv2.THRESH_BINARY)[1]
imageHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
#turn any red pixels into white
#reason for this is tesseract was having issues recognizing red as a text color
lower_red = np.array([0,100,100])
upper_red = np.array([10,255,255])
redMask = cv2.inRange(imageHSV, lower_red, upper_red)
image[redMask>0]=(255,255,255)

#might need to add similar as above for green but waiting for now

#convert to grayscale and then threshold so only white is turned into black allowing for better text detection
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
return image
cv2.imshow("test",img5)
cv2.waitKey(0)