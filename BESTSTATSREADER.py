import cv2
import pytesseract
import numpy as np
from os import path
from skimage.metrics import structural_similarity
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
import json

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

team_completer = WordCompleter(["Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"])

teams = ["Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]

master_stats_file = open('master_stats.json',) 
master_stats = json.load(master_stats_file)

LIST_OF_NUMS = ["1","2","3","4","5","6","7","8","9","10"]

def getSimilarity(A,B) -> float:
    print(cv2.matchTemplate(A,B))

def getAllPlayerDicts(image):
    for i in range(1,5):
        getPlayerDict(i,image)


def getPlayerDict(position, image) -> dict:
    #CONSTANTS
    playerNameTopY = 476
    playerNameBottomY = 495
    RowTopY = [0,511,526,541,556,571] #first zeros are for 0-indexing
    RowHeight = 14
    ColLength = 14
    playerNameLength = 148
    ColOneNames = ["0-index","BLK","CTH","DRB","DNK","PAS"]
    ColTwoNames = ["0-index","SPD","STL","STR","2PT","3PT"]
    playerPicTopY = 346
    playerPicHeight = 120
    playerPicWidth = 175
    veryBottomY = 590

    #PLAYER DEPENDENT
    if position == 1:
        playerNameTopX = 227
        colOneTopX = 328
        colTwoTopX = 394
        playerPicTopX = 225
        veryBottomX = 410
    elif position == 2:
        playerNameTopX = 444
        colOneTopX = 549
        colTwoTopX = 615
        playerPicTopX = 447
        veryBottomX = 630
    elif position == 3:
        playerNameTopX = 672
        colOneTopX = 769
        colTwoTopX = 835
        playerPicTopX = 667
        veryBottomX = 848
    else: #hopefully position == 4, but i dont feel like throwing errors
        playerNameTopX = 888
        colOneTopX = 990
        colTwoTopX = 1055
        playerPicTopX = 888
        veryBottomX = 1070

   #get player name and confirm it is correct
    playerNameIMG = image[playerNameTopY:playerNameBottomY,playerNameTopX:playerNameTopX+playerNameLength]
    playerName = pytesseract.image_to_string(playerNameIMG,config='--psm 7').strip().rstrip()
    playerPic = image[playerPicTopY:playerPicTopY+playerPicHeight,playerPicTopX:playerPicTopX+playerPicWidth]
    print("OCR detected Player Name: " + playerName)
    cv2.imshow("Player Name",playerNameIMG)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    nameCheck = input("Is the above name correct? If so, input y. Otherwise input n:")
    if nameCheck == "n":
        playerName = input("Please enter the correct name in all caps:") 
    elif nameCheck == "skip":
        return
    cv2.imshow("Player Pic",playerPic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    curr_team_valid = False
    while not (curr_team_valid):
        curr_team = prompt('Curr Team: ', completer=team_completer,
                complete_while_typing=True)
        curr_team = curr_team.lower().capitalize()
        curr_team = list(curr_team)
        for i in range(1,len(curr_team)): #for full court press etc. multi name teams
            if curr_team[i].isspace():
                curr_team[i+1] = curr_team[i+1].upper()
        curr_team = "".join(curr_team)
        if curr_team in teams:
            curr_team_valid = True
        elif curr_team == "Teams":
            print("LIST OF TEAMS")
            for team in teams:
                print(team)
        else:
            print("Invalid input! Please enter a valid NBA team. For a list of teams type 'teams'.")
    playerPath = "./headshots/"+curr_team+"/"+playerName+".png"
    if not path.exists(playerPath):
        cv2.imwrite(playerPath,playerPic)
    
    playerDict = {}
    playerDict["lastname"] = playerName
    playerDict["team"] = curr_team
    
    for i in range(1,6):
        colOneStat = ColOneNames[i]
        colTwoStat = ColTwoNames[i]
        rowTop = RowTopY[i]
        rowBottom = rowTop + RowHeight
        colOneimg = image[rowTop:rowBottom,colOneTopX:colOneTopX+ColLength]
        colTwoimg = image[rowTop:rowBottom,colTwoTopX:colTwoTopX+ColLength]
        colOneBestMatch = 0
        colOneBestMatchRating = 0
        colTwoBestMatch = 0
        colTwoBestMatchRating = 0
        for j in range(1,11):
            currentComparisionIMG = cv2.imread("./labels/"+str(j)+".png",cv2.IMREAD_UNCHANGED)
            (colOneScore, diff1) = structural_similarity(colOneimg, currentComparisionIMG, full=True,multichannel=True)
            if abs(colOneScore) > colOneBestMatchRating:
                colOneBestMatch = j
                colOneBestMatchRating = abs(colOneScore)
            (colTwoScore, diff2) = structural_similarity(colTwoimg, currentComparisionIMG, full=True,multichannel=True)
            if abs(colTwoScore) > colTwoBestMatchRating:
                colTwoBestMatch = j
                colTwoBestMatchRating = abs(colTwoScore)
        playerDict[colOneStat] = colOneBestMatch
        playerDict[colTwoStat] = colTwoBestMatch
    print(playerDict)
    fullStatsIMG = image[playerNameTopY:veryBottomY,playerNameTopX:veryBottomX]
    cv2.imshow("Player Stats",fullStatsIMG)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    still_fixing = True

    while (still_fixing):
        print("Any stats/name/team to correct?")
        print("Type 'img' to see the image again!")
        print("Type 'd' to be done and save!")
        currInput = input("Type input:")
        if currInput == "d":
            still_fixing = False
        elif currInput in ColOneNames or currInput in ColTwoNames or currInput == "name" or currInput == "team":
            playerDict[currInput] = input("Input corrected " + currInput + " stat:")
            print(playerDict)
        elif currInput=="img":
            cv2.imshow("Player Stats",fullStatsIMG)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Unrecognized command")
    
    master_stats[curr_team][playerName] = playerDict
    json_object = json.dumps(master_stats) 
    with open("master_stats.json", "w") as outfile: 
        outfile.write(json_object) 

    return playerDict



    # #get player stats and store in dict
    # for i in range(1,6):
    #     colOneStat = ColOneNames[i]
    #     colTwoStat = ColTwoNames[i]
    #     rowTop = RowTopY[i]
    #     rowBottom = RowBottomY[i]
    #     colOneimg = cleanImage[rowTop:rowBottom,colOneTopX:colOneBottomX]
    #     colOneimgtext = pytesseract.image_to_string(colOneimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
    #     colTwoimg = cleanImage[rowTop:rowBottom,colTwoTopX:colTwoBottomX]
    #     colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
    #     if colOneimgtext not in "012345678910" or colOneimgtext=="": 
    #         print("OCR detected invalid input for " + playerName +"'s " + colOneStat + " stat. Expected: integer 1 - 10. Got " + colOneimgtext)
    #         colOneimgtext = input("Please enter correct stat here:")
    #     if colTwoimgtext not in "012345678910"or colTwoimgtext=="": 
    #         print("OCR detected invalid input for " + playerName +"'s " + colTwoStat + " stat. Expected: integer 1 - 10. Got " + colTwoimgtext)
    #         colTwoimgtext = input("Please enter correct stat here:")    
    #     playerDict[colOneStat] = int(colOneimgtext)
    #     playerDict[colTwoStat] = int(colTwoimgtext)
    
    # print(playerDict)
    # return playerDict

# mainIMG = cv2.imread("temp.PNG",cv2.IMREAD_UNCHANGED)
# getPlayerDict(3,mainIMG)


def getPicsOfNumberText(image):
    numbersFound = ["1","3","4","5","6","7","8","9","10"]
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
        
# mainIMG = cv2.imread("temp.PNG",cv2.IMREAD_UNCHANGED) 
# getPicsOfNumberText(mainIMG)

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

def fgetPlayerDict(position,cleanImage,originalImage) -> dict:
    #CONSTANTS
    playerNameTopY = 476
    playerNameBottomY = 495
    RowTopY = [0,511,526,541,556,571] #first zeros are for 0-indexing
    RowBottomY = [0,523,538,553,568,583]
    ColOneNames = ["0-index","BLK","CTH","DRB","DNK","PAS"]
    ColTwoNames = ["0-index","SPD","STL","STR","2PT","3PT"]
    playerPicTopY = 346
    playerPicBottomY = 467

    #PLAYER DEPENDENT
    if position == 1:
        playerNameTopX = 227
        playerNameBottomX = 375
        colOneTopX = 328
        colOneBottomX = 342
        colTwoTopX = 394
        colTwoBottomX = 408
        playerPicTopX = 225
        playerPicBottomX = 400
    elif position == 2:
        playerNameTopX = 698
        playerNameBottomX = 916
        colOneTopX = 549
        colOneBottomX = 563
        colTwoTopX = 615
        colTwoBottomX = 629
        playerPicTopX = 665
        playerPicBottomX = 940
    elif position == 3:
        playerNameTopX = 1035
        playerNameBottomX = 1239
        colOneTopX = 769
        colOneBottomX = 783
        colTwoTopX = 835
        colTwoBottomX = 849
        playerPicTopX = 990
        playerPicBottomX = 1265
    else: #hopefully position == 4, but i dont feel like throwing errors
        playerNameTopX = 1328
        playerNameBottomX = 1574
        colOneTopX = 990
        colOneBottomX = 1004
        colTwoTopX = 1056
        colTwoBottomX = 1070
        playerPicTopX = 1320
        playerPicBottomX = 1595

   #get player name and confirm it is correct
    playerNameIMG = originalImage[playerNameTopY:playerNameBottomY,playerNameTopX:playerNameBottomX]
    playerName = pytesseract.image_to_string(playerNameIMG,config='--psm 7').strip().rstrip()
    playerPic = originalImage[playerPicTopY:playerPicBottomY,playerPicTopX:playerPicBottomX]
    cv2.imwrite("playerHeadshot.png",playerPic)
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
        colOneimg = cleanImage[rowTop:rowBottom,colOneTopX:colOneBottomX]
        colOneimgtext = pytesseract.image_to_string(colOneimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
        colTwoimg = cleanImage[rowTop:rowBottom,colTwoTopX:colTwoBottomX]
        colTwoimgtext = pytesseract.image_to_string(colTwoimg,config='-c tessedit_char_whitelist=0123456789 --psm 7').strip().rstrip()
        if colOneimgtext not in "012345678910" or colOneimgtext=="": 
            print("OCR detected invalid input for " + playerName +"'s " + colOneStat + " stat. Expected: integer 1 - 10. Got " + colOneimgtext)
            colOneimgtext = input("Please enter correct stat here:")
        if colTwoimgtext not in "012345678910"or colTwoimgtext=="": 
            print("OCR detected invalid input for " + playerName +"'s " + colTwoStat + " stat. Expected: integer 1 - 10. Got " + colTwoimgtext)
            colTwoimgtext = input("Please enter correct stat here:")    
        playerDict[colOneStat] = int(colOneimgtext)
        playerDict[colTwoStat] = int(colTwoimgtext)
    
    print(playerDict)
    return playerDict

mainIMG = cv2.imread("temp.PNG",cv2.IMREAD_UNCHANGED)
# getPicsOfNumberText(mainIMG)
# mainIMGcopy = mainIMG.copy()
# cleanedIMG = cleanImage(mainIMGcopy)
# getPlayerDict(1,cleanedIMG,mainIMG)
# getPlayerDict(2,cleanedIMG)


#color ranges for player names
#(22,22,22) and up
#it would be good to find egdes for this

#color ranges for yellow text
#(50,50,50) and up
