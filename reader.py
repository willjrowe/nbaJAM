import csv
from tweet import TweetMachine

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

team_completer = WordCompleter(["Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"])

teams = ["Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]
who_won_valid = False
DONT_SAVE = False
while not (who_won_valid):
    who_won = input("Who won: ")
    if who_won in "JjWw" and who_won != "":
        who_won_valid = True
    else:
        print("Invalid input! Please enter 'J' (Joseph) or 'W' (Will).")
num_ot_valid = False
while not (num_ot_valid):
    num_ot = input("How many OTs: ")
    if num_ot.isdigit():
        num_ot_valid = True
    else:
        print("Invalid input! Please enter a whole number.")
winner_score_valid = False
while not (winner_score_valid):
    winner_score = input("Winner Score: ")
    if winner_score.isdigit():
        winner_score_valid = True
    else:
        print("Invalid input! Please enter a whole number.")
loser_score_valid = False
while not (loser_score_valid):
    loser_score = input("Loser Score: ")
    if loser_score.isdigit():
        loser_score_valid = True
        if int(winner_score) <= int(loser_score):
            DONT_SAVE = True
            print("Error: Winner score is <= loser score. This data will not be added to the dataset. Please restart.")
            exit()
    else:
        print("Invalid input! Please enter a counting number.")
winner_team_valid = False
while not (winner_team_valid):
    winner_team = prompt('Winner Team: ', completer=team_completer,
              complete_while_typing=True)
    winner_team = winner_team.lower().capitalize()
    winner_team = list(winner_team)
    for i in range(1,len(winner_team)): #for full court press etc. multi name teams
        if winner_team[i].isspace():
            winner_team[i+1] = winner_team[i+1].upper()
    winner_team = "".join(winner_team)
    if winner_team in teams:
        winner_team_valid = True
    elif winner_team == "Teams":
        print("LIST OF TEAMS")
        for team in teams:
            print(team)
    else:
        print("Invalid input! Please enter a valid NBA team. For a list of teams type 'teams'.")
loser_team_valid = False
while not (loser_team_valid):
    loser_team = prompt('Loser Team: ', completer=team_completer,
              complete_while_typing=True)
    loser_team = loser_team.lower().capitalize()
    loser_team = list(loser_team)
    for i in range(1,len(loser_team)): #for full court press etc. multi name teams
        if loser_team[i].isspace():
            loser_team[i+1] = loser_team[i+1].upper()
    loser_team = "".join(loser_team)
    if loser_team in teams:
        loser_team_valid = True
    elif loser_team == "Teams":
        print("LIST OF TEAMS")
        for team in teams:
            print(team)
    else:
        print("Invalid input! Please enter a valid NBA team. For a list of teams type 'teams'.")
if (num_ot == "0"):
    otString = ""
elif (num_ot == "1"):
    otString = "-OT"
else:
    otString = "-" + num_ot + "OT"
#do the work
if not (DONT_SAVE):
    with open('NBA_JAM.csv', mode='a', newline='') as nba_file:
        nba_writer = csv.writer(nba_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if (who_won == "J"):
            josephScore = winner_score
            josephTeam = winner_team
            josephResult = "W" + otString
            willScore = loser_score
            willTeam = loser_team
            willResult = "L"
        else:
            willScore = winner_score
            willTeam = winner_team
            willResult = "W" + otString
            josephScore = loser_score
            josephTeam = loser_team
            josephResult = "L"
        nba_writer.writerow([josephTeam,josephResult,josephScore,willScore,willResult,willTeam])
    
    if ("W" in josephResult):
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
    if ("W" in josephResult):
        finalPhrase = "Joseph who played as the " + josephTeam + keyPhrase + " Will who played as the " + willTeam + " with a final score of " + josephScore + " - " + willScore 
    else:
        finalPhrase = "Will who played as the " + willTeam + keyPhrase + " Joseph who played as the " + josephTeam + " with a final score of " + willScore + " - " + josephScore
    gameReport = TweetMachine()
    #gameReport.makeATweet(finalPhrase)


