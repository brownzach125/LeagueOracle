import matplotlib.pyplot as plt
import MySQLdb
import time
import datetime
import numpy as np

class LeagueCrawlerDB:
  
    def __init__(self , cred):
        self.cred = cred
        self.db = self.getConnection()
        
    def getConnection(self):
        cred = self.cred
        db = MySQLdb.connect( host   = cred['host']   , user = cred['user'], \
                              passwd = cred['passwd'] , db   = cred['db'], \
                              port   = cred['port']                                ) 
        
        return db

    
    def execute(self, command_str ):
        while(1):
            try:
                cur = {}
                cur = self.db.cursor()
                cur.execute( command_str )
                self.db.commit( )
                break
            except:
                self.db = self.getConnection()
        return cur
        
    
    def getAllGamesWith(self, character_id ):
        command_str = "SELECT * FROM Games WHERE " 
        
        for i in range(1,5):
            command_str += " Champ_T1_P" + str(i) + " = " + str(character_id) + " OR"
            command_str += " Champ_T2_P" + str(i) + " = " + str(character_id) + " OR "
        
        command_str += " Champ_T1_P" + "5 = " + str(character_id) + " OR "
        command_str += " Champ_T2_P" + "5 = " + str(character_id)
        
        cur =  self.execute(command_str)
        row = cur.fetchall()
        return row 
    
    
    def updatePlayers(self,playerlist):
        
        str_command = "UPDATE Players SET LASTUSED = CASE id "
        for player in playerlist:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            str_command += " WHEN " + str(player[0]) + " THEN " \
                                    + "\'" + st + "\'" + " "
        str_command += " ELSE LASTUSED END WHERE id IN ( "
        for player in playerlist: 
            str_command += " " + str(player[0]) + " , "
        str_command += " -1 )"
        
        self.execute(str_command)
        
    def addPlayers(self,playerlist):
       
	str_command = "SELECT ID FROM Players"
        already_exist =  self.execute(str_command).fetchall()
        already_exist = [ row[0] for row in already_exist ]
        newplayers = []
        for player in playerlist:
            if player not in already_exist and player not in newplayers:
                newplayers.append( player )
         
        command_str = "INSERT INTO Players VALUES "
        length = len(newplayers)
        count = 1 
        if newplayers: 
          for player in newplayers:
              if count < length:
                command_str += " ( " + str(player) + " , \' 2000-01-24 00:00:00 \' ) ,"
              else:
                command_str += " ( " + str(player) + " , \' 2000-01-24 00:00:00 \' ) " 
              count = count + 1
        
        self.execute(command_str)
       
    def getRipePlayers(self,amount):
       	str_command = "SELECT * FROM (SELECT id, LASTUSED FROM Players order by LASTUSED LIMIT " + \
                       str(amount) + " ) F WHERE 1" 
        return self.execute(str_command).fetchall()
    
    def getBadEntries(self,amount):
        str_command = "SELECT gameID FROM Games WHERE Champ_T2_P1 = 0 LIMIT " + str(amount) 
        return self.execute(str_command).fetchall()
    
    def fixBadEntries(self,list):
        for entry in list:
            id = entry[0]
            value = entry[1]
            str_command = "UPDATE Games SET Champ_T2_P1 = " + str(value) + " WHERE gameID = " + str(id)
            self.execute(str_command)
    
    def getAllPlayersID(self):
        str_command = "SELECT id FROM Players"
        return self.execute(str_command).fetchall()
    
    def getAllGamesID(self):
        str_command = "SELECT gameID FROM Games"
        return self.execute(str_command).fetchall()

        
    def getAllGames(self):
        str_command = "SELECT * FROM Games"
        return self.execute(str_command).fetchall()    
        
    def addGames(self, gamelist ):
        
        newgames = []
        if gamelist:
            str_command = "SELECT gameID FROM Games" 
            already_exist = self.execute(str_command).fetchall()
            
            already_exist = [ row[0] for row in already_exist ]
            newgames = []
            newgamesID = []
            for dict in gamelist:
                if dict['gameID'] not in already_exist and dict['gameID'] not in newgamesID:
                    newgames.append( dict )
                    newgamesID.append( dict['gameID'] )
            
            columns = [ 'gameID' ,  'queueType' , 'Winner' , 'Elo_T2_P1' , \
                        'Elo_T2_P2' , 'Elo_T2_P3' ,  'Elo_T2_P4' , 'Elo_T2_P5' , 'Elo_T1_P1' , \
                        'Elo_T1_P2' , 'Elo_T1_P3' ,  'Elo_T1_P4' , 'Elo_T1_P5' , 'Champ_T1_P1' , \
                        'Champ_T1_P2', 'Champ_T1_P3' , 'Champ_T1_P4' , 'Champ_T1_P5' , \
                        'Champ_T2_P1', 'Champ_T2_P2' , 'Champ_T2_P3', 'Champ_T2_P4' ,\
                        'Champ_T2_P5' ] 
            
            command_str = "INSERT INTO Games VALUES "
            count = 1
            length = len(newgames)
            if newgames: 
              for game in newgames:
                  value = " ( "
                  for key in columns:
                    entry = 0
                    if key in game:
                        entry = game[key]
                    if key is 'queueType':
                        entry = "\'"+game[key]+"\'"
                    if key != 'Champ_T2_P5':                           
                        value += str(entry) + " , "
                    else:
                        value += str(entry) + " " 
                  
                  if count < length:
                    command_str += value + " ) , "
                  else:
                    command_str += value + " ) "
                  count = count + 1
              cur = self.execute(command_str).fetchall()
    	return len(newgames)

    


def main():
    pass


if __name__ == "__main__":
    main()


        
