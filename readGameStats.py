import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# testIMG = cv2.imread("testIMG.png",cv2.IMREAD_UNCHANGED)
statsIMG = cv2.imread("testIMG.png",0)
statsIMG = cv2.threshold(statsIMG, 150, 255, cv2.THRESH_BINARY_INV)[1]

nameIMG  = cv2.imread("testIMG.png",cv2.IMREAD_UNCHANGED)


#first box top left 270, 424 bottom right 604, 612
#second box top left 618 , 424 bottom right 949, 612
#third box top left 973, 424 bottom right 1293, 612
#fourth box top left 1321, 424 bottom right 1651, 612

firstPlayerNameTopX = 296
firstPlayerNameBottomX = 569
secondPlayerNameTopX = 660
secondPlayerNameBottomX = 915
thirdPlayerNameTopX = 1009
thirdPlayerNameBottomX = 1268
fourthPlayerNameTopX = 1366
fourthPlayerNameBottomX = 1612
NameTopY = 425
NameBottomY = 464
firstPlayerPTSTopX = 346
firstPlayerPTSTopY = 464
firstPlayerPTSBottomX = 407
firstPlayerPTSBottomY = 497
firstPlayerColOneTopX = 346
firstPlayerColOneBottomX = 407
firstPlayerColTwoTopX = 515
firstPlayerColTwoBottomX = 575
secondPlayerColOneTopX = 695
secondPlayerColOneBottomX = 751
secondPlayerColTwoTopX = 858
secondPlayerColTwoBottomX = 921
thirdPlayerColOneTopX = 1052
thirdPlayerColOneBottomX = 1115
thirdPlayerColTwoTopX = 1217
thirdPlayerColTwoBottomX = 1274
fourthPlayerColOneTopX = 1398
fourthPlayerColOneBottomX = 1460
fourthPlayerColTwoTopX = 1564
fourthPlayerColTwoBottomX = 1626
Row1TopY = 464
Row1BottomY = 497
Row2TopY = 494
Row2BottomY = 522
Row3TopY = 522
Row3BottomY = 548
Row4TopY = 548
Row4BottomY = 574
Row5TopY = 574
Row5BottomY = 602

RowTopY = [0,464,494,522,548,574]
RowBottomY = [0,494,522,548,574,602]

firstColNames = ["0-index","PTS","AST","BLK","STL","3PT"]
secondColNames = ["0-index","DNK","SHV","OOP","PCT","REB"]


