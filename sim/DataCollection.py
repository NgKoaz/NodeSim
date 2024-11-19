import numpy as np
from typing import List

class Data:
    def __init__(self):
        self.numInQueue = []
        self.waitingTime = []
        self.serviceTime = []
        self.numberArrivalRequest = 0
        self.numberLeavingRequest = 0
        self.utilization = []


class DataCollection:
    _instance = None

    def __init__(self):
        self.dataList = {}
        self.totalRequestLeaveSystem = 0
        self.totalSimDuration = 1


    @staticmethod
    def getInstance():
        if DataCollection._instance == None:
            DataCollection._instance = DataCollection()
        return DataCollection._instance
        
    def _getDataOfNode(self, nodeId: str) -> Data:
        if self.dataList.get(nodeId) is None:
            self.dataList[nodeId] = Data()
        return self.dataList[nodeId]

    def recordServiceTime(self, nodeId: str, serviceTime: float) -> None:
        self._getDataOfNode(nodeId).serviceTime.append(serviceTime)

    def recordWaitingTime(self, nodeId: str, waitingTime: float) -> None:
        self._getDataOfNode(nodeId).waitingTime.append(waitingTime)

    def recordNumInQueue(self, nodeId: str, time: float, numInQueue: float) -> None:
        self._getDataOfNode(nodeId).numInQueue.append((time, numInQueue))

    def recordArrivalRequest(self, nodeId: str) -> None:
        self._getDataOfNode(nodeId).numberArrivalRequest += 1

    def recordLeavingRequest(self, nodeId: str) -> None:
        self._getDataOfNode(nodeId).numberLeavingRequest += 1

    def recordUsingResources(self, nodeId: str, time: float, numUsingResource: float) -> None:
        self._getDataOfNode(nodeId).utilization.append((time, numUsingResource))

    def recordTotalSimulationDuration(self, totalSimDuration: float) -> None:
        self.totalSimDuration = totalSimDuration

    def onRequestLeaveSystem(self) -> None:
        self.totalRequestLeaveSystem += 1

    def getTotalRequestLeaveSystem(self) -> int:
        return self.totalRequestLeaveSystem

    def getNodeNameList(self) -> List[str]:
        return self.dataList.keys()
    
    def getMeanWaitingTime(self, nodeId: str) -> float:
        return np.mean(self._getDataOfNode(nodeId).waitingTime)
    
    def getMeanServiceTime(self, nodeId: str) -> float:
        return np.mean(self._getDataOfNode(nodeId).serviceTime)

    def _calculateMeanByTime(self, data):
        totalWeightedQueueTime = 0
        for i in range(len(data) - 1):
            timeStart, queueStart = data[i]
            timeEnd, _ = data[i + 1]

            deltaT = timeEnd - timeStart
            totalWeightedQueueTime += queueStart * deltaT

        return totalWeightedQueueTime / self.totalSimDuration

    def getMeanNumberInQueue(self, nodeId: str) -> float:
        data = self._getDataOfNode(nodeId).numInQueue
        return self._calculateMeanByTime(data)
    
    def getMeanArrivalRequest(self, nodeId: str) -> float:
        return self._getDataOfNode(nodeId).numberArrivalRequest / self.totalSimDuration
    
    def getMeanThroughput(self, nodeId: str) -> float:
        return self._getDataOfNode(nodeId).numberLeavingRequest / self.totalSimDuration

    def getMeanUtilization(self, nodeId: str) -> float:
        data = self._getDataOfNode(nodeId).utilization 
        return self._calculateMeanByTime(data)

