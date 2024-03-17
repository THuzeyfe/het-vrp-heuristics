from CustomerManagement import CustomerManagement
from copy import copy, deepcopy
import datetime
import numpy as np

class Vehicle:
    def __init__(self, vehicleType, path):
        self.route = list() 
        self.vehicleType = vehicleType
        self.setVehicleTypes(path=path)
        self.fixed_cost = self.vehicleProperties[self.vehicleType][2]
        self.unit_cost = self.vehicleProperties[self.vehicleType][3]
        self.weightCapacity = self.vehicleProperties[self.vehicleType][0]
        self.volumeCapacity = self.vehicleProperties[self.vehicleType][1]
        
        #self.avg_speed = 70
        #self.max_seconds = 8 * 60 * 60
        #self.travel_time = 0
        self.loadWeight = 0
        self.loadVolume = 0
        self.cost = 0+self.fixed_cost
        self.distance = 0
        
    def setVehicleTypes(self, path):
        self.vehicleProperties = np.genfromtxt(path, delimiter=',')
       
        
    def isCapable(self, weight, volume):
        if (self.loadWeight + weight <= self.weightCapacity) & (self.loadVolume + volume <= self.volumeCapacity):
            return True
        else:
            return False
        
    def getType(self):
        return self.vehicleType
    
    def getLoad(self):
        return self.loadWeight, self.loadVolume
    
    def getDistance(self):
        return self.distance
    
    def getCost(self):
        return self.cost
    
    def removeCustomer(self, customer, custMan):
        while self.vehicleType != 0:
            downWeight = self.vehicleProperties[self.vehicleType-1][0]
            downVolume = self.vehicleProperties[self.vehicleType-1][1]
            
            if (self.loadWeight - custMan.get_demands(customer)[0] <= downWeight) & \
        (self.loadVolume - custMan.get_demands(customer)[1] <= downVolume):
                self.downgradeType()
            else:
                break
                
        self.route.remove(customer)
        self.setRoute(custMan, self.route[1:-1])
        
    def addCustomer(self, customer, where, custMan, justAfter=False):
        while self.vehicleType != len(self.vehicleProperties)-1:
            if(self.loadWeight + custMan.get_demands(customer)[0] > self.weightCapacity) | (self.loadVolume + custMan.get_demands(customer)[1] > self.volumeCapacity):
                self.upgradeType()
            else:
                break
                
        idy = self.route.index(where)
        
        if justAfter:
            self.route.insert(idy+1, customer)
        else:
            if custMan.get_arc(customer, self.route[idy-1]) < custMan.get_arc(customer, self.route[idy+1]):
                self.route.insert(idy, customer)
            else:
                self.route.insert(idy+1, customer)
            
        self.setRoute(custMan, self.route[1:-1])
        
        
        
    def setRoute(self, CustomerManagement, idx):
        self.resetValues()
        idx.append(0)
        self.route.append(0)
        for i in range(len(idx)):
            self.route.append(idx[i])
            if i==0:
                arcdistance = CustomerManagement.get_arc(0, idx[i])
                self.distance += arcdistance
                self.cost += arcdistance*self.unit_cost
                #self.travel_time += datetime.timedelta(hours=arcdistance/self.avg_speed).seconds
            else:
                arcdistance = CustomerManagement.get_arc(idx[i-1],idx[i])
                self.distance += arcdistance
                self.cost += arcdistance*self.unit_cost
                self.loadWeight += CustomerManagement.get_demands(idx[i-1])[0]
                self.loadVolume += CustomerManagement.get_demands(idx[i-1])[1]
                #self.travel_time += datetime.timedelta(hours=arcdistance/self.avg_speed).seconds
                
        
                
    def addOther(self, other, afterWhom, CustomerManagement, reverse):
        position = self.route.index(afterWhom)
        if reverse:
            array = range(len(other.route)-2)[::-1]
        else:
            array = range(len(other.route)-2)
        for i in array:
            removedArc = CustomerManagement.get_arc(self.route[position], self.route[position+1])
            position += 1
            self.route.insert(position,other.route[i+1])
            insertedArc1 = CustomerManagement.get_arc(self.route[position-1], self.route[position])
            insertedArc2 = CustomerManagement.get_arc(self.route[position], self.route[position+1])
            distanceDifference = insertedArc1 + insertedArc2 - removedArc
            self.distance += distanceDifference
            #self.travel_time += datetime.timedelta(hours=distanceDifference/self.avg_speed).seconds
            self.cost += distanceDifference*self.unit_cost
            
        #if self.travel_time > self.max_seconds:
         #   raise Exception("Time constraint is violated!")

        while self.vehicleType != len(self.vehicleProperties)-1:
            if(self.loadWeight + other.loadWeight > self.weightCapacity) | (self.loadVolume + other.loadVolume > self.volumeCapacity):
                self.upgradeType()
            else:
                break
                
        if(self.loadWeight + other.loadWeight > self.weightCapacity) | (self.loadVolume + other.loadVolume > self.volumeCapacity):
            raise Exception("Maximum capacity constraint is violated!")
                
        self.loadWeight += other.loadWeight
        self.loadVolume += other.loadVolume
        
        
    def SwitchCustomers(self, x, y, custMan):
        idx = self.route.index(x)
        idy = self.route.index(y)
        self.route[idx], self.route[idy] = self.route[idy], self.route[idx]        
        self.setRoute(custMan, self.route[1:-1])
        
    def replaceCustomer(self, x, y, custMan):
        while self.vehicleType != len(self.vehicleProperties)-1:
            if(self.loadWeight - custMan.get_demands(x)[0] + custMan.get_demands(y)[0] > self.weightCapacity) | (self.loadVolume - custMan.get_demands(x)[1] + custMan.get_demands(y)[1] > self.volumeCapacity):
                self.upgradeType()
            else:
                break
        
        while self.vehicleType != 0:
            downWeight = self.vehicleProperties[self.vehicleType-1][0]
            downVolume = self.vehicleProperties[self.vehicleType-1][1]
            
            if (self.loadWeight - custMan.get_demands(x)[0] + custMan.get_demands(y)[0] <= downWeight) & \
        (self.loadVolume - custMan.get_demands(x)[1] + custMan.get_demands(y)[1] <= downVolume):
                self.downgradeType()
            else:
                break
                
        idx = self.route.index(x)
        self.route[idx] = y
        self.setRoute(custMan, self.route[1:-1])
            
        
        
            
    def upgradeType(self):
        self.vehicleType += 1
        self.fixed_cost = self.vehicleProperties[self.vehicleType][2]
        self.unit_cost = self.vehicleProperties[self.vehicleType][3]
        self.weightCapacity = self.vehicleProperties[self.vehicleType][0]
        self.volumeCapacity = self.vehicleProperties[self.vehicleType][1]
        self.cost = self.distance * self.unit_cost + self.fixed_cost
        
    def downgradeType(self):
        self.vehicleType -= 1
        self.fixed_cost = self.vehicleProperties[self.vehicleType][2]
        self.unit_cost = self.vehicleProperties[self.vehicleType][3]
        self.weightCapacity = self.vehicleProperties[self.vehicleType][0]
        self.volumeCapacity = self.vehicleProperties[self.vehicleType][1]
        self.cost = self.distance * self.unit_cost + self.fixed_cost
            
    def isIn(self, idx):
        if idx in self.route:
            return True
        else:
            return False
                
                
    def resetValues(self):
        self.route = list()
        self.loadWeight = 0
        self.loadVolume = 0
        self.cost = 0 + self.fixed_cost
        self.distance = 0
        self.travel_time = 0 
        
    def printRoutes(self):
        print("Type {}\t Total Cost: {:.2f}\t Distance:{:.2f} km\t Demands: {} kg and {} liters. Route: {}" \
              .format(self.vehicleType,self.cost,self.distance, self.loadWeight, self.loadVolume, self.route))
        
    def getCost(self):        
        return self.cost
    
    def get_customer(self, idx):
        return self.customers[idx]
    
    def getCapacity(self):
        return self.weightCapacity, self.volumeCapacity
    
    def getCustomers(self):
        return self.route[1:-1]
    
    def isLast(self, customerId):
        if self.route[-2] == customerId:
            return True
        else:
            return False
        
    def isFirst(self, customerId):
        if self.route[1] == customerId:
            return True
        else:
            return False
        
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result