import simpy
from typing import List

from .Node import Node
from .NodeBuilder import NodeBuilder

class NodeManager:
    def __init__(self, env: simpy.Environment, nodeBuilder: NodeBuilder) -> None:
        self.env = env
        self._nodes = nodeBuilder.build(env)

    def getNodes(self):
        return self._nodes

    def getNodeById(self, nodeId: str) -> Node:
        return self._nodes[nodeId]
