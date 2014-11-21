from LeagueCrawlerDB import LeagueCrawlerDB
import pprint
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.validation import ModuleValidator
import simplejson as json
import pickle
import sys


idmap = 0
class NeuralOracle:
    
    @staticmethod
    def loadIdMap():
        data = open("Champ_Data.json")
        data = json.loads(data.readline())
        data = data['data']
        index = 0
        map = {}
        for key in data:
            map[ data[key]['id'] ] = index
            index +=1
        return map
    
    @staticmethod
    def getIdMap():
        if idmap != 0:
            return idmap
        else:
            return NeuralOracle.loadIdMap()
            
    @staticmethod
    def createAndTrainNetwork(name):
        
        cred = open("DBCreds.json")
        cred = json.loads(cred.readline())
        LC = LeagueCrawlerDB(cred)
        
        map = NeuralOracle.getIdMap()
        maplen = len(map)
        
        rows = LC.getAllGames()
        ds = SupervisedDataSet(maplen * 2 , 1)
        count = 0
        entry = []
        for row in rows:
            entry = NeuralOracle.createEntry( row[13:] , map ) 
            ds.addSample( entry , [ int( row[2] ) ] ) 

        network = buildNetwork(maplen * 2 , maplen * 2 , 1 )
        trainer = BackpropTrainer(network, ds)
        trainer.train()
        NeuralOracle.saveNetwork( network , name )
       
    @staticmethod
    def createEntry( champs,  map ):
        maplen = len(map)
        entry = [False] * maplen * 2
        for i in range(0 , 5 ):
            if champs[i] != 0:
                entry[ map[ int(champs[i]) ] ] = True
        for i in range( 5 , 9 ):
            if champs[i] != 0:
                entry[ map[ int(champs[i]) ] + maplen ] = True
                    
        return entry
            
        
    
    @staticmethod
    def saveNetwork(net , name):
        fileObject = open(name, 'w')
        pickle.dump(net, fileObject)
        fileObject.close()
    
    @staticmethod
    def loadNetwork(name):
        fileObject = open(name,'r')
        net = pickle.load(fileObject)
        return net
    
    def __init__(self , name):
        self.net = NeuralOracle.loadNetwork(name)
    
    def predict(self, champs):
        entry = NeuralOracle.createEntry( champs , NeuralOracle.getIdMap() )
        return self.net.activate(entry)
        

def main():
    
    champs = sys.argv[1]
    champs = champs.split()
    print champs
    network = NeuralOracle("test-network")
    print NeuralOracle.getIdMap()
    print "The prediction is " + str(network.predict(champs))
    #NeuralOracle.createAndTrainNetwork("test-network")
    


if __name__ == "__main__":
    main()





   

