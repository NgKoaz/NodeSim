import simpy
import random
from typing import Callable, Optional

class Node:
    def __init__(self, env: simpy.Environment, nodeId: str, numResource: int, queueLength: int, getServiceTime: Callable) -> None:
        self.env = env
        self._nodeId = nodeId
        self._resources = simpy.Resource(env, numResource)
        self._queueLength = queueLength
        self.getServiceTime = getServiceTime
        self._network = []

        # Statistical Data  
        self.servedNum = 0

    def connect(self, node: 'Node', prob: float) -> None:
        self._network.append((node, prob))
    
    def getResources(self) -> simpy.Resource:
        return self._resources

    def getNumWaiting(self) -> int:
        return len(self._resources.queue)

    def getTotalInside(self) -> int:
        return self._resources.count + self.getNumWaiting()
    
    def isFull(self): 
        return self._queueLength <= self.getNumWaiting()


    def nextNode(self) -> Optional['Node']:
        randNum = random.random()
        floor = 0
        for (node, prob) in self._network:
            if floor <= randNum and randNum <= floor + prob:
                return node
            floor += prob
        return None

    def onRequestDone(self):
        self.servedNum += 1


    def printAllEdges(self):
        for n in self._network:
            print(n)