import csv

with open('NBA_JAM.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            print("A quick recap of every game lol")
            line_count+=1
        else:
            josephTeam = row[0]
            josephWon = row[1].__contains__("W")
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
            line_count += 1
    print(f'Processed {line_count} lines.')