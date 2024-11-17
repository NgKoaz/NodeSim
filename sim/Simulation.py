import simpy
from typing import Callable
import numpy as np


from .Generator import Generator
from .NodeManager import NodeManager
from .NodeBuilder import NodeBuilder
from .DataCollection import DataCollection

# , 
class Simulation:
    def __init__(self, getInterArrivalTime: Callable, nodeBuilder: NodeBuilder, nodeIdStart: str) -> None:
        self.env = simpy.Environment()
        self._dataCollection = DataCollection()
        self._nodeManager = NodeManager(self.env, nodeBuilder)
        self._generator = Generator(self.env, getInterArrivalTime, self.getNodeStart(nodeIdStart), self._dataCollection)
        self._prepare()

    def getNodeStart(self, nodeIdStart: str):
        nodeStart = self._nodeManager.getNodeById(nodeIdStart)
        if nodeStart == None: 
            raise Exception("NodeStartId is not found!")
        return nodeStart

    def _prepare(self) -> None:
        self.env.process(self._generator.run())

    def print(self):
        nodes = self._nodeManager.getNodes()
        for node in nodes.values():
            print("Served Request: ", node.servedNum, "| Still waiting: ", node.getNumWaiting())

        print("TOTAL REQUEST: ", self._dataCollection.request["TotalRequest"])
        print("TOTAL COMPLETED REQUEST: ", self._dataCollection.request["NumCompleted"])
        print("TOTAL REJECTED REQUEST: ", self._dataCollection.request["NumRejected"])
        print("MEAN RESPONSE TIME: ", np.mean(self._dataCollection.request["ResponseTime"]))

    def run(self, until):
        self.env.run(until=until)

