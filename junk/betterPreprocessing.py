import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def cleanImage(image):
#function to clean image and allow for easier tesseract text recognition (primarily for stats)

    #convert to HSV (hue saturation value)
    imageHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    #turn any red pixels into white
    #reason for this is tesseract was having issues recognizing red as a text color
    # lower_red = np.array([0,100,100])
    # upper_red = np.array([10,255,255])
    # redMask = cv2.inRange(imageHSV, lower_red, upper_red)
    brown_lo=np.array([22,22,22])
    brown_hi=np.array([255,255,255])

    mask=cv2.inRange(imageHSV,brown_lo,brown_hi)

    image[mask>0]=(255,255,255)

    #might need to add similar as above for green but waiting for now

    #convert to grayscale and then threshold so only white is turned into black allowing for better text detection
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
    return image

statsIMG = cv2.imread("BIGTESTTIME.png",cv2.IMREAD_UNCHANGED)
statsIMG = cleanImage(statsIMG)
cv2.imshow("hi",statsIMG)
cv2.waitKey(0)
