from Vehicle import Vehicle
from CustomerManagement import CustomerManagement
from copy import copy, deepcopy
import numpy as np

class Fleet:
    def __init__(self, fleetN):
        self.VehicleTypes = dict()
        self.fleetPath = 'data/fleet' + str(fleetN) + '.csv'
        self.setVehicles(self.fleetPath)
        self.vehicles = list()
        
    def maxCapacity(self):
        return max([Vehicle(x, self.fleetPath).getCapacity()[0] for x in self.VehicleTypes]), max([Vehicle(x, self.fleetPath).getCapacity()[1] for x in self.VehicleTypes])
    
    def weightCapacities(self):
        return [Vehicle(x, self.fleetPath).getCapacity()[0] for x in self.VehicleTypes]
    
    def volumeCapacities(self):
        return [Vehicle(x, self.fleetPath).getCapacity()[1] for x in self.VehicleTypes]
    
    def FixedCosts(self):
        return [Vehicle(x, self.fleetPath).fixed_cost for x in self.VehicleTypes]
    
    def setVehicles(self, path):
        vehs = np.genfromtxt(path, delimiter=',')
        for i in range(len(vehs)):
            self.VehicleTypes[i] = 0
            
    def returnVehicles(self):
        for veh in self.vehicles:
            self.VehicleTypes[veh.getType()] += 1 
        return list(self.VehicleTypes.values())
        
        
    def addNewVehicle(self, vehicleType, customerManagement, customerIDs):
        newVehicle = Vehicle(vehicleType, self.fleetPath)
        newVehicle.setRoute(customerManagement, customerIDs) 
        self.vehicles.append(newVehicle)
        
    def printVehicleRoutes(self):
        for vehicle in self.vehicles:
            vehicle.printRoutes()
        print("\033[1m" + "Total cost is {:.2f} and {:.2f} km distance is traveled" \
              .format(self.totalCost(), self.totalKm()) + "\033[0m")
            
    def isLast(self, customerId):
        for vehicle in self.vehicles:
            if vehicle.isLast(customerId):
                return True
        return False
        
    def isFirst(self, customerId):
        for vehicle in self.vehicles:
            if vehicle.isFirst(customerId):
                return True
        return False
    
    def getAssignedVehicletoCustomer(self, customerId):
        for vehicle in range(len(self.vehicles)):
            if self.vehicles[vehicle].isIn(customerId):
                return vehicle
        return None
    
    def mergeVehicles(self, vehicle1, vehicle2, position, CustomerManagement, reverse):
        self.vehicles[vehicle1].addOther(self.vehicles[vehicle2], position, CustomerManagement, reverse)
        del self.vehicles[vehicle2]
        
    def totalKm(self):
        totalDistance = 0
        for vehicle in self.vehicles:
            totalDistance += vehicle.getDistance()
        return totalDistance
    
    def totalCost(self):
        totalCost = 0
        for vehicle in self.vehicles:
            totalCost += vehicle.getCost()
        return totalCost
    
    def vehicleList(self):
        return self.vehicles
    
    def getAssignedCustomerstoVehicle(self, vehicle):
        return vehicle.getCustomers()
    
    def estimateRemoveAdd(self, customer, newVehicle, custMan):
        if (newVehicle.getLoad()[0]+custMan.get_demands(customer)[0]>self.maxCapacity()[0]) | \
        (newVehicle.getLoad()[1]+custMan.get_demands(customer)[1]>self.maxCapacity()[1]):
            return self.totalCost() * 999
        
        oldInd = self.getAssignedVehicletoCustomer(customer)
        oldVeh = deepcopy(self.vehicles[oldInd])
        
        if self.vehicles[oldInd] == newVehicle:
            return self.totalCost() * 999
        
        oldCostofOld = oldVeh.getCost()
        newVeh = deepcopy(newVehicle)
        oldCostofNew = newVeh.getCost()
        closest = custMan.findClosest(customer, newVeh.getCustomers())
        
        if len(self.getAssignedCustomerstoVehicle(self.vehicles[oldInd]))==1:
            newCostofOld = 0
        else:
            oldVeh.removeCustomer(customer, custMan)
            newCostofOld = oldVeh.getCost()
            
        newVeh.addCustomer(customer, closest, custMan)
        newCostofNew = newVeh.getCost()
        
        del oldVeh, newVeh        
        return self.totalCost() - oldCostofOld - oldCostofNew + newCostofOld + newCostofNew
        
    
    def EstimateIntraSwitchCost(self, vehicle, x, y, custMan):
        currCost = self.totalCost()
        ind = self.vehicles.index(vehicle)
        tmpVehicle = deepcopy(self.vehicles[ind])
        tmpVehicle.SwitchCustomers(x,y, custMan)
        oldCost = self.vehicles[ind].getCost()
        newCost = tmpVehicle.getCost()
        del tmpVehicle
        return currCost - oldCost + newCost
    
    def EstimateInterSwitchCost(self, vehicle1, vehicle2, x, y, custMan):
        currCost = self.totalCost()
        ind1 = self.vehicles.index(vehicle1)
        ind2 = self.vehicles.index(vehicle2)
        if (self.vehicles[ind1].getLoad()[0]-custMan.get_demands(x)[0] + custMan.get_demands(y)[0] > self.maxCapacity()[0]) | \
        (self.vehicles[ind1].getLoad()[1]-custMan.get_demands(x)[1] + custMan.get_demands(y)[1] > self.maxCapacity()[1]) | \
        (self.vehicles[ind2].getLoad()[0]-custMan.get_demands(y)[0] + custMan.get_demands(x)[0] > self.maxCapacity()[0]) | \
        (self.vehicles[ind2].getLoad()[1]-custMan.get_demands(y)[1] + custMan.get_demands(x)[1] > self.maxCapacity()[1]):
            return currCost
        
        tmpVehicle1 = deepcopy(self.vehicles[ind1])
        tmpVehicle2 = deepcopy(self.vehicles[ind2])
        tmpVehicle1.replaceCustomer(x, y, custMan)
        tmpVehicle2.replaceCustomer(y, x, custMan)
        oldCost = self.vehicles[ind1].getCost() + self.vehicles[ind2].getCost()
        newCost = tmpVehicle1.getCost() + tmpVehicle2.getCost()
        del tmpVehicle1, tmpVehicle2
        return currCost - oldCost + newCost
    
    
    def RemoveAdd(self, customer, newVeh, custMan):
        if (newVeh.getLoad()[0]+custMan.get_demands(customer)[0]>self.maxCapacity()[0]) | \
        (newVeh.getLoad()[1]+custMan.get_demands(customer)[1]>self.maxCapacity()[1]):
            return
        
        oldVeh = self.getAssignedVehicletoCustomer(customer)
        if oldVeh == newVeh:
            return
        
        closest = custMan.findClosest(customer, newVeh.getCustomers())
        
        newVeh.addCustomer(customer, closest, custMan)
        if len(self.getAssignedCustomerstoVehicle(self.vehicles[oldVeh]))==1:
            del self.vehicles[oldVeh]
        else:
            self.vehicles[oldVeh].removeCustomer(customer, custMan)
            
        
    
        
    def IntraSwitchCustomers(self, vehicle, x, y, custMan):
        ind = self.vehicles.index(vehicle)
        self.vehicles[ind].SwitchCustomers(x,y,custMan)
        
    def InterSwitchCustomers(self, vehicle1, vehicle2, x, y, custMan):
        ind1 = self.vehicles.index(vehicle1)
        ind2 = self.vehicles.index(vehicle2)
        if (self.vehicles[ind1].getLoad()[0]-custMan.get_demands(x)[0] + custMan.get_demands(y)[0] > self.maxCapacity()[0]) | \
        (self.vehicles[ind1].getLoad()[1]-custMan.get_demands(x)[1] + custMan.get_demands(y)[1] > self.maxCapacity()[1]) | \
        (self.vehicles[ind2].getLoad()[0]-custMan.get_demands(y)[0] + custMan.get_demands(x)[0] > self.maxCapacity()[0]) | \
        (self.vehicles[ind2].getLoad()[1]-custMan.get_demands(y)[1] + custMan.get_demands(x)[1] > self.maxCapacity()[1]):
            return
        self.vehicles[ind1].replaceCustomer(x,y,custMan)
        self.vehicles[ind2].replaceCustomer(y,x,custMan)
        
    def assignVehicle(self, customerManagement, customerIDs):
        requiredWeightCapacity = 0
        requiredVolumeCapacity = 0
        for customer in customerIDs:
            requiredWeightCapacity += customerManagement.get_demands(customer)[0]
            requiredVolumeCapacity += customerManagement.get_demands(customer)[1]
            
        if (requiredWeightCapacity>self.maxCapacity()[0]) | (requiredWeightCapacity>self.maxCapacity()[1]): 
            return
        
        for vehicle in self.VehicleTypes:
            if Vehicle(vehicle, self.fleetPath).isCapable(requiredWeightCapacity, requiredVolumeCapacity):
                self.addNewVehicle(vehicle, customerManagement, customerIDs)
                break
                
                
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result