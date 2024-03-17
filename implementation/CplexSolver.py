import matplotlib.pyplot as plt
from docplex.mp.model import Model

class CplexSolver:
    def __init__(self, n, nFleet, nDay):
        fleetData = np.genfromtxt('data/fleet{}.csv'.format(nFleet), delimiter=',')
        demands = np.genfromtxt('data/n{}day{}.csv'.format(n,nDay), delimiter=',')
        
        self.Q1= list()
        self.Q2= list()
        self.F = list()
        self.var = list()

        for veh in fleetData:
            self.Q1.append(veh[0])
            self.Q2.append(veh[1])
            self.F.append(veh[2])
            self.var.append(veh[3])

        self.K = [i for i in range(len(F))]
        self.N = [i for i in range(1, len(demands))]
        self.V = [0] + N

        self.loc_x = []
        self.loc_y = []
        self.q1 = dict()
        self.q2 = dict()

        self.loc_x.append(demands[0][0])
        self.loc_y.append(demands[0][1])

        for cust in range(1,len(demands)):
            self.loc_x.append(demands[cust][0])
            self.loc_y.append(demands[cust][1])
            self.q1[cust] = demands[cust][2]
            self.q2[cust] = demands[cust][3]
        
        
    def solve(self, timeLimit=120, logOutput=False, isPrint=False):
        
        A = [(i, j, k) for i in self.V for j in self.V if i != j for k in self.K]
        c = {(i, j, k): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) * var[k] for i,j,k in A}
        
        mdl = Model('CVRP')
        
        x = mdl.binary_var_dict(A, name='x')
        u1 = mdl.continuous_var_dict(self.V, ub=self.Q1[-1], name='u1')
        u2 = mdl.continuous_var_dict(self.V, ub=self.Q2[-1], name='u2')
        
        
        mdl.minimize(mdl.sum(c[i, j, k]*x[i, j, k] for i, j, k in A) + mdl.sum(self.F[k]* x[0,j,k] for j in self.N for k in self.K))
        mdl.add_constraints(mdl.sum(x[i,j,k] for i in self.V if i!=j for k in self.K) == 1 for j in self.N)
        mdl.add_constraints((mdl.sum(x[i,p,k] for i in self.V if i!=p)-mdl.sum(x[p,j,k] for j in self.V if j!=p))==0 for k in self.K for p in self.N)
        mdl.add_constraint(u1[0]==0)
        mdl.add_constraints(u1[j]-u1[i]>=(self.q1[j]+ self.Q1[-1])*mdl.sum(x[i,j,k] for k in self.K)-self.Q1[-1] for i in self.V for j in self.N if i!=j)
        mdl.add_constraints(u1[j]<=mdl.sum(self.Q1[k]*x[i,j,k] for i in self.V if i!=j for k in self.K) for j in self.N)
        mdl.add_constraint(u2[0]==0)
        mdl.add_constraints(u2[j]-u2[i]>=(self.q2[j]+ self.Q2[-1])*mdl.sum(x[i,j,k] for k in self.K)-self.Q2[-1] for i in self.V for j in self.N if i!=j)
        mdl.add_constraints(u2[j]<=mdl.sum(self.Q2[k]*x[i,j,k] for i in self.V if i!=j for k in self.K) for j in self.N)
        mdl.parameters.timelimit = timeLimit
        solution = mdl.solve(log_output=logOutput)
        
        return solution
    
    
    

        
        
        
        
        
        
        
        
        
        