firstPlayerNameimg = nameIMG[NameTopY:NameBottomY,firstPlayerNameTopX:firstPlayerNameBottomX]
firstPlayerNameimgtext = pytesseract.image_to_string(firstPlayerNameimg,config='--psm 7')
print("First Player Name: " + firstPlayerNameimgtext)
secondPlayerNameimg = nameIMG[NameTopY:NameBottomY,secondPlayerNameTopX:secondPlayerNameBottomX]
secondPlayerNameimgtext = pytesseract.image_to_string(secondPlayerNameimg,config='--psm 7')
print("Second Player Name: " + secondPlayerNameimgtext)
thirdPlayerNameimg = nameIMG[NameTopY:NameBottomY,thirdPlayerNameTopX:thirdPlayerNameBottomX]
thirdPlayerNameimgtext = pytesseract.image_to_string(thirdPlayerNameimg,config='--psm 7')
print("Third Player Name: " + thirdPlayerNameimgtext)
fourthPlayerNameimg = nameIMG[NameTopY:NameBottomY,fourthPlayerNameTopX:fourthPlayerNameBottomX]
fourthPlayerNameimgtext = pytesseract.image_to_string(fourthPlayerNameimg,config='--psm 7')
print("Fourth Player Name: " + fourthPlayerNameimgtext)
#first player loop
for i in range(1,6):
    colOneStat = firstColNames[i]
    colTwoStat = secondColNames[i]
    rowTop = RowTopY[i]
    rowBottom = RowBottomY[i]
    colOneimg = statsIMG[rowTop:rowBottom,firstPlayerColOneTopX:firstPlayerColOneBottomX]
    colOneimgtext = pytesseract.image_to_string(colOneimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    colTwoimg = statsIMG[rowTop:rowBottom,firstPlayerColTwoTopX:firstPlayerColTwoBottomX]
    colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    print("First Player " + colOneStat + ": " + colOneimgtext)
    print("First Player " + colTwoStat + ": " + colTwoimgtext)

#second player loop
for i in range(1,6):
    colOneStat = firstColNames[i]
    colTwoStat = secondColNames[i]
    rowTop = RowTopY[i]
    rowBottom = RowBottomY[i]
    colOneimg = statsIMG[rowTop:rowBottom,secondPlayerColOneTopX:secondPlayerColOneBottomX]
    colOneimgtext = pytesseract.image_to_string(colOneimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    colTwoimg = statsIMG[rowTop:rowBottom,secondPlayerColTwoTopX:secondPlayerColTwoBottomX]
    colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    print("Second Player " + colOneStat + ": " + colOneimgtext)
    print("Second Player " + colTwoStat + ": " + colTwoimgtext)

#third player loop
for i in range(1,6):
    colOneStat = firstColNames[i]
    colTwoStat = secondColNames[i]
    rowTop = RowTopY[i]
    rowBottom = RowBottomY[i]
    colOneimg = statsIMG[rowTop:rowBottom,thirdPlayerColOneTopX:thirdPlayerColOneBottomX]
    colOneimgtext = pytesseract.image_to_string(colOneimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    colTwoimg = statsIMG[rowTop:rowBottom,thirdPlayerColTwoTopX:thirdPlayerColTwoBottomX]
    colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    print("Third Player " + colOneStat + ": " + colOneimgtext)
    print("Third Player " + colTwoStat + ": " + colTwoimgtext)

#fourth player loop
for i in range(1,6):
    colOneStat = firstColNames[i]
    colTwoStat = secondColNames[i]
    rowTop = RowTopY[i]
    rowBottom = RowBottomY[i]
    colOneimg = statsIMG[rowTop:rowBottom,fourthPlayerColOneTopX:fourthPlayerColOneBottomX]
    colOneimgtext = pytesseract.image_to_string(colOneimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    colTwoimg = statsIMG[rowTop:rowBottom,fourthPlayerColTwoTopX:fourthPlayerColTwoBottomX]
    colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='--psm 7 tessedit_char_whitelist=0123456789')
    print("Fourth Player " + colOneStat + ": " + colOneimgtext)
    print("Fourth Player " + colTwoStat + ": " + colTwoimgtext)


# firstPlayerPTSimg = statsIMG[RowOneTopY:RowOneBottomY,firstPlayerColOneTopX:firstPlayerColOneBottomX]
# firstPlayerPTS = pytesseract.image_to_string(firstPlayerPTSimg,config='--psm 7 tessedit_char_whitelist=0123456789')
# print("First Player PTS: " + firstPlayerPTS)
# del firstPlayerPTSimg

# firstPlayerNameIMG = testIMG[firstPlayerNameTopY:firstPlayerNameBottomY,firstPlayerNameTopX:firstPlayerNameBottomX]
# text = pytesseract.image_to_string(firstPlayerNameIMG)
# print(text)

#USE THRESHOLDING FOR NUMBERS, BUT NOT FOR NAMES

# firstPlayerPTSIMG = testIMG[firstPlayerPTSTopY:firstPlayerPTSBottomY,firstPlayerPTSTopX:firstPlayerPTSBottomX]
# text = pytesseract.image_to_string(firstPlayerPTSIMG)
# print(text)

# firstPlayerASTimg = testIMG[RowThreeTopY:RowThreeBottomY,secondPlayerColOneTopX:secondPlayerColOneBottomX]
# text = pytesseract.image_to_string(firstPlayerASTimg,config='--psm 7 tessedit_char_whitelist=0123456789')
# print(text)


# cv2.imshow("test", firstPlayerASTimg)  
# cv2.waitKey(0)

# text = pytesseract.image_to_string(testIMG)
# print(text)
# print(testIMG.shape)
# firstPlayer = testIMG[424:612,270:604]
# secondPlayer = testIMG[424:612,618:949]
# text = pytesseract.image_to_string(secondPlayer)
# print(text)
# cv2.imshow("test", secondPlayer)  
# cv2.waitKey(0)