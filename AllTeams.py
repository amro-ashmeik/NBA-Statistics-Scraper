import csv
import requests
import json
import pandas as pd
import os

allTeams = {'ATL': 1610612737, 'BOS': 1610612738, 'BKN': 1610612751, 'CHA': 1610612766, 'CHI': 1610612741, 
'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765, 'GSW': 1610612744, 'HOU': 1610612745, 
'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763, 'MIA': 1610612748, 'MIL': 1610612749, 
'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752, 'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755,
'PHX': 1610612756, 'POR': 1610612757, 'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761, 'UTA': 1610612762, 'WAS': 1610612764}

#Get dataframe of team's stats for a particular season. If no season input, defaults to all seasons.
#Paramaters: team: string abbreviation of team (e.g.: OKC, SAS) season: string: XXXX-XX (e.g. 2009-10)
def teamData(team, season=''):

	id = allTeams[team]

	#Url of the JSON file
	url = 'https://stats.nba.com/stats/leaguegamefinder?Conference=&DateFrom=&DateTo=&Division=&DraftNumber=&DraftRound=&DraftYear=&GB=N&LeagueID=00&Location=&Outcome=&PlayerOrTeam=T&Season=' + season + '&SeasonType=&StatCategory=PTS&TeamID=' + str(id) + '&VsConference=&VsDivision=&VsTeamID='

	#Headers to prevent hanging
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

	#Convert to JSON formatting
	raw = requests.get(url, headers=headers)
	data = raw.json()

	#Open csv file and write headers.
	filename = team + 'stats.csv'
	csv_file = open(filename, 'w')
	writer = csv.writer(csv_file)
	writer.writerow(data['resultSets'][0]['headers'])

	#Writes stats for each season (row).
	for row in data['resultSets'][0]['rowSet']:
		writer.writerow(row)

	csv_file.close()


	df = pd.read_csv(filename)

	#Changing date type from int to datetime.
	df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])

	os.remove(filename)
	return df

#Creates CSV of team's overall stats for a particular season.
#Paramters: same as teamData function
def createCSV(team, season=''):

	df = teamData(team, season)
	df.to_csv(team + 'stats.csv')