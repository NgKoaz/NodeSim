import random
from sim.Simulation import Simulation
from sim.NodeBuilder import NodeBuilder

random.seed(123)

nodeBuilder = NodeBuilder()
nodeBuilder.addNode(nodeId="Web Server", numResource=10, queueLength=10000, getServiceTime=lambda: 0.3)
nodeBuilder.addNode(nodeId="Application Server 1", numResource=4, queueLength=10000, getServiceTime=lambda: 2)
nodeBuilder.addNode(nodeId="Application Server 2", numResource=4, queueLength=10000, getServiceTime=lambda: 2)
nodeBuilder.addNode(nodeId="Application Server 3", numResource=4, queueLength=10000, getServiceTime=lambda: 2)
nodeBuilder.addNode(nodeId="Database", numResource=1, queueLength=10000, getServiceTime=lambda: 5)
nodeBuilder.addNode(nodeId="File System", numResource=1, queueLength=10000, getServiceTime=lambda: 5)


nodeBuilder.connect("Web Server", "", 0.5)
nodeBuilder.connect("Web Server", "Application Server 1", 0.2)
nodeBuilder.connect("Web Server", "Application Server 2", 0.2)
nodeBuilder.connect("Web Server", "Application Server 3", 0.1)

nodeBuilder.connect("Application Server 1", "Database", 0.4)
nodeBuilder.connect("Application Server 1", "Web Server", 0.6)

nodeBuilder.connect("Application Server 2", "Web Server", 1)

nodeBuilder.connect("Application Server 3", "File System", 0.5)
nodeBuilder.connect("Application Server 3", "Web Server", 0.5)

nodeBuilder.connect("Database", "Application Server 1", 1)

nodeBuilder.connect("File System", "Application Server 3", 1)

sim = Simulation(getInterArrivalTime=lambda: 0.05, nodeBuilder=nodeBuilder, nodeIdStart="Web Server")
sim.run(until=2000)

sim.print()






# Simulation
#   NodeManager
#       Nodes
#   Generator
#       Passenger