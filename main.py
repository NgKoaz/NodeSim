import random
from sim.Simulation import Simulation
from sim.NodeBuilder import NodeBuilder

random.seed(123)

nodeBuilder = NodeBuilder()
nodeBuilder.addNode("Web Server", 4, 200000, lambda: 5)
nodeBuilder.addNode("Application Server 1", 8, 400000, lambda: 5)
nodeBuilder.addNode("Application Server 2", 4, 300000, lambda: 10)

nodeBuilder.connect("Web Server", "Application Server 1", 0.1)
nodeBuilder.connect("Web Server", "Application Server 2", 0.9)



sim = Simulation(getInterArrivalTime=lambda: 0.5, nodeBuilder=nodeBuilder, nodeIdStart="Web Server")
sim.run(until=20000)

sim.print()






# Simulation
#   NodeManager
#       Nodes
#   Generator
#       Passenger