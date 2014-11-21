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
PyBrain Neural Network - Availible from [PyBrain](https://github.com/pybrain/pybrain) <br>
Python wrapper for MySQL - Tutorial for installing at http://zetcode.com/db/mysqlpython/ <br>
riotwatcher - Included in Repository but availible from [Pseudonym117](https://github.com/pseudonym117/Riot-Watcher) <br> 

####Setup
Setup a mysql database.<br>
Fill in the Creds.json file with the info for you database.<br> 
- You are to fill out each field that has a % in it. ""s Are provided to show where strings are expected in the host, user, password, and db fields. The port field only needs an integer.

Get a riot games dev key/s. Requires League of Legends Account. You can get these at the following links:<br>
- [League of Legends Account](https://signup.na.leagueoflegends.com/en/signup/index?realm_key=na) 
- [API Key](https://developer.riotgames.com/) 

Fill in the Keys.txt file with your API key and the program can be run. <br>
- For multiple kets delimit with spaces { "keys" : [ "%key1" , "%key2" , "%key3"] }
- If you only have one key be sure to in clude no commas { "keys" : [ "%key1"] }

Due to Riot API Rate limits you willl likely need to leave crawler running for some time togather enough data before classifiers can predict effictively.
  

League Oracle isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
