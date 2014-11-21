LeagueOracle
============

League Oracle is a project to build classifiers that can
predict the outcome of League of Legends games. 

#Here is gist of the process.

Using the riot api, we collect games.
Then we use the games to train classifiers.
Next users visit our website, and enter in the specifications for a game,
and the classifier returns a prediction.

##Dependicies
pybrain
riotwatcher - included 
mysql

##Setup
###Setup a mysql database.
Fill in the Creds.json file with the info for you database 
#Get a riot games dev key/s 
Fill in the Keys.txt file with the key/s
  
