# NBA-Statistics-Scraper

This web scraper is a current WIP that scrapes statistics off of https://stats.nba.com/.

# Current functionality:
Get dataframe of team's stats for a particular season. If no season input, defaults to all seasons.
Paramaters: team: string abbreviation of team (e.g.: OKC, SAS) season: string: XXXX-XX (e.g. 2009-10)

AllTeams.teamData(team, season='')


Creates CSV of team's overall stats for a particular season.
Paramters: same as teamData function

AllTeams.createCSV(team, season='')


Returns dataframe of a player's overall stats for a particular season
Parameters: name: string: (Last, First) e.g (Adams, Steven); season: string: XXXX-XX e.g. (2009-10)

AllPlayers.playerData(name, season)


Creates csv of player's overall stats for a particular season.
Parameters: same as playerData.

AllPlayers.createCSV(name, season)


# To come:

Team and player statistics by game.

Pre/Post-all star weekend statistics.

Scores for all NBA games by date.
