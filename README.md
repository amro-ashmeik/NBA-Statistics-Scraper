# NBA-Statistics-Scraper

This python web scraper is a current WIP that scrapes statistics off of https://stats.nba.com/.

# Required python libraries:
Pandas:
https://pandas.pydata.org/

Requests:
http://docs.python-requests.org/en/master/

Selenium(only required once to gather player ID's and names)
http://selenium-python.readthedocs.io/

JSON:
https://docs.python.org/2/library/json.html

CSV:
https://docs.python.org/2/library/csv.html

# Current functionality:
Get dataframe of team's stats for a particular season. If no season input, defaults to all seasons.
Paramaters: team: string abbreviation of team (e.g.: OKC, SAS) season: string: XXXX-XX (e.g. 2009-10)

AllTeams.teamData(team, season='')


Creates CSV of team's overall stats for a particular season.
Parameters: same as teamData function

AllTeams.createCSV(team, season='')


Returns dataframe of a player's overall stats for a particular season
Parameters: name: string: (Last, First) e.g (Adams, Steven); season: string: XXXX-XX e.g. (2009-10)

AllPlayers.playerData(name, season)


Creates csv of player's overall stats for a particular season.
Parameters: same as playerData.

AllPlayers.createCSV(name, season)


#Creates CSV of player names and ID's.

AllPlayers.nameIdCSV():


#Returns a dataframe of all player's box stats for a particular date and season.
#Parameters: season as string(e.g. '2017-18'); date as string(e.g. '03/02/2018' = 'mm/dd/year')

AllPlayers.box(season, date)


#Returns dataframe of a player's box stats for each game in a particular season.
#Parameters: name: string: (Last, First) e.g (Adams, Steven); season: string: XXXX-XX e.g. (2009-10)

AllPlayers.playerbox(name, season)



# To come:

Team and player statistics by game.

Pre/Post-all star weekend statistics.

Scores for all NBA games by date.

and more...
