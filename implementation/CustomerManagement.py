import numpy as np
import math

class CustomerManagement:
    def __init__(self, day, n):
        self.n = n
        self.day = day
        self.getCustomerInfo()
        
        
    def setDistances(self):
        t = self.n
        self.distances = np.array(np.random.randint(0,1,t*t)).reshape(t,t)
        for i in range(t):
            for j in range(t):
                self.distances[i][j] = ((self.x[i]-self.x[j])**2 + (self.y[i]-self.y[j])**2) ** (1/2)
        
        
    def getCustomers(self):
        return len(self.weights)

    def get_arc(self, customer1, customer2):
        return self.distances[customer1][customer2]
    
    def get_distances(self):
        return self.distances

    def get_demands(self, idx):
        return self.weights[idx], self.volumes[idx]
    
    def findClosest(self, idx, idys=None):
        if idys == None:
            idys=list(range(self.getCustomers()))
        mindistance = math.inf
        for idy in idys:
            if idx!=idy and self.get_arc(idx, idy) < mindistance:
                mindistance = self.get_arc(idx, idy)
                closest = idy
        return closest
    
    def getFeasibleSpace(self, W, V, cList=None):
        
        if cList is None:
            cList = [0] + range(1, self.getCustomers())
        
        returnList = list()
        
        for c in cList:
            if self.weights[c]<= W and self.volumes[c]<=V:
                returnList.append(c)
                
        return returnList
    
    
    def sortArcs(self,idx=None):
        if idx==None:
            sorted_arcs = np.dstack(np.unravel_index(np.argsort(self.get_distances(), axis=None),\
                                                     self.get_distances().shape))[0]
        else:
            sorted_arcs = np.dstack(np.unravel_index(np.argsort(self.get_distances()[idx][:,idx], axis=None),\
                                                     self.get_distances()[idx][:,idx].shape))[0]
            
        iu1 = np.triu_indices(sorted_arcs.shape[0],k=1)
        iu1 = np.dstack(iu1)[0]
        arcs = []
        for i in sorted_arcs:
            if (np.all(iu1 == i,1)).any():
                arcs.append(i)
        del i
        
        return arcs
    
    
    def getCustomerInfo(self):
        path= "data/n"+ str(self.n)+"day"+str(self.day)+".csv"
        
        self.weights = []
        self.volumes = []
        self.x = []
        self.y = []
        
        demandData = np.genfromtxt(path, delimiter=',')
        
        for i in demandData:
            self.x.append(i[0])
            self.y.append(i[1])            
            self.weights.append(i[2])
            self.volumes.append(i[3])
            
        self.setDistances()
            

