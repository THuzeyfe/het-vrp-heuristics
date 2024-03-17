import numpy as np
from copy import copy, deepcopy

class ConstructiveHeuristic:
    def __init__(self, CustomerManager, Fleet):
        self.cm = deepcopy(CustomerManager)
        self.fleet = deepcopy(Fleet)
        self.clusters =dict()
        self.totalClusterDemands = dict()
        
    def run(self, isPrint=False):
        self.BuildClusters()
        self.BuildRoutes()
        if isPrint:
            self.printClusters()
            self.fleet.printVehicleRoutes()
        return self.fleet
       
        
    def BuildClusters(self):
        ClusterNumber = 0
        
        arcs = self.cm.sortArcs()    
        
        for arc in arcs:
            if arc[0] == 0 or arc[1] == 0:
                continue
            elif arc[0] in self.clusters.keys() and arc[1] in self.clusters.keys():
                continue
            elif arc[0] in self.clusters.keys():
                cCluster = self.clusters[arc[0]]
                if (self.totalClusterDemands[cCluster][0]+self.cm.get_demands(arc[1])[0]<=self.fleet.maxCapacity()[0]) \
                & (self.totalClusterDemands[cCluster][1]+self.cm.get_demands(arc[1])[1]<=self.fleet.maxCapacity()[1]):
                    self.totalClusterDemands[cCluster][0] += self.cm.get_demands(arc[1])[0]
                    self.totalClusterDemands[cCluster][1] += self.cm.get_demands(arc[1])[1]
                    self.clusters[arc[1]] = cCluster
                    continue
            elif arc[1] in self.clusters.keys():
                cCluster = self.clusters[arc[1]]
                if (self.totalClusterDemands[cCluster][0]+self.cm.get_demands(arc[0])[0]<=self.fleet.maxCapacity()[0]) \
                & (self.totalClusterDemands[cCluster][1]+self.cm.get_demands(arc[0])[1]<=self.fleet.maxCapacity()[1]):
                    self.totalClusterDemands[cCluster][0] += self.cm.get_demands(arc[0])[0]
                    self.totalClusterDemands[cCluster][1] += self.cm.get_demands(arc[0])[1]
                    self.clusters[arc[0]] = cCluster
                    continue 
            elif(self.cm.get_demands(arc[0])[0]+self.cm.get_demands(arc[1])[0]<=self.fleet.maxCapacity()[0]) \
            & (self.cm.get_demands(arc[0])[1]+self.cm.get_demands(arc[1])[1]<=self.fleet.maxCapacity()[1]):
                ClusterNumber += 1
                self.clusters[arc[0]] = ClusterNumber
                self.clusters[arc[1]] = ClusterNumber
                self.totalClusterDemands[ClusterNumber] = [self.cm.get_demands(arc[0])[0]+self.cm.get_demands(arc[1])[0], \
                                                           self.cm.get_demands(arc[0])[1]+self.cm.get_demands(arc[1])[1]]
            else:
                ClusterNumber +=1
                self.clusters[arc[0]] = ClusterNumber
                self.totalClusterDemands[ClusterNumber] = [self.cm.get_demands(arc[0])[0], self.cm.get_demands(arc[0])[1]]
                ClusterNumber +=1
                self.clusters[arc[1]] = ClusterNumber
                self.totalClusterDemands[ClusterNumber] = [self.cm.get_demands(arc[1])[0], self.cm.get_demands(arc[1])[1]]
                
    def printClusters(self):
        for key in self.totalClusterDemands:
            nodes = self.getCluster(key)
            print("Cluster #" +str(key) + " has " + str(self.totalClusterDemands[key][0]) + \
                  " kg and " + str(self.totalClusterDemands[key][1]) + " liters of total demands, and for customers: " \
                  + str(nodes))
            
    def getCluster(self, cluster):
        nodes = []
        for key2 in self.clusters:
            if(self.clusters[key2]==cluster):
                nodes.append(key2)
        return nodes
        
            
    def BuildRoutes(self):
        for key, demand in self.totalClusterDemands.items():
            customers  = self.getCluster(key)
            
            for customer in customers:
                self.fleet.assignVehicle(self.cm, [customer])
                
            arcs = self.cm.sortArcs(customers)
            
            for arc in arcs:
                if self.fleet.isLast(customers[arc[0]]) & self.fleet.isFirst(customers[arc[1]]):
                    vehicle1 = self.fleet.getAssignedVehicletoCustomer(customers[arc[0]])
                    vehicle2 = self.fleet.getAssignedVehicletoCustomer(customers[arc[1]])
                    if vehicle1 != vehicle2:
                        self.fleet.mergeVehicles(vehicle1, vehicle2, customers[arc[0]], self.cm,  reverse=False)
                    del vehicle1, vehicle2
                elif self.fleet.isLast(customers[arc[1]]) & self.fleet.isFirst(customers[arc[0]]):
                    vehicle1 = self.fleet.getAssignedVehicletoCustomer(customers[arc[1]])
                    vehicle2 = self.fleet.getAssignedVehicletoCustomer(customers[arc[0]])
                    if vehicle1 != vehicle2:
                        self.fleet.mergeVehicles(vehicle1, vehicle2, customers[arc[1]], self.cm, reverse=False)
                    del vehicle1, vehicle2
                elif self.fleet.isLast(customers[arc[0]]) & self.fleet.isLast(customers[arc[1]]):
                    vehicle1 = self.fleet.getAssignedVehicletoCustomer(customers[arc[0]])
                    vehicle2 = self.fleet.getAssignedVehicletoCustomer(customers[arc[1]])
                    if vehicle1 != vehicle2:
                        self.fleet.mergeVehicles(vehicle1, vehicle2, customers[arc[0]], self.cm, reverse=True)
                    del vehicle1, vehicle2
                elif self.fleet.isFirst(customers[arc[0]]) & self.fleet.isFirst(customers[arc[1]]):
                    vehicle1 = self.fleet.getAssignedVehicletoCustomer(customers[arc[0]])
                    vehicle2 = self.fleet.getAssignedVehicletoCustomer(customers[arc[1]])
                    if vehicle1 != vehicle2:
                        self.fleet.mergeVehicles(vehicle1, vehicle2, 0, self.cm, reverse=True)
                    del vehicle1, vehicle2
            