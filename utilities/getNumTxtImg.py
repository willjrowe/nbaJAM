import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def getPicsOfNumberText(image):
    numbersFound = ["1","2","3","4","5","6","7","8","9"]
    RowTopY = [0,511,526,541,556,571] #first zeros are for 0-indexing
    RowHeight = 14
    # RowBottomY = [0,523,538,553,568,583]
    ColTopX = [0,328,394,549,615,769,835,990,1056]
    ColLength = 14
    # ColBottomX = [0,342,408]
    j = 1
    for i in range(1,9):
        for j in range(1,6):
            rowTop = RowTopY[j]
            colTop = ColTopX[i]
            colOneimg = image[rowTop:rowTop+RowHeight,colTop:colTop+ColLength]
            cv2.imshow("Col",colOneimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            colOneLabel = input("What number is this?")
            if colOneLabel not in numbersFound:
                numbersFound.append(colOneLabel)
                cv2.imwrite('./labels/'+colOneLabel+".png",colOneimg)