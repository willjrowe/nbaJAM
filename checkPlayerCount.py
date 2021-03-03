import csv
import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

team_completer = WordCompleter(["NBA Street","Nimble Ninjas","Honey Badgers","Vancouver Stickman","Team EA","SSX","Beastie Boys","Athens Panathinaikos","Maccabi Electra","Siena Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"])

teams = ["NBA Street","Nimble Ninjas","Honey Badgers","Vancouver Stickman","Team EA","SSX","Beastie Boys","Athens Panathinaikos","Maccabi Electra","Siena Montepaschi","Dunk Champs","Sad Pandas","Fast Breaks","Dime Droppers","Angry Mascots","Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]

while True:
    team_valid = False
    while not (team_valid):
        team = prompt('Team to check: ', completer=team_completer,
                complete_while_typing=True)
        team = team.lower().capitalize()
        team = list(team)
        for i in range(1,len(team)): #for full court press etc. multi name teams
            if team[i].isspace():
                team[i+1] = team[i+1].upper()
        team = "".join(team)
        if team in teams:
            team_valid = True
        elif team == "Teams":
            print("LIST OF TEAMS")
            for team in teams:
                print(team)
        else:
            print("Invalid input! Please enter a valid NBA team. For a list of teams type 'teams'.")
    path, dirs, files = next(os.walk("./headshots/"+team))
    file_count = len(files)
    print(team + " has " + str(file_count) + " players")