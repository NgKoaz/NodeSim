import simpy
from typing import Callable

from .DataCollection import DataCollection
from .Request import Request
from .Node import Node


# nodeManager: NodeManager, 
class Generator:
    def __init__(self, env: simpy.Environment,getInterArrivalTime: Callable, nodeStart: Node) -> None:
        self.env = env
        self.nodeStart = nodeStart
        self._getInterArrivalTime = getInterArrivalTime

    def run(self): 
        while True:
            newRequest = Request(self.env, self.nodeStart)
            self.env.process(newRequest.run())
            yield self.env.timeout(self._getInterArrivalTime())
            

    