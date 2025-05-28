from model.model import Model

myModel = Model()
myModel.getTeamsOfYear(2015)
myModel.buildGraph(2015)
myModel.printGraphDetails()

start= myModel.getRandomNode()
path,score=myModel.getBestPathV2(start)
print(len(path),score)

