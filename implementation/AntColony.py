import numpy as np
import random
from copy import copy, deepcopy
import math


class AntColony:
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
        
        arcs = [(i, j) for i in allNodes for j in allNodes if i != j]
        
        
        
        for arc in arcs:
            self.pheromones[arc] = 1
            
        population = [deepcopy(self.fleet) for i in range(nAnt)]
        nonImp=0
         
        while(nonImp<stop):
            improved=False
            for ant in range(nAnt):
                remainings = customers.copy()

                route = [0]

                while(len(remainings)>0):
                    if route[-1] == 0:
                        curNode = random.choices(remainings, weights=[FitnessFunc(0,j,alpha,beta) for j in remainings])[0]
                        route.append(curNode)
                        remainings.remove(curNode)
                        population[ant].assignVehicle(self.cm, [curNode])
                        veh = population[ant].getAssignedVehicletoCustomer(curNode)
                        curC1 = C1 - self.cm.get_demands(curNode)[0]
                        curC2 = C2 - self.cm.get_demands(curNode)[1]
                    else:
                        S = self.cm.getFeasibleSpace(curC1, curC2, [0]+remainings)
                        tmpNode = random.choices(S, weights=[FitnessFunc(curNode,j,alpha,beta) for j in S])[0]
                        if tmpNode!=0:
                            population[ant].vehicles[veh].addCustomer(tmpNode, curNode ,self.cm, justAfter=True)
                            remainings.remove(tmpNode)
                        curNode = tmpNode
                        route.append(curNode)                        
                        curC1 = curC1 - self.cm.get_demands(curNode)[0]
                        curC2 = curC2 - self.cm.get_demands(curNode)[1]
                    
                
                tmpCost = population[ant].totalCost()
                if bestCost > tmpCost:
                    self.fleet = deepcopy(population[ant])
                    bestCost = self.fleet.totalCost()
                    improved=True

            
            for i in range(len(route)-1):
                self.pheromones[route[i],route[i+1]] += 1 / math.log(tmpCost, n)
                
            self.pheromones.update({k: evaporation*v for k, v in self.pheromones.items()})
            
            if improved is False:
                nonImp += 1

            
        if isPrint:
            self.fleet.printVehicleRoutes()
        return self.fleet
    
    def ArithmeticFitness(self, node1, node2, pAlpha, pBeta):
        return self.pheromones[node1, node2]*pAlpha+(1/self.cm.get_arc(node1,node2))*pBeta
    
    def GeometricFitness(self, node1, node2, pAlpha, pBeta):
        return self.pheromones[node1, node2]**pAlpha*(1/self.cm.get_arc(node1,node2))**pBeta
    
