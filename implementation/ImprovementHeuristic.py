import random
import itertools
from copy import copy, deepcopy

class ImprovementHeuristic:
    def __init__(self, CustomerManagement, fleet):
        self.cm = deepcopy(CustomerManagement)
        self.fleet = deepcopy(fleet)
        
        
    def run(self, strategy='FirstImprovement', method='mix',stopping=15,isPrint=False):
        if strategy=='FirstImprovement':
            self.FirstImprovementStrategy(stopping=stopping, method=method)
        elif strategy=='BestImprovement':
            self.BestImprovementStrategy(stopping=stopping, method=method)
        else:
            raise ValueError("Unknown strategy")
        if isPrint:
            self.fleet.printVehicleRoutes()
        return self.fleet
    
        
    def FirstImprovementStrategy(self, method, stopping):
        curr_cost = self.fleet.totalCost()
        nonImprovedSteps = 0
        if method == 'mix':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                strategy = random.randint(0,2)
                if strategy == 0:
                    tempVeh = random.choice(vehicles)
                    customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)            
                    switchCombinations = list(itertools.combinations(customerList,2))            
                    random.shuffle(switchCombinations)

                    for couple in switchCombinations:
                        if self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)<curr_cost:
                            self.fleet.IntraSwitchCustomers(tempVeh, couple[0], couple[1], self.cm)
                            curr_cost = self.fleet.totalCost()
                            nonImprovedSteps = 0
                            break
                    nonImprovedSteps +=1
                elif strategy == 1:
                    tempVeh1, tempVeh2 = random.sample(vehicles,2)
                    customerList1 = self.fleet.getAssignedCustomerstoVehicle(tempVeh1)
                    customerList2 = self.fleet.getAssignedCustomerstoVehicle(tempVeh2)
                    switchCombinations = []
                    for customer1 in customerList1:
                        for customer2 in customerList2:
                            switchCombinations.append([customer1, customer2])
                    random.shuffle(switchCombinations)
                    for couple in switchCombinations:
                        if self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)<curr_cost:
                            self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)
                            curr_cost = self.fleet.totalCost()
                            nonImprovedSteps = 0
                            break
                    nonImprovedSteps +=1
                else:
                    selVeh = random.choice(vehicles)
                    selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))
                    random.shuffle(vehicles)
                    for VehicleToAdd in vehicles:
                        if VehicleToAdd == selVeh:
                            continue
                        estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)
                        if estimatedCost < curr_cost:
                            self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                            curr_cost = self.fleet.totalCost()
                            nonImprovedSteps = 0
                            break
                    nonImprovedSteps +=1
        elif method == 'addremove':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                selVeh = random.choice(vehicles)
                selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))
                random.shuffle(vehicles)
                for VehicleToAdd in vehicles:
                    if VehicleToAdd == selVeh:
                        continue
                    estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)
                    if estimatedCost < curr_cost:
                        self.fleet.RemoveAdd(selCust, VehicleToAdd, self.cm)
                        curr_cost = self.fleet.totalCost()
                        nonImprovedSteps = 0
                        break
                nonImprovedSteps +=1
        elif method == 'inter-switch':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                tempVeh1, tempVeh2 = random.sample(vehicles,2)
                customerList1 = self.fleet.getAssignedCustomerstoVehicle(tempVeh1)
                customerList2 = self.fleet.getAssignedCustomerstoVehicle(tempVeh2)
                switchCombinations = []
                for customer1 in customerList1:
                    for customer2 in customerList2:
                        switchCombinations.append([customer1, customer2])
                random.shuffle(switchCombinations)
                for couple in switchCombinations:
                    if self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)<curr_cost:
                        self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)
                        curr_cost = self.fleet.totalCost()
                        nonImprovedSteps = 0
                        break
                nonImprovedSteps +=1
        elif method == 'intra-switch':
                vehicles = self.fleet.vehicleList()
                tempVeh = random.choice(vehicles)
                customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)            
                switchCombinations = list(itertools.combinations(customerList,2))            
                random.shuffle(switchCombinations)

                for couple in switchCombinations:
                    if self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)<curr_cost:
                        self.fleet.IntraSwitchCustomers(tempVeh, couple[0], couple[1], self.cm)
                        curr_cost = self.fleet.totalCost()
                        nonImprovedSteps = 0
                        break
                nonImprovedSteps +=1
        else:
            raise ValueError("Unknown method")

            
            
            
                
            
    def BestImprovementStrategy(self, method, stopping):
        
        bestCost = self.fleet.totalCost()
        nonImprovedSteps = 0
        if method == 'mix':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                bestCouple =None
                strategy = random.randint(0,2)
                if strategy == 0:
                    tempVeh = random.choice(vehicles)
                    customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)            
                    switchCombinations = list(itertools.combinations(customerList,2))            

                    for couple in switchCombinations:
                        if self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)<bestCost:
                            bestCouple = couple
                            bestCost = self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)
                            nonImprovedSteps = 0

                    if bestCouple is not None:
                        self.fleet.IntraSwitchCustomers(tempVeh, bestCouple[0], bestCouple[1], self.cm)
                    else:
                        nonImprovedSteps +=1
                elif strategy== 1:
                    tempVeh1, tempVeh2 = random.sample(vehicles,2)
                    customerList1 = self.fleet.getAssignedCustomerstoVehicle(tempVeh1)
                    customerList2 = self.fleet.getAssignedCustomerstoVehicle(tempVeh2)
                    switchCombinations = []
                    for customer1 in customerList1:
                        for customer2 in customerList2:
                            switchCombinations.append([customer1, customer2])

                    for couple in switchCombinations:
                        if self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)<bestCost:
                            bestCouple = couple
                            bestCost = self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)
                            nonImprovedSteps = 0

                    if bestCouple is not None:
                        self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, bestCouple[0], bestCouple[1], self.cm)
                    else:
                        nonImprovedSteps +=1
                else:
                    selVeh = random.choice(vehicles)
                    selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))

                    for VehicleToAdd in vehicles:
                        if VehicleToAdd == selVeh:
                            continue
                        estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)
                        if estimatedCost < bestCost:
                            bestCouple = VehicleToAdd
                            bestCost = estimatedCost
                            nonImprovedSteps = 0

                    if bestCouple is not None:
                        self.fleet.RemoveAdd(selCust, bestCouple, self.cm)
                    else:
                        nonImprovedSteps +=1
        elif method == 'addremove':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                bestCouple =None
                selVeh = random.choice(vehicles)
                selCust = random.choice(self.fleet.getAssignedCustomerstoVehicle(selVeh))

                for VehicleToAdd in vehicles:
                    if VehicleToAdd == selVeh:
                        continue
                    estimatedCost = self.fleet.estimateRemoveAdd(selCust, VehicleToAdd, self.cm)
                    if estimatedCost < bestCost:
                        bestCouple = VehicleToAdd
                        bestCost = estimatedCost
                        nonImprovedSteps = 0

                if bestCouple is not None:
                    self.fleet.RemoveAdd(selCust, bestCouple, self.cm)
                else:
                    nonImprovedSteps +=1
        elif method == 'inter-switch':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                bestCouple =None
                tempVeh1, tempVeh2 = random.sample(vehicles,2)
                customerList1 = self.fleet.getAssignedCustomerstoVehicle(tempVeh1)
                customerList2 = self.fleet.getAssignedCustomerstoVehicle(tempVeh2)
                switchCombinations = []
                for customer1 in customerList1:
                    for customer2 in customerList2:
                        switchCombinations.append([customer1, customer2])

                for couple in switchCombinations:
                    if self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)<bestCost:
                        bestCouple = couple
                        bestCost = self.fleet.EstimateInterSwitchCost(tempVeh1, tempVeh2, couple[0], couple[1], self.cm)
                        nonImprovedSteps = 0

                if bestCouple is not None:
                    self.fleet.InterSwitchCustomers(tempVeh1, tempVeh2, bestCouple[0], bestCouple[1], self.cm)
                else:
                    nonImprovedSteps +=1
        elif method == 'intra-switch':
            while(nonImprovedSteps < stopping):
                vehicles = self.fleet.vehicleList()
                bestCouple =None
                tempVeh = random.choice(vehicles)
                customerList = self.fleet.getAssignedCustomerstoVehicle(tempVeh)            
                switchCombinations = list(itertools.combinations(customerList,2))            

                for couple in switchCombinations:
                    if self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)<bestCost:
                        bestCouple = couple
                        bestCost = self.fleet.EstimateIntraSwitchCost(tempVeh, couple[0], couple[1], self.cm)
                        nonImprovedSteps = 0

                if bestCouple is not None:
                    self.fleet.IntraSwitchCustomers(tempVeh, bestCouple[0], bestCouple[1], self.cm)
                else:
                    nonImprovedSteps +=1            
            
                        
                        
                    