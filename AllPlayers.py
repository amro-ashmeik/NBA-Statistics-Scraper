from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import csv
import os
from os.path import normpath, basename
import pandas as pd
import requests
import json

#Creates CSV of player names and ID's.
def nameIdCSV():

	#Open Firefox and go to url
	driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe')
	driver.get('https://stats.nba.com/players/list/')

	#Open csv file and write headers.
	csv_file = open('PlayerNameandIDs.csv', 'w')
	writer = csv.writer(csv_file)
	writer.writerow(['Player Name', 'Player ID'])

	#Grabs list of player names and ID's.
	playerlist = driver.find_elements_by_class_name('players-list__name')

	#Dictionary of player names and ID's.
	players = {}

	for player in playerlist:
		#Player ID is within href.
		fullLink = player.find_element_by_tag_name('a').get_attribute('href')
		id = basename(normpath(fullLink))

		#Player name is within <a> text.
		name = player.find_element_by_tag_name('a').text
		players[name] = id

	#Write player name and ID into rows of csv.
	for k,v in players.items():
		writer.writerow([k, v])

	csv_file.close()


#Returns dataframe of a player's overall stats for a particular season
#Parameters: name: string: (Last, First) e.g (Adams, Steven); season: string: XXXX-XX e.g. (2009-10)
def playerData(name, season):

	df = pd.read_csv('PlayerNameandIDs.csv')

	playerID = df.loc[df['Player Name'] == name, 'Player ID'].iloc[0]
	
	#Url of the JSON file
	url = 'https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=' + str(playerID) + '&PlusMinus=N&Rank=N&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision='

	#Headers to prevent hanging
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

	#Convert formatting
	raw = requests.get(url, headers=headers)
	data = raw.json()

	#Open csv file and write headers.
	filename = name + 'stats.csv'
	csv_file = open(filename, 'w')
	writer = csv.writer(csv_file)
	writer.writerow(data['resultSets'][0]['headers'])

	for row in data['resultSets'][0]['rowSet']:
		writer.writerow(row)

	csv_file.close()


	df2 = pd.read_csv(filename)

	os.remove(filename)
	return df2

#Creates csv of player's overall stats for a particular season.
#Parameters: same as playerData.
def createCSV(name, season):

	df = playerData(name, season)

	df.to_csv(name + ' stats.csv')

#Returns a dataframe of all player's box stats for a particular date and season.
#Paramaters: season as string(e.g. '2017-18'); date as string(e.g. '03/02/2018' = 'mm/dd/year')
def box(season, date):

	#Url of the JSON file
	
	url = 'https://stats.nba.com/stats/playergamelogs?DateFrom=' + date + '&DateTo=' + date + '&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision='

	#Headers to prevent hanging
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

	#Convert to JSON formatting
	raw = requests.get(url, headers=headers)
	data = raw.json()

	#Open csv file and write headers.
	fdate = date.replace("/", "")
	filename = fdate + ' playerboxdata.csv'
	csv_file = open(filename, 'w')
	writer = csv.writer(csv_file)
	writer.writerow(data['resultSets'][0]['headers'])

	#Writes stats for each season (row).
	for row in data['resultSets'][0]['rowSet']:
		writer.writerow(row)

	csv_file.close()


	df = pd.read_csv(filename)

	temp = [0, 1, 3, 5, 6]
	rmcols = list(range(32, 64)) + temp

	df = df.drop(df.columns[rmcols], axis = 1)

	os.remove(filename)
	return df

#Returns dataframe of a player's box stats for each game in a particular season.
#Parameters: name: string: (Last, First) e.g (Adams, Steven); season: string: XXXX-XX e.g. (2009-10)
def playerbox(name, season):

	df = pd.read_csv('PlayerNameandIDs.csv')

	playerID = df.loc[df['Player Name'] == name, 'Player ID'].iloc[0]

	#Url of the JSON file
	url = 'https://stats.nba.com/stats/playergamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerID=' + str(playerID) + '&PlusMinus=N&Rank=N&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision='

	#Headers to prevent hanging
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

	#Convert to JSON formatting
	raw = requests.get(url, headers=headers)
	data = raw.json()

	#Open csv file and write headers.
	filename = name + season + ' boxdata.csv'
	csv_file = open(filename, 'w')
	writer = csv.writer(csv_file)
	writer.writerow(data['resultSets'][0]['headers'])

	#Writes stats for each season (row).
	for row in data['resultSets'][0]['rowSet']:
		writer.writerow(row)

	csv_file.close()


	df = pd.read_csv(filename)

	temp = [0, 1, 3, 5, 6]
	rmcols = list(range(32, 64)) + temp

	df = df.drop(df.columns[rmcols], axis = 1)

	#Changing date type from int to datetime.
	df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])

	os.remove(filename)
	return df