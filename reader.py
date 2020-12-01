import csv

teams = ["Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]
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
    winner_team = input("Winner Team: ")
    winner_team = winner_team.lower().capitalize()
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
    loser_team = input("Loser Team: ")
    loser_team = loser_team.lower().capitalize()
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
    with open('NBA_JAM_copy.csv', mode='a', newline='') as nba_file:
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