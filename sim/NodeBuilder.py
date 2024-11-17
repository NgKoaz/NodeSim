import simpy
from typing import Callable

from .Node import Node


class NodeBuilder:
    def __init__(self):
        self._nodes = {}
        self._edges = []

    def build(self, env: simpy.Environment):
        nodes = {nodeId: Node(env, nodeId, numResource, queueLength, getServiceTime) for (nodeId, numResource, queueLength, getServiceTime) in self._nodes.values()}
        for (startNodeId, endNodeId, prob) in self._edges:
            startNode = nodes[startNodeId]
            endNode = nodes[endNodeId]
            startNode.connect(endNode, prob)
        return nodes

    def addNode(self, nodeId: str, numResource: int, queueLength: int, getServiceTime: Callable) -> None:
        self._nodes[nodeId] = (nodeId, numResource, queueLength, getServiceTime)
        
    def connect(self, startNodeId: str, endNodeId: str, prob: float):
        self._edges.append((startNodeId, endNodeId, prob))

