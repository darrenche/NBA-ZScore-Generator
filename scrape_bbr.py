# Credit to Sam Morehouse for the getPlayers() scraping function, github: smorehouse

# Pip install bs4 and requests into a dir w/ this file. 
# Zip that, upload it to aws for a new lambda. 
# I run this daily for weekly/biweekly/monthly deltas, 
# or atleast that's the idea right now :) 

from bs4 import BeautifulSoup
import requests
import boto3
import datetime
import statistics

s3 = boto3.resource('s3')
now = datetime.datetime.now()

def lambda_handler(event, context):

    bucket = 'daily-player-data'
    file_name = "player_data-" + now.strftime("%Y%m%d") + ".json"
    s3_path = "data/" + file_name

    s3.Bucket(bucket).put_object(Key=s3_path, Body=json.dumps(getPlayers()))

    return {
        'statusCode': 200,
        'body': 'SUCCESS - '+file_name
    }

# Credit to Sam Morehouse for this function
# Web Scraper for Basketball Reference to acquire 2018-2019 NBA Statistics of each player
def getPlayers():
    allNbaPlayers = []
    page = requests.get("https://www.basketball-reference.com/leagues/NBA_2019_totals.html")
    soup = BeautifulSoup(page.content, 'html.parser')
    players = soup.findAll("tr", {"class":"full_table"})
    for player in players:
        player_link = player.findAll("td", {"data-stat": "player"})
        player_games_played = player.findAll("td", {"data-stat": "g"})
        player_minutes_played = player.findAll("td", {"data-stat": "mp"})
        player_pts = player.findAll("td", {"data-stat": "pts"})
        player_rebs = player.findAll("td", {"data-stat": "trb"})
        player_asts = player.findAll("td", {"data-stat": "ast"})

        player_fg = player.findAll("td", {"data-stat": "fg_pct"})
        player_ft = player.findAll("td", {"data-stat": "ft_pct"})
        player_3pt = player.findAll("td", {"data-stat": "fg3"})
        player_blk = player.findAll("td", {"data-stat": "blk"})
        player_stl = player.findAll("td", {"data-stat": "stl"})

        for i in player_link:
            player = {
                #link is like /players/f/foo01.html, we only want foo01.
                "id": player_link[0].find('a')['href'].split('/')[3].split('.')[0], 
                "player": player_link[0].text,
                "g": player_games_played[0].text,
                "mp": player_minutes_played[0].text,
                "pts": player_pts[0].text,
                "trb": player_rebs[0].text,
                "ast": player_asts[0].text,
                "fg_pct": player_fg[0].text,
                "ft_pct": player_ft[0].text,
                "3ptm": player_3pt[0].text,
                "blk": player_blk[0].text,
                "stl": player_stl[0].text
            }
            allNbaPlayers.append(player)

    return allNbaPlayers


"""
Returns a JSON containing the corresponding total z-score of every player in the NBA
"""
def calculateZscore():
    playerList = getPlayers()
    categories = ["pts", "trb", "ast", "fg_pct", "ft_pct", "3ptm", "blk", "stl"]

    """
    *** zscoreJSON ***
    key/value pair of "bbr_id" : "z-score"
    - key represents the id according to basketball reference
    - value is the total z-score which is calculated by adding the respective z-scores the following categories: fg%, ft%, 3PTM, PTS, REB, AST, STL, BLK 
    """
    zscoreJSON = {}

    # Do this process for every player in the NBA
    for player in playerList:
        zscoreJSON[player['id']] = 0.0

    # For each of the eight categories, we will calculate the individual z-scores of that specific category for each respective player
    for category in categories:
        # temporary list that holds all of the data of a specific category
        categoryData = []
        
        for player in playerList:
            # for the cases in which the web scraper returned an empty string
            if player[category] == '':
                player[category] = '0'
            categoryData.append(float(player[category]))

        # used calculate the mean and standard deviations that will be used for calculating the z-score
        arithmetic_mean = statistics.mean(categoryData)
        standard_deviation_population = statistics.pstdev(categoryData)

        # update the playerList JSON object with the z-scores of each of the eight categories (fg%, ft%, 3PTM, PTS, REB, AST, STL, BLK)
        for index, item in enumerate(categoryData):
            # z-score calculation
            zscore = (item - arithmetic_mean) / standard_deviation_population
            # update in our original player list JSON
            playerList[index].update({category + '_score' : str(zscore)})
            # also update in the total z-score JSON
            tempInt = float(zscoreJSON[playerList[index]['id']])
            tempInt += zscore
            zscoreJSON[playerList[index]['id']] = str(tempInt)

    # for printing & debugging purposes
    # for player in playerList:
    #     print(player)
    #     print("\n ---------------------------\n")
    # print(zscoreJSON)

    return zscoreJSON

# print(calculateZscore())