import simpy
import random
from typing import Callable, Optional
from .DataCollection import DataCollection

class Node:
    def __init__(self, env: simpy.Environment, nodeId: str, numResource: int, queueLength: int, getServiceTime: Callable) -> None:
        self.env = env
        self._nodeId = nodeId
        self._resources = simpy.Resource(env, numResource)
        self._queueLength = queueLength
        self._getServiceTime = getServiceTime
        self._network = []

    def connect(self, node: 'Node', prob: float) -> None:
        self._network.append((node, prob))
    
    def getNodeId(self) -> str:
        return self._nodeId

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

    def getServiceTime(self):
        mu = self._getServiceTime()
        DataCollection.getInstance().recordServiceTime(self._nodeId, mu)
        return mu
    
    def onRequestEnqueue(self):
        DataCollection.getInstance().recordNumInQueue(self._nodeId, self.env.now, self.getNumWaiting())

    def onRequestDequeue(self):
        DataCollection.getInstance().recordNumInQueue(self._nodeId, self.env.now, self.getNumWaiting())
        DataCollection.getInstance().recordUsingResources(self._nodeId, self.env.now, self._resources.count / self._resources.capacity)

    def onRequestArrive(self):
        DataCollection.getInstance().recordArrivalRequest(self._nodeId)

    def onRequestLeave(self):
        DataCollection.getInstance().recordLeavingRequest(self._nodeId)
        DataCollection.getInstance().recordUsingResources(self._nodeId, self.env.now, self._resources.count / self._resources.capacity)

    def printAllEdges(self):
        for n in self._network:
            print(n)