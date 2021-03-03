import cv2
import pytesseract
import numpy as np
from os import path
from skimage.metrics import structural_similarity
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
import json

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

team_completer = WordCompleter(["Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"])

teams = ["Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]

master_stats_file = open('master_stats.json',) 
master_stats = json.load(master_stats_file)

LIST_OF_NUMS = ["1","2","3","4","5","6","7","8","9","10"]

def getSimilarity(A,B) -> float:
    print(cv2.matchTemplate(A,B))

def getAllPlayerDicts(image):
    for i in range(1,3):
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
    else:
        print("Player photo already exists.")
        user_response = input("Add player anyways? Input y or otherwise input n")
        if user_response == "n":
            return
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




