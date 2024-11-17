import simpy
from .Node import Node
from .DataCollection import DataCollection


class Request:
    NextId = 0

    def __init__(self, env: simpy.Environment, nodeStart: Node, dataCollection: DataCollection) -> None:
        self.env = env
        self.currentNode = nodeStart
        # Statistical Data
        self.tempData = {}
        self.dataCollection = dataCollection
        self.dataCollection.request["TotalRequest"] += 1

    def run(self):
        self.tempData["StartTime"] = self.env.now
        while self.currentNode != None and not self.currentNode.isFull():
            with self.currentNode.getResources().request() as req:
                yield req
                mu = self.currentNode.getServiceTime()
                yield self.env.timeout(mu) 

            self.currentNode.onRequestDone()
            self.currentNode = self.currentNode.nextNode()

        self.tempData["EndTime"] = self.env.now
        if self.currentNode == None:
            self.dataCollection.request["ResponseTime"].append(self.tempData["EndTime"] - self.tempData["StartTime"])
            self.dataCollection.request["NumCompleted"] += 1
        else:
            self.dataCollection.request["NumRejected"] += 1