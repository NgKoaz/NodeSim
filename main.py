import numpy as np

from sim.Simulation import Simulation
from sim.DataCollection import DataCollection
from sim.NodeBuilder import NodeBuilder


np.random.seed(123)

nodeBuilder = NodeBuilder()
nodeBuilder.addNode(nodeId="Web Server", numResource=1000, queueLength=1000, getServiceTime=lambda: np.random.exponential(1.0 / 1))
nodeBuilder.addNode(nodeId="Application Server 1", numResource=400, queueLength=1000, getServiceTime=lambda: np.random.exponential(1.0 / 1))
nodeBuilder.addNode(nodeId="Application Server 2", numResource=400, queueLength=1000, getServiceTime=lambda: np.random.exponential(1.0 / 1))
nodeBuilder.addNode(nodeId="Database", numResource=1000, queueLength=1000, getServiceTime=lambda: np.random.exponential(1.0 / 2))
nodeBuilder.addNode(nodeId="File System", numResource=1000, queueLength=1000, getServiceTime=lambda: np.random.exponential(1.0 / 2))


nodeBuilder.connect("Web Server", "", 0.5)
nodeBuilder.connect("Web Server", "Application Server 1", 0.3)
nodeBuilder.connect("Web Server", "Application Server 2", 0.2)

nodeBuilder.connect("Application Server 1", "Database", 0.4)
nodeBuilder.connect("Application Server 1", "Web Server", 0.6)

nodeBuilder.connect("Application Server 2", "File System", 0.5)
nodeBuilder.connect("Application Server 2", "Web Server", 0.5)

nodeBuilder.connect("Database", "Application Server 1", 1)

nodeBuilder.connect("File System", "Application Server 2", 1)

sim = Simulation(getInterArrivalTime=lambda: np.random.poisson(1.0 / 50), nodeBuilder=nodeBuilder, nodeIdStart="Web Server")
sim.run(until=2000)


dataCollection = DataCollection.getInstance()

for nodeName in dataCollection.getNodeNameList():
    print("=============================Node name: ", nodeName, "================================")
    print("Mean of waiting time: ", dataCollection.getMeanWaitingTime(nodeName))
    print("Mean of service time: ", dataCollection.getMeanServiceTime(nodeName))
    print("Mean of number request in queue: ", dataCollection.getMeanNumberInQueue(nodeName))
    print("Mean of Arrival Request in queue: ", dataCollection.getMeanArrivalRequest(nodeName))
    print("Mean of Throughput in queue: ", dataCollection.getMeanThroughput(nodeName))
    print("Mean of Utilization in queue: ", dataCollection.getMeanUtilization(nodeName))
print("Total request out of system: ", dataCollection.getTotalRequestLeaveSystem())    


