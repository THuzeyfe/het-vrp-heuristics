import numpy as np
import random
from copy import copy, deepcopy
import math


class AntColony_v2:
    def __init__(self, CustomerManager, Fleet):
        self.cm = deepcopy(CustomerManager)
        self.fleet = deepcopy(Fleet)
        self.pheromones = dict()
        
    def run(self, nAnt, evaporation=0.8, stop=20, alpha=1, beta=0, fitness='g', isPrint=False):
        
        n = self.cm.getCustomers()
        C1, C2 = self.fleet.maxCapacity()
        bestCost = math.inf
        
        if fitness=='g':
            FitnessFunc = self.GeometricFitness
        elif fitness=='a':
            FitnessFunc = self.ArithmeticFitness
        else:
            raise("Unknown fitness. Fitness can be 'g' or 'a'.")
        
        customers = list(range(1,n))
        allNodes = [0] + customers
        
        Nodes = [(i,j) for i in allNodes for j in allNodes if i!=j]
        arcs = [(i, j) for i in Nodes for j in Nodes if i != j and i[1]==j[0]]
        
        
        
        for arc in arcs:
            self.pheromones[arc] = 1
            
        population = [deepcopy(self.fleet) for i in range(nAnt)]
        nonImp=0
         
        while(nonImp<stop):
            improved=False
            for ant in range(nAnt):
                remainings = customers.copy()                
                curNode = random.choice([i for i in Nodes if i[0]==0])
                
                route = [curNode[0], curNode[1]]
                remainings.remove(curNode[1])
                population[ant].assignVehicle(self.cm, [curNode[1]])
                veh = population[ant].getAssignedVehicletoCustomer(curNode[1])
                curC1 = C1 - self.cm.get_demands(curNode[1])[0]
                curC2 = C2 - self.cm.get_demands(curNode[1])[1]

                while(len(remainings)>0):
                    if route[-1] == 0:
                        S = [i for i in Nodes if i[0]==0 and i[1] in remainings]
                        tmpNode = random.choices(S, weights=[FitnessFunc(curNode,j,alpha,beta) for j in S])[0]
                        curNode = tmpNode
                        route.append(curNode[1])
                        remainings.remove(curNode[1])
                        population[ant].assignVehicle(self.cm, [curNode[1]])
                        veh = population[ant].getAssignedVehicletoCustomer(curNode[1])                        
                        curC1 = C1 - self.cm.get_demands(curNode[1])[0]
                        curC2 = C2 - self.cm.get_demands(curNode[1])[1]
                    else:
                        eligibles = self.cm.getFeasibleSpace(curC1, curC2, [0]+remainings)
                        S = [i for i in Nodes if i[0]==curNode[1] and i[1] in eligibles]                        
                        tmpNode = random.choices(S, weights=[FitnessFunc(curNode,j,alpha,beta) for j in S])[0]
                        if tmpNode[1]!=0:
                            population[ant].vehicles[veh].addCustomer(tmpNode[1], tmpNode[0] ,self.cm, justAfter=True)
                            remainings.remove(tmpNode[1])
                        curNode = tmpNode
                        route.append(curNode[1])                        
                        curC1 = curC1 - self.cm.get_demands(curNode[1])[0]
                        curC2 = curC2 - self.cm.get_demands(curNode[1])[1]
                        
                
                tmpCost = population[ant].totalCost()
                if bestCost > tmpCost:
                    self.fleet = deepcopy(population[ant])
                    bestCost = self.fleet.totalCost()
                    improved=True

            
            for i in range(len(route)-2):
                self.pheromones[(route[i],route[i+1]), (route[i+1],route[i+2])] += 1 / math.log(tmpCost, n)
                
            self.pheromones.update({k: evaporation*v for k, v in self.pheromones.items()})
            
            if improved is False:
                nonImp += 1
            
        if isPrint:
            self.fleet.printVehicleRoutes()
        return self.fleet
    
    def ArithmeticFitness(self, node1, node2, pAlpha, pBeta): 
        return self.pheromones[node1, node2]*pAlpha+(1/self.cm.get_arc(node2[0],node2[1]))*pBeta
    
    def GeometricFitness(self, node1, node2, pAlpha, pBeta):
        return self.pheromones[node1, node2]**pAlpha*(1/self.cm.get_arc(node2[0],node2[1]))**pBeta 
    
    
