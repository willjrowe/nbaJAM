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
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])
    redMask = cv2.inRange(imageHSV, lower_red, upper_red)
    image[redMask>0]=(255,255,255)

    #might need to add similar as above for green but waiting for now

    #convert to grayscale and then threshold so only white is turned into black allowing for better text detection
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
    return image

def getPlayerDict(position) -> dict:
    #CONSTANTS
    playerNameTopY = 714
    playerNameBottomY = 750
    RowTopY = [0,766,790,811,835,857] #first zeros are for 0-indexing
    RowBottomY = [0,790,811,835,857,880]
    ColOneNames = ["0-index","BLK","CTH","DRB","DNK","PAS"]
    ColTwoNames = ["0-index","SPD","STL","STR","2PT","3PT"]
    playerPicTopY = 525
    playerPicBottomY = 700

    #PLAYER DEPENDENT
    if position == 1:
        playerNameTopX = 350
        playerNameBottomX = 588
        colOneTopX = 493
        colOneBottomX = 522
        colTwoTopX = 589
        colTwoBottomX = 622
        playerPicTopX = 330
        playerPicBottomX = 605
    elif position == 2:
        playerNameTopX = 698
        playerNameBottomX = 916
        colOneTopX = 820
        colOneBottomX = 852
        colTwoTopX = 920
        colTwoBottomX = 950
        playerPicTopX = 665
        playerPicBottomX = 940
    elif position == 3:
        playerNameTopX = 1035
        playerNameBottomX = 1239
        colOneTopX = 1149
        colOneBottomX = 1184
        colTwoTopX = 1248
        colTwoBottomX = 1282
        playerPicTopX = 990
        playerPicBottomX = 1265
    else: #hopefully position == 4, but i dont feel like throwing errors
        playerNameTopX = 1328
        playerNameBottomX = 1574
        colOneTopX = 1480
        colOneBottomX = 1511
        colTwoTopX = 1578
        colTwoBottomX = 1612
        playerPicTopX = 1320
        playerPicBottomX = 1595

    #get player name and confirm it is correct
    playerNameIMG = mainIMG[playerNameTopY:playerNameBottomY,playerNameTopX:playerNameBottomX]
    playerName = pytesseract.image_to_string(playerNameIMG,config='--psm 7').strip().rstrip()
    print("OCR detected Player Name: " + playerName)
    nameCheck = input("Is the above name correct? If so, input y. Otherwise input n:")
    if nameCheck == "n":
        playerName = input("Please enter the correct name in all caps:") 
    
    playerDict = {}
    playerDict["lastname"] = playerName

    #get player stats and store in dict
    for i in range(1,6):
        colOneStat = ColOneNames[i]
        colTwoStat = ColTwoNames[i]
        rowTop = RowTopY[i]
        rowBottom = RowBottomY[i]
        colOneimg = cleanedIMG[rowTop:rowBottom,colOneTopX:colOneBottomX]
        colOneimgtext = pytesseract.image_to_string(colOneimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
        colTwoimg = cleanedIMG[rowTop:rowBottom,colTwoTopX:colTwoBottomX]
        colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
        if colOneimgtext not in "012345678910": 
            print("OCR detected invalid input for " + playerName +"'s " + colOneStat + " stat. Expected: integer 1 - 10. Got " + colOneimgtext)
            colOneimgtext = input("Please enter correct stat here:")
        if colTwoimgtext not in "012345678910": 
            print("OCR detected invalid input for " + playerName +"'s " + colTwoStat + " stat. Expected: integer 1 - 10. Got " + colTwoimgtext)
            colTwoimgtext = input("Please enter correct stat here:")    
        playerDict[colOneStat] = int(colOneimgtext)
        playerDict[colTwoStat] = int(colTwoimgtext)
    
    print(playerDict)
    playerPic = mainIMG[playerPicTopY:playerPicBottomY,playerPicTopX:playerPicBottomX]
    cv2.imshow(playerName, playerPic)  
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    return playerDict

mainIMG = cv2.imread("teamScreen.png",cv2.IMREAD_UNCHANGED)
mainIMGcopy = mainIMG.copy()
cleanedIMG = cleanImage(mainIMGcopy)
getPlayerDict(1)
getPlayerDict(2)
getPlayerDict(3)
getPlayerDict(4)

