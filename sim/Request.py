import simpy
from .Node import Node
from .DataCollection import DataCollection


class Request:
    NextId = 0

    def __init__(self, env: simpy.Environment, nodeStart: Node) -> None:
        self.env = env
        self.currentNode = nodeStart

    def run(self):
        while self.currentNode != None:
            self.currentNode.onRequestArrive()
            if self.currentNode.isFull(): 
                break
            startWaitingTime = self.env.now
            with self.currentNode.getResources().request() as req:
                self.currentNode.onRequestEnqueue()
                yield req
                endWaitingTime = self.env.now
                self.currentNode.onRequestDequeue()
                yield self.env.timeout(self.currentNode.getServiceTime()) 
                
            self.currentNode.onRequestLeave()

            DataCollection.getInstance().recordWaitingTime(self.currentNode.getNodeId(), endWaitingTime - startWaitingTime)
            self.currentNode = self.currentNode.nextNode()
