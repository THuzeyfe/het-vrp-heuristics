import numpy as np
from copy import copy, deepcopy
import random

class DecomposedGenetic:
    def __init__(self, CustomerManager, Fleet):
        self.cm = deepcopy(CustomerManager)
        self.fleet = deepcopy(Fleet)
        self.clusters =dict()
        self.totalClusterDemands = dict()
        self.population = dict()
        self.fitnessValues = dict()
        
    def run(self, n, tournamentSize=3, eliteSize=1, stopCon = 50, isPrint=False):
        self.BuildClusters(n,tournamentSize, eliteSize, stopCon)
        self.BuildRoutes()
        if isPrint:
            self.printClusters()
            self.fleet.printVehicleRoutes()
        return self.fleet
       
        
    def BuildClusters(self, n, tournamentSize, eliteSize, stopCon):
        
        self.population = self.GeneratePopulation(n=n)
        self.fitnessValues = dict()
        bestValue = 0
        nonImp = 0
        while(nonImp<stopCon):
            for key, value in self.population.items():
                self.fitnessValues[key] = self.FitnessFunction(value)
                

            newGeneration = dict()
            sortedList = sorted(self.fitnessValues.keys(), key = lambda x:self.fitnessValues[x], reverse = True)
            for c in range(eliteSize):
                newGeneration[c] = self.population[sortedList[c]]
            
            if bestValue < self.fitnessValues[sortedList[0]]:
                bestValue = self.fitnessValues[sortedList[0]]
                nonImp = 0
            
            
            for c in range(eliteSize,n):

                child = self.Tournament(random.sample(list(self.population.keys()), tournamentSize))
                child = self.Mutation(child)
                newGeneration[c] = child
                
            self.population = newGeneration
            nonImp += 1
            
            for key, value in self.population.items():
                self.fitnessValues[key] = self.FitnessFunction(value)
                
            bestSolInd = sorted(self.fitnessValues.keys(), key = lambda x:self.fitnessValues[x], reverse = True)[0]
            bestSol = self.population[bestSolInd]
            
            for k in list(set(bestSol)):
                tW=0
                tV=0
                itemsIn = np.where(np.isin(bestSol,k))[0]
                for i in itemsIn:
                    tW += self.cm.get_demands(i+1)[0]
                    tV += self.cm.get_demands(i+1)[1]
                self.totalClusterDemands[k] = [tW, tV]
            
            
            for cust in range(len(bestSol)):
                self.clusters[cust+1] = bestSol[cust]
                
    def GeneratePopulation(self, n):
        
        population = dict()
        customers = [i for i in range(1, self.cm.getCustomers())]
        W = self.fleet.weightCapacities()
        V = self.fleet.volumeCapacities()
            
        for i in range(n):
            vehicleWeights = [0 for k in customers]
            vehicleVolumes =[0 for k in customers]
            population[i] = [0 for k in customers]
            remainings = customers.copy()
            
            
            while(len(remainings)>0):
                tmpC = random.choice(remainings)
                remainings.remove(tmpC)                
                vehList = list(range(1, max(population[i])+1))
                np.random.shuffle(vehList)
                vehList.append(max(population[i])+1)
                for j in vehList:
                    if (vehicleWeights[j-1]+self.cm.get_demands(tmpC)[0]<=W[-1]) \
                    and (vehicleVolumes[j-1]+self.cm.get_demands(tmpC)[1]<=V[-1]):
                        population[i][tmpC-1]=j
                        vehicleWeights[j-1] += self.cm.get_demands(tmpC)[0]
                        vehicleVolumes[j-1] += self.cm.get_demands(tmpC)[1]
                        break
                        
        return population
    
    def MaliyetHesapla(self, array):
        vehicleCount = max(array)
        fitnessValue = 0
        W = self.fleet.weightCapacities()
        V = self.fleet.volumeCapacities()
        F = self.fleet.FixedCosts()
        minItemCount = len(array)
        for j in range(1,vehicleCount+1):
            tW = 0
            tV = 0
            itemsIn = np.where(np.isin(array,j))[0]
            for i in itemsIn:
                tW += self.cm.get_demands(i+1)[0]
                tV += self.cm.get_demands(i+1)[1]
            
            for k in range(len(W)):
                if tW<=W[k] and tV<=V[k]:
                    fitnessValue += F[k]
                    break
                    
                    
        return fitnessValue
    
    
    def FitnessFunction(self, array):
        vehicleCount = max(array)
        fitnessValue = 0
        W = self.fleet.weightCapacities()
        V = self.fleet.volumeCapacities()
        F = self.fleet.FixedCosts()
        minItemCount = len(array)
        for j in range(1,vehicleCount+1):
            tW = 0
            tV = 0
            itemsIn = np.where(np.isin(array,j))[0]
            for i in itemsIn:
                tW += self.cm.get_demands(i+1)[0]
                tV += self.cm.get_demands(i+1)[1]
                
            if len(itemsIn)< minItemCount:
                minItemCount=len(itemsIn)
                count = 1
            elif len(itemsIn) == minItemCount:
                count += 1
            
            for k in range(len(W)):
                if tW<=W[k] and tV<=V[k]:
                    fitnessValue += 1/np.log(F[k])
                    break
                    
        fitnessValue += np.exp(-1*(minItemCount-0.1*count))
                    
        return fitnessValue
    
    def Tournament(self, array):
        ReqFits = { k: self.fitnessValues[k] for k in array }
        ind = max(ReqFits, key=ReqFits.get)
        return self.population[ind].copy()
    
    '''
    def CrossOver(self, parent1, parent2):
        N1 = max(parent1)
        
        tmpN = np.ceil(N1/2).astype(int)
        
        child = [0 for  i in range(1, self.cm.getCustomers())]
        
        for k in range(tmpN):
            
    '''
    
    def Mutation(self, chromosome):
        customers = [i for i in range(1, self.cm.getCustomers())]
        vehicles = [i for i in range(1, max(chromosome)+1)]
        NewVeh = random.choice(vehicles)
        try:
            oldVeh = random.choices(vehicles, weights=[1/chromosome.count(j) for j in vehicles])[0]
        except:
            print(vehicles, chromosome)
        if NewVeh == oldVeh:
            return chromosome
        cust = random.choice(list(np.where(np.isin(chromosome,oldVeh)))[0])
        
        tW = 0
        tV = 0
        for i in np.where(np.isin(chromosome,NewVeh))[0]:
            tW += self.cm.get_demands(i+1)[0]
            tV += self.cm.get_demands(i+1)[1]
            
        if tW+self.cm.get_demands(cust)[0]<= self.fleet.maxCapacity()[0] \
        and tV+self.cm.get_demands(cust)[1]<= self.fleet.maxCapacity()[1]:
            chromosome[cust] = NewVeh
            
        if len(list(np.where(np.isin(chromosome,oldVeh)))[0]) == 0:
            chromosome = [i-1 if i>=oldVeh else i for i in chromosome]
            
        return chromosome
    
    
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
