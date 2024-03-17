import numpy as np
import random
from copy import copy, deepcopy

class ClosestNeighborInitializer:
    def __init__(self, CustomerManager, Fleet):
        self.cm = deepcopy(CustomerManager)
        self.fleet = deepcopy(Fleet)
        
    def run(self, isPrint=False):
        
        n = self.cm.getCustomers()
        C = self.fleet.maxCapacity()
        
        customers = list(range(1,n))
        
        while(len(customers)>0):
            tempC = self.cm.findClosest(0, customers)
            self.fleet.assignVehicle(self.cm, [tempC])
            veh = self.fleet.getAssignedVehicletoCustomer(tempC)
            customers.remove(tempC)           
            
            neigbList = customers.copy()
            while(len(neigbList)>0):
                neig = self.cm.findClosest(tempC, neigbList)
                if (self.fleet.vehicles[veh].getLoad()[0]+self.cm.get_demands(neig)[0]<=self.fleet.maxCapacity()[0]) and \
                    (self.fleet.vehicles[veh].getLoad()[1]+self.cm.get_demands(neig)[1]<=self.fleet.maxCapacity()[1]):
                    self.fleet.vehicles[veh].addCustomer(neig, tempC ,self.cm, justAfter=True)
                    tempC = neig
                    customers.remove(tempC)
                    
                neigbList.remove(neig)
        
        if isPrint:
            self.fleet.printVehicleRoutes()
        return self.fleet
         