import simpy
from typing import Callable


from .Generator import Generator
from .NodeManager import NodeManager
from .NodeBuilder import NodeBuilder
from .DataCollection import DataCollection

class Simulation:
    def __init__(self, getInterArrivalTime: Callable, nodeBuilder: NodeBuilder, nodeIdStart: str) -> None:
        self.env = simpy.Environment()
        self._nodeManager = NodeManager(self.env, nodeBuilder)
        self._generator = Generator(self.env, getInterArrivalTime, self.getNodeStart(nodeIdStart))
        self._prepare()

    def getNodeStart(self, nodeIdStart: str):
        nodeStart = self._nodeManager.getNodeById(nodeIdStart)
        if nodeStart == None: 
            raise Exception("NodeStartId is not found!")
        return nodeStart

    def _prepare(self) -> None:
        self.env.process(self._generator.run())

    def run(self, until):
        self.env.run(until=until)
        DataCollection.getInstance().recordTotalSimulationDuration(self.env.now)

