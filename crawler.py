import time
import sys, traceback
import logging
from LeagueCrawlerDB import LeagueCrawlerDB
from riotwatcher import RiotWatcher, NORTH_AMERICA
import riotwatcher
import pprint
import thread
import simplejson as json

included_games = [
    'NORMAL',					# Summoner's Rift unranked games
    'NORMAL_3x3',				# Twisted Treeline unranked games
    'ODIN_UNRANKED',			# Dominion/Crystal Scar games
    'ARAM_UNRANKED_5v5',		# ARAM / Howling Abyss games
    'RANKED_SOLO_5x5',			# Summoner's Rift ranked solo queue games
    'RANKED_TEAM_3x3',			# Twisted Treeline ranked team games
    'RANKED_TEAM_5x5',			# Summoner's Rift ranked team games
    'ONEFORALL_5x5',			# One for All games
    'CAP_5x5',					# Team Builder games
    'URF',						# Ultra Rapid Fire games
]



DBLock = thread.allocate_lock()
PrintLock = thread.allocate_lock()

#waits some time to get more requests 
def waitForRequest(RW):
	while not RW.can_make_request():
		time.sleep(1)
		
	
def convertLeague(league, division):
	sum = 0
	if league == 'BRONZE':
		sum = 0
	if league == 'SILVER':
		sum = 5
	if league == 'GOLD':
		sum = 10
	if league == 'PLATINUM':
		sum = 15
	if league == 'DIAMOND':
		sum = 20
	if league == 'MASTER':
		sum = 25
	if league == 'CHALLENGER':
		sum = 30
		
	if division == 'V':
		sum += 1
	if division == 'IV':
		sum += 2
	if division == 'III':
		sum += 3
	if division == 'II':
		sum += 4
	if division == 'I':
		sum += 5
	return sum
	
def getElos(playerIDs , RW , name):
	result = {}
	waitForRequest(RW)
	raw_data = {}
	while raw_data == {}:
		try:
			raw_data = RW.get_league(summoner_ids = playerIDs)
			break
		except riotwatcher.LoLException as e:
                        with PrintLock:
			   print e.error
			if e.error == "Game data not found":
		      		raw_data = {} #get_league returns error 404 when no summoners have league. This should not break program though.
				break
		        else:
			   with PrintLock:
			      print name + " had an error in getElos assuming I out of api calls waiting 10 min"
			   init = time.time()
			   while (time.time() - init) < 600:
			      time.sleep(60)			
				


	for player in playerIDs:
		if not raw_data.has_key(str(player)):
			result[player] = 0
		else:
			for person in raw_data[str(player)][0]['entries']:
				if str(person['playerOrTeamId']) == str(player):
					result[player] = convertLeague(str(raw_data[str(player)][0]['tier']), str(person['division']))
			if not result.has_key(player):
				result[player] = 0
	return result			
	
#this is a super ugly algorithm
def getMatchesOfPlayer(playerID , RW , name):
	
	# need to put error check
        waitForRequest(RW)
	raw_data = {}
	while raw_data == {}:
		try:
			raw_data = RW.get_recent_games(playerID)
			break
		except:
		   with PrintLock:
		      print name + " had an error in getMatches assuming I out of api calls waiting 10 min"
		   init = time.time()
		   while (time.time() - init) < 600:
		      time.sleep(60)
		   count = count + 1 
	games_data = []
	ids = []
	for game in raw_data['games']:
		dataDict = {}
		dataDict['gameID'] = game['gameId']
		
		#Only interested games where match making keeps teams even
		if game['subType'] not in included_games:
			continue
		dataDict['queueType'] = game['subType']
		
		#winner check
		if (game['stats']['win'] and game['teamId'] == 100) or (not game['stats']['win'] and game['teamId'] == 200):
			dataDict['Winner'] = 100
		else:
			dataDict['Winner'] = 200
		
		#player elos request+
		
		ids = []
		ids.append(playerID)
		for player in game['fellowPlayers']:
			ids.append(player['summonerId'])
	
		eloDict = getElos(ids , RW , name)		
		
		#get owner of report
		i1 = 1
		i2 = 1
		if game['teamId'] == 100:
			dataDict['Champ_T1_P1'] = game['championId']
			dataDict['Elo_T1_P1'] = eloDict[playerID]
			i1 += 1
		else:
			dataDict['Champ_T2_P1'] = game['championId']
			dataDict['Elo_T2_P1'] = eloDict[playerID]
			i2 += 1
		#get teammates and opponents
		for player in game['fellowPlayers']:
			index = ''
			if player['teamId'] == 100:
				index = 'T1_P' + str(i1) 
				i1 += 1
			else:
				index = 'T2_P' + str(i2)
				i2 += 1
			
			dataDict['Champ_' + index] = player['championId']
			dataDict['Elo_' + index] = eloDict[player['summonerId']]
		
		games_data.append(dataDict)
	return (games_data, ids)
	
def thread_fun(name , RW ,LeagueCrawlerDB):
	# init_players = [21590342,21556676,19949496,24272491,21019602,\
					# 24912984,47826257,23481155,51007806,23575033,\
					# 48588677,20299025,39149175,307568,25106179,27710956,\
					# 23820400,21265930,24328639,25024201,29315097,30730901,\
					# 37739368,28375372] 
	# #LeagueCrawlerDB.addPlayers(init_players)
	
	#logging.basicConfig(filename='error.log', level=logging.DEBUG)
	
    while(True):
        ripe_players = []
        try:
            with DBLock:
                ripe_players = LeagueCrawlerDB.getRipePlayers(10)
                LeagueCrawlerDB.updatePlayers(ripe_players)
            games = []
            players = []
            for id in ripe_players:
				 with PrintLock:
					print name + " is doing " + str(id[0])
				 temp = getMatchesOfPlayer(id[0] , RW, name)
				 games.extend(temp[0])
				 players.extend(temp[1])
            with DBLock:	
				val = LeagueCrawlerDB.addGames(games)
				LeagueCrawlerDB.addPlayers(players)
            with PrintLock:
				print str(name) + ' Sent'
				print "The number of new games "  + str(val)
        except Exception as e:
			with PrintLock:
				print e
				print name + " had an error assuming I out of api calls waiting 10 min"
			init = time.time()
	
			while (time.time() - init) < 600:
				 time.sleep(60)
			



def main():
    
    
    cred = open(sys.argv[1])
    cred = json.loads(cred.readline())
    RWS  = open(sys.argv[2])
    RWS  = json.loads(RWS.readline())['keys']
    RWS = [ RiotWatcher( str ( x ) ) for x in RWS ]
            
    LC = LeagueCrawlerDB( cred ) 
    try:
        count = 1
        for RW in RWS:
            thread.start_new_thread( thread_fun , ( "Thread " + str(count) , RW , LC) )
            count += 1
    except:
	print "Error making thread"
    while 1:
        pass


if __name__ == '__main__':
    main()
