LeagueOracle
============

League Oracle is a project to build classifiers that can
predict the outcome of League of Legends games. 

####The Process

1. Using Riot API to collect game data. Availible [Here](https://developer.riotgames.com/) 
2. Use game data to train classifiers.
3. Users view LeagueOracle.html to provide new game data.
4. Use classifiers to preict winning side.

####Dependicies
pybrain - Availible from [PyBrain](https://github.com/pybrain/pybrain) <br>
python wrapper for mysql - Tutorial for installing at http://zetcode.com/db/mysqlpython/ <br>
riotwatcher - Included in Repository but availible from [Pseudonym117](https://github.com/pseudonym117/Riot-Watcher) <br> 

####Setup
Setup a mysql database.<br>
Fill in the Creds.json file with the info for you database.<br> 
Get a riot games dev key/s. Requires League of Legends Account, but one can be created for free.<br>
- [League of Legends Account](https://signup.na.leagueoflegends.com/en/signup/index?realm_key=na) 
- [API Key Availible at](https://developer.riotgames.com/) 

Fill in the Keys.txt file with your keys and the program can be run. <br>
Due to Riot API Rate limits you willl likely need to leave crawler running for some time togather enough data before classifiers can predict effictively.
  
