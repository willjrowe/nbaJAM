import csv, statistics

josephTeamArray = []
josephWonArray = []
josephScoreArray = []
willScoreArray = []
willTeamArray = []
numOTArray = []
scoreDiffArray = []

with open('NBA_JAM.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("A quick recap of every game lol")
            line_count+=1
        elif line_count == 1:
            line_count+=1
        else:
            josephTeam = row[0]
            josephWon = row[1].__contains__("W")
            numOT = 0
            if ("-OT" in row[1] or "-OT" in row[4]):
                numOT = 1
            elif("OT" in row[1]):
                numOT = row[1][2]
            elif("OT" in row[4]):
                numOT = row[4][2]
            josephScore = row[2]
            willScore = row[3]
            willTeam = row[5]
            if (josephWon):
                scoreDifferential = int(josephScore) - int(willScore)
            else:
                scoreDifferential = int(willScore) - int(josephScore)
            keyPhrase = " narrowly defeated"
            if (scoreDifferential > 5):
                keyPhrase = " solidly beat"
            if (scoreDifferential > 9):
                keyPhrase = " blew out"
            if (scoreDifferential > 13):
                keyPhrase = " completely dominated"
            if (scoreDifferential > 20):
                keyPhrase = " straight embarassed"
            if (josephWon):
                finalPhrase = "Joseph who played as the " + josephTeam + keyPhrase + " Will who played as the " + willTeam + " with a final score of " + josephScore + " - " + willScore 
            else:
                finalPhrase = "Will who played as the " + willTeam + keyPhrase + " Joseph who played as the " + josephTeam + " with a final score of " + willScore + " - " + josephScore
            print(finalPhrase)
            josephTeamArray.append(josephTeam)
            josephWonArray.append(josephWon)
            josephScoreArray.append(int(josephScore))
            willScoreArray.append(int(willScore))
            willTeamArray.append(willTeam)
            numOTArray.append(int(numOT))
            scoreDiffArray.append(int(scoreDifferential))
            line_count += 1
    gamesPlayed = len(josephScoreArray)
    avgScoreDiff = sum(scoreDiffArray) / gamesPlayed
    josephWins = josephWonArray.count(True)
    josephLosses = gamesPlayed - josephWins
    willWins = josephLosses
    willLosses = josephWins
    josephTotalScore = sum(josephScoreArray)
    willTotalScore = sum(willScoreArray)
    josephAVGScore = josephTotalScore / gamesPlayed
    willAVGScore = willTotalScore / gamesPlayed
    josephWinScore = 0
    willWinScore = 0
    josephLongestWinStreak = 0
    willLongestWinStreak = 0
    josephMaxLongestWin = 0
    willMaxLongestWin = 0
    josephScoreStD = statistics.stdev(josephScoreArray)
    willScoreStD = statistics.stdev(willScoreArray)
    for result in josephWonArray:
        if result:
            josephLongestWinStreak+=1
            if (willLongestWinStreak>willMaxLongestWin):
                willMaxLongestWin = willLongestWinStreak
            willLongestWinStreak=0
        else:
            willLongestWinStreak+=1
            if (josephLongestWinStreak>josephMaxLongestWin):
                josephMaxLongestWin = josephLongestWinStreak
            josephLongestWinStreak=0
    if (josephLongestWinStreak>josephMaxLongestWin):
        josephMaxLongestWin = josephLongestWinStreak
    if (willLongestWinStreak>willMaxLongestWin):
        willMaxLongestWin = willLongestWinStreak 
    josephBiggestLoss = 0
    willBiggestLoss = 0
    for i in range(0,len(josephWonArray)):
        if josephWonArray[i]:
            josephWinScore += scoreDiffArray[i]
            if scoreDiffArray[i] > willBiggestLoss:
                willBiggestLoss = scoreDiffArray[i]
        else:
            willWinScore += scoreDiffArray[i]
            if scoreDiffArray[i] > josephBiggestLoss:
                josephBiggestLoss = scoreDiffArray[i]
    josephAVGWinScore = josephWinScore / josephWins
    willAVGWinScore = willWinScore / willWins
    totalTimePlayed = gamesPlayed * 12 + sum(numOTArray) * 3
    totalTimePlayedHours = totalTimePlayed / 60
    totalScoreArray = []
    for i in range(0,len(josephScoreArray)):
        totalScoreArray.append(josephScoreArray[i] + willScoreArray[i])
    print("Games played: " + str(gamesPlayed))
    print("Total time played: " + str(totalTimePlayed) + " minutes or " + str(totalTimePlayedHours) + " hours")
    print("Joseph's Record: " + str(josephWins) + "-" + str(josephLosses) + "  (" + str(josephWins/gamesPlayed) + ")")
    print("Will's Record: " + str(willWins) + "-" + str(willLosses) + "  (" + str(willWins/gamesPlayed) + ")")
    print("Joseph Total Score: " + str(josephTotalScore))
    print("Will Total Score: " + str(willTotalScore))
    if (josephTotalScore == willTotalScore):
        print("Total score tied. That's crazy!")
    elif (josephTotalScore > willTotalScore):
        scoreDifferential = josephTotalScore - willTotalScore
        print("Joseph has scored " + str(scoreDifferential) + " more points than Will.")
    else:
        scoreDifferential = willTotalScore - josephTotalScore
        print("Will has scored " + str(scoreDifferential) + " more points than Joseph.")
    print("Joseph's Longest Win Streak: " + str(josephMaxLongestWin))
    print("Will's Longest Win Streak: " + str(willMaxLongestWin))
    print("Joseph AVG Score: " + str(josephAVGScore))
    print("Joseph's Score Standard Deviation: " + str(josephScoreStD))
    print("Will AVG Score: " + str(willAVGScore))
    print("Will's Score Standard Deviation: " + str(willScoreStD))
    if (josephAVGScore == willAVGScore):
        print("Tied AVG score too obviously")
    elif (josephAVGScore > willAVGScore):
        print("Joseph scores " + str(josephAVGScore - willAVGScore) + " more points on average than Will.")
    else:
        print("Will scores " + str(willAVGScore - josephAVGScore) + " more points on average than Joseph.")
    print("Average game score differential: " + str(avgScoreDiff))
    print("When Joseph wins he wins by " + str(josephAVGWinScore) + " points on average.")
    print("When Will wins he wins by " + str(willAVGWinScore) + " points on average.")
    print("Highest total scoring game: " + str(max(totalScoreArray)))
    print("Lowest total scoring game: " + str(min(totalScoreArray)))
    print("Joseph's highest scoring game: " + str(max(josephScoreArray)))
    print("Joseph's lowest scoring game: " + str(min(josephScoreArray)))
    print("Will's highest scoring game: " + str(max(willScoreArray)))
    print("Will's lowest scoring game: " + str(min(willScoreArray)))
    print("Joseph's biggest win: " + str(willBiggestLoss))
    print("Will's biggest win: " + str(josephBiggestLoss))
    josephTeamsDict = {}
    willTeamsDict = {}
    for i in range(0,len(josephWonArray)):
        joTeam = josephTeamArray[i]
        willTeam = willTeamArray[i]
        if josephWonArray[i]:
            #joseph won with this team
            if willTeam in willTeamsDict:
                willTeamsDict[willTeam]["losses"]+=1
            else:
                willTeamsDict[willTeam] = {"wins":0,"losses":1}
            if joTeam in josephTeamsDict:
                josephTeamsDict[joTeam]["wins"]+=1
            else:
                 josephTeamsDict[joTeam] = {"wins":1,"losses":0}
        else:
            #will won with this team
            if willTeam in willTeamsDict:
                willTeamsDict[willTeam]["wins"]+=1
            else:
                willTeamsDict[willTeam] = {"wins":1,"losses":0}
            if joTeam in josephTeamsDict:
                josephTeamsDict[joTeam]["losses"]+=1
            else:
                 josephTeamsDict[joTeam] = {"wins":0,"losses":1}
    print("Joseph's Team Dict: "+str(josephTeamsDict))
    print("Will's Team Dict: "+str(willTeamsDict))