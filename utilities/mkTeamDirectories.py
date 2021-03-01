import os

teams = ["Real Madrid","Rainmakers","Block Party","Full Court Press","Cover Kings","Supersonics","Republicans","Democrats","Hawks","Celtics","Bobcats","Bulls","Cavs","Mavericks","Nuggets","Pistons","Warriors","Rockets","Pacers","Clippers","Lakers","Grizzlies","Heat","Bucks","Timberwolves","Nets","Hornets","Knicks","Thunder","Magic","76ers","Suns","Trailblazers","Kings","Spurs","Raptors","Jazz","Wizards"]

def makeTeamDirectories():
    for team in teams:
        if not os.path.isdir("../headshots/"+team+"/"):
            os.mkdir("../headshots/"+team+"/")

makeTeamDirectories()