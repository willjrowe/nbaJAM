import json

teams = ["Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]

team_dict = { i : dict() for i in teams }

json_object = json.dumps(team_dict) 

with open("master_stats.json", "w") as outfile: 
    outfile.write(json_object) 