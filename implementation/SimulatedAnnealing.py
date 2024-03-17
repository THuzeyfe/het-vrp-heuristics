from copy import copy, deepcopy
import math
import random

class SimulatedAnnealing:
    def __init__(self, CustomerManagement, fleet):
        self.cm = deepcopy(CustomerManagement)
        self.fleet = deepcopy(fleet)
        
    def run(self, method='intra-switch', initialTemp=1000, minTemp=0.1, coolingP=0.5, maxEpoch=2, isPrint=False):
        
        
        bestCost = self.fleet.totalCost()
        initialTemp = initialTemp
        minTemp = minTemp
        coolingP = coolingP
        
        currentTemp = initialTemp
        
        if method == 'mix':
            while(currentTemp>minTemp):
                epoch=0
                while(epoch<=maxEpoch):
                    vehicles = self.fleet.vehicleList()
                    strategy = random.randint(0,2)
                    if strategy == 0:
                        tempVeh = random.choice(vehicles)
                        customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)
                        if len(customerList)>=2:
                            customer1, customer2 = random.sample(customerList,2)
                        else:
                            continue

                        estimatedCost = self.fleet.EstimateIntraSwitchCost(tempVeh, customer1, customer2, self.cm)
                        if estimatedCost < bestCost:
                            self.fleet.IntraSwitchCustomers(tempVeh, customer1, customer2, self.cm)
                            bestCost = self.fleet.totalCost()
                        else:
                            acceptProb = (bestCost-estimatedCost)/currentTemp
                            acceptProb = math.exp(acceptProb)
                            randVar = random.random()
                            if (acceptProb>randVar):
                                self.fleet.IntraSwitchCustomers(tempVeh, customer1, customer2, self.cm)
                                bestCost = self.fleet.totalCost()
                    elif strategy == 1:
                        vehicles = self.fleet.vehicleList()
                        tempVeh1, tempVeh2 = random.sample(vehicles,2)
                        customer1 = random.choice(self.fleet.getAssignedCustomerstoVehicle(tempVeh1))
                        customer2 = random.choice(self.fleet.getAssignedCustomerstoVehicle(tempVeh2))

                        estimatedCost = self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                        if estimatedCost < bestCost:
                            self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                            bestCost = self.fleet.totalCost()
                        else:
                            acceptProb = (bestCost-estimatedCost)/currentTemp
                            acceptProb = math.exp(acceptProb)
                            randVar = random.random()
                            if (acceptProb>randVar):
                                self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                                bestCost = self.fleet.totalCost()
                    else:
                        vehicles = self.fleet.vehicleList()
                        selVeh = random.choice(vehicles)
                        selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))
                        VehicleToAdd = random.choice(vehicles)

                        estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)

                        if estimatedCost < bestCost:
                            self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                            bestCost = self.fleet.totalCost()
                        else:
                            acceptProb = (bestCost-estimatedCost)/currentTemp
                            acceptProb = math.exp(acceptProb)
                            randVar = random.random()
                            if (acceptProb>randVar):
                                self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                                bestCost = self.fleet.totalCost()
                    epoch += 1
                currentTemp = currentTemp * coolingP
        elif method == 'addremove':
            while(currentTemp>minTemp):
                epoch=0
                while(epoch<=maxEpoch):
                    vehicles = self.fleet.vehicleList()
                    selVeh = random.choice(vehicles)
                    selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))
                    VehicleToAdd = random.choice(vehicles)

                    estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)

                    if estimatedCost < bestCost:
                        self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                        bestCost = self.fleet.totalCost()
                    else:
                        acceptProb = (bestCost-estimatedCost)/currentTemp
                        acceptProb = math.exp(acceptProb)
                        randVar = random.random()
                        if (acceptProb>randVar):
                            self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                            bestCost = self.fleet.totalCost()
                    epoch += 1
                currentTemp = currentTemp * coolingP
        elif method == 'inter-switch':
            while(currentTemp>minTemp):
                epoch=0
                while(epoch<=maxEpoch):
                    vehicles = self.fleet.vehicleList()
                    tempVeh1, tempVeh2 = random.sample(vehicles,2)
                    customer1 = random.choice(self.fleet.getAssignedCustomerstoVehicle(tempVeh1))
                    customer2 = random.choice(self.fleet.getAssignedCustomerstoVehicle(tempVeh2))
                    
                    estimatedCost = self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                    if estimatedCost < bestCost:
                        self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                        bestCost = self.fleet.totalCost()
                    else:
                        acceptProb = (bestCost-estimatedCost)/currentTemp
                        acceptProb = math.exp(acceptProb)
                        randVar = random.random()
                        if (acceptProb>randVar):
                            self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, customer1, customer2, self.cm)
                            bestCost = self.fleet.totalCost()
                    epoch += 1
                currentTemp = currentTemp * coolingP
        elif method == 'intra-switch':
            while(currentTemp>minTemp):
                epoch=0
                while(epoch<=maxEpoch):
                    vehicles = self.fleet.vehicleList()
                    tempVeh = random.choice(vehicles)
                    customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)
                    if len(customerList) >= 2:
                        customer1, customer2 = random.sample(customerList,2)
                    else:
                        continue
                    
                    estimatedCost = self.fleet.EstimateIntraSwitchCost(tempVeh, customer1, customer2, self.cm)
                    if estimatedCost < bestCost:
                        self.fleet.IntraSwitchCustomers(tempVeh, customer1, customer2, self.cm)
                        bestCost = self.fleet.totalCost()
                    else:
                        acceptProb = (bestCost-estimatedCost)/currentTemp
                        acceptProb = math.exp(acceptProb)
                        randVar = random.random()
                        if (acceptProb>randVar):
                            self.fleet.IntraSwitchCustomers(tempVeh, customer1, customer2, self.cm)
                            bestCost = self.fleet.totalCost()
                    epoch += 1
                currentTemp = currentTemp * coolingP
                
                
        
        if isPrint:
            self.fleet.printVehicleRoutes()
        return self.fleet
                    
    
    
    

        
                
                