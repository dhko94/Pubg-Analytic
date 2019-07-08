import pandas as pd
import calendar
from pubg_python import PUBG, Shard
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
import multiprocessing as mp

api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwYjAyNTFiMC0yZWZhLTAxMzctNTFhZi0xOTIyZDBiYzFkMzIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUzMjc3NTE4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IndoZXJlIn0.dTn2NwSPzkvOUZjKGvd4XmILXzdJWZXKDUbzcqZ21GU'


class pubgData():
	def __init__(self, name):
		self.name = name
		self.api = PUBG(api_token, Shard.PC_NA)

		# Player Data:
		self.playerMatchDetail = self._getMatchDetail((self.api.players().filter(player_names=[self.name])[0]).matches)
		self.playerDF = self._getDF(self.playerMatchDetail)

	def f(self, x):
		return self.api.matches().get(x.id)

	def _getMatchDetail(self, lofMatchID):
		with mp.Pool(processes = mp.cpu_count()) as pool:
			answer = pool.map(self.f, lofMatchID)

		pool.close()

		return answer

	def g(self, x):
		answer = {
			'matchID' : None,
			'createdAt' : None,
			'mapName' : None,
			'name' : None,
			'gameMode' : None,
			'duration' : None,
			'rank' : None,
			'kills': None,
			'longestKill' : None,
			'headshotKills' : None,
			'assists' : None,
			'damageDealt' : None,
			'timeSurvived' : None,
			'timeSurvivedMIN' : None,
			'endedAt' : None,
			'date' : None,
			'enemy' : None,
			'ally' : None
		}

		answer['matchID'] = x.id
		answer['createdAt'] = datetime.strptime(x.attributes['createdAt'], "%Y-%m-%dT%H:%M:%SZ")

		tempName = x.attributes['mapName']
		
		if tempName == 'Erangel_Main': answer['mapName'] = 'Erangel'
		elif tempName == 'Desert_Main': answer['mapName'] = 'Miramar'
		elif tempName == 'Savage_Main': answer['mapName'] = 'Sanhok'
		elif tempName == 'Range_Main': answer['mapName'] = 'Practice'
		elif tempName == 'DihorOtok_Main': answer['mapName'] = 'Vikendi'
		else: answer['mapName'] = 'Unknown'

		answer['gameMode'] = x.attributes['gameMode']
		answer['duration'] = x.attributes['duration']

		enemy = []
		for roster in x.rosters:
			temp_team = []

			for participant in roster.participants:
				temp_team.append(participant.name)
				if participant.name == self.name:
					answer['name'] = participant.name
					answer['rank'] = roster.attributes['stats']['rank']
					answer['kills'] = participant.attributes['stats']['kills']
					answer['longestKill'] = participant.attributes['stats']['longestKill']
					answer['headshotKills'] = participant.attributes['stats']['headshotKills']
					answer['assists'] = participant.attributes['stats']['assists']
					answer['damageDealt'] = participant.attributes['stats']['damageDealt']
					answer['timeSurvived'] = participant.attributes['stats']['timeSurvived']

					answer['timeSurvivedMIN'] = float(format(Decimal(answer['timeSurvived'] / 60), '.2f'))
					answer['endedAt'] = answer['createdAt'] + timedelta(seconds = answer['timeSurvived'])
					answer['date'] = str(answer['createdAt'].month) + "-" + str(answer['createdAt'].day)

			if self.name in temp_team: answer['ally'] = temp_team
			else: enemy += temp_team

		answer['enemy'] = enemy

		return answer

	def _getDF(self, matchDetails):
		with mp.Pool(processes = mp.cpu_count()) as pool:
			answer = pool.map(self.g, matchDetails)

		pool.close()

		return pd.DataFrame(answer)

	def _filterBy(self, df, type):
		game = {}
		for element in set(df[type]):
			game[element] = len(df[df[type] == element])

		return game

	def _getPIE(self, df):
		return [['gmaeMode', 'Number of Games']] + [[k,v] for k, v in self._filterBy(df, 'gameMode').items()]

	def _getBAR(self, df):
		return [['mapName', 'Count']] + [[k,v] for k, v in self._filterBy(df, 'mapName').items()]

	def _getSCATTER(self, df):
		return [['timeSurvived', 'kills']] + df[['timeSurvivedMIN', 'kills']].values.tolist()

	def _getLINE(self, df):
		df = df[df['gameMode'] != 'practice']
		data = [['Date', 'kills_assists', 'damageDealt', 'headshotKills']]

		split = df.groupby(df['date'])
		for each in split:
			temp = []
			temp.append(each[0])

			temp.append(sum(list(each[1].kills + each[1].assists)) / len(each[1]))
			temp.append((sum(list(each[1].damageDealt)) / len(each[1]))/100)
			# headshotKills
			if sum(list(each[1].headshotKills)) == 0: temp.append(0)
			elif sum(list(each[1].kills)) == 0: temp.append(10)
			else: temp.append((sum(list(each[1].headshotKills)) / sum(list(each[1].kills))) * 10)

			data.append(temp)

		return data

	def _getGANTT(self, df):
		data = list(df.apply(lambda row: [row.date, row.createdAt.hour, row.createdAt.minute, row.endedAt.hour, row.endedAt.minute], axis = 1))
		data = data[::-1]
		for i in range(len(data)):
		    if data[i][1] > data[i][3]:
		        data[i] = [data[i][0], data[i][1], data[i][2], data[i][1], 59]

		return data

	def _getSNIPE(self, df):
		test = df[
			(df['gameMode'] == 'solo')		|
			(df['gameMode'] == 'duo') 		|
			(df['gameMode'] == 'squad') 	|
			(df['gameMode'] == 'solo-fpp')	|
			(df['gameMode'] == 'duo-fpp') 	|
			(df['gameMode'] == 'squad-fpp')
		]

		dicTotal = {}
		for index, row in test.iterrows():
			for single in row.enemy:
				if single in dicTotal: dicTotal[single] += [index]
				else: dicTotal[single] = [index]

		dicTotal = {k : v for (k, v) in dicTotal.items() if len(v) >= 3}
		
		temp = {}
		for k, v in dicTotal.items():
			count = 0
			for i in range(1, len(v)):
				if v[i] - v[i - 1] <= 2: count += 1

			if count >= 2: temp[k] = v

		dicTotal = temp
		data = [['Player Name', 'List of Match Date']]
		for k, v in dicTotal.items():
			data.append([k, [str(df.iloc[x].createdAt) for x in v][::-1]])

		return data
