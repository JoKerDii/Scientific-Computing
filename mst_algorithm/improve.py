import numpy as np
import random
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

class PriorityQueue:
    def __init__(self):
        self.hash = {}
        self.length = 0
        
    def insert(self, node, length):
        if node not in self.hash:
            self.hash[node] = length
        elif self.hash[node] > length:
            self.hash[node] = length
        
    def deletemin(self):
        MIN = None
        minDist = float('inf')
        for node in self.hash:
            if (MIN is None) or (self.hash[node] < minDist):
                MIN = node
                minDist = self.hash[node]
        del self.hash[MIN]
        return MIN, minDist
    
    def isEmpty(self):
        return True if len(self.hash) == 0 else False

class Graph:
    def __init__(self, n, dim = 1):
        self.adjMat = []
        self.adjList = {}
        self.dim = dim
        self.n = n
        self.source = 0
        self.mst = defaultdict(set)
        self.weight = []
        self.sumWeight = 0
    
    def construct(self):
        n = self.n
        
        # construct adjacency matrix
        self.adjMat = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                if self.dim == 1:
                    rand = random.uniform(0,1)
                elif self.dim == 2:
                    rand = np.sqrt((random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2)
                elif self.dim == 3:
                    rand = np.sqrt((random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2)
                elif self.dim == 4:
                    rand = np.sqrt((random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2 +
                                   (random.uniform(0,1) - random.uniform(0,1))**2)
                self.adjMat[i][j] = rand
                self.adjMat[j][i] = rand
        
        # construct adjacency list
        for i in range(n):
            for j in range(n):
                if i != j:
                    if i not in self.adjList:
                        self.adjList[i] = {j: self.adjMat[i][j]}
                    else:
                        self.adjList[i].update({j: self.adjMat[i][j]})
            
    def prim_mst(self):
        source = self.source
        graph = self.adjList
        
        visited = set()
        
        Q = PriorityQueue()
        Q.insert(source, 0)
        
        while not Q.isEmpty():
            
            child, dist = Q.deletemin()
            if child not in visited:
                visited.add(child)
                self.weight += dist
                for nxt, dist in graph[child].items():
                    if nxt not in visited:
                        Q.insert(nxt, dist)
    
    def Weight(self):
        return self.weight


if __name__ == '__main__':
    
    repeat = 5
    bList = [5.446] # 1.661 for 1D, 2.66 for 2D, 3.869 for 3D
    bestB = defaultdict(list)
    res = defaultdict(list)
    for b in bList:
        for i in range(4,201):
            simu = i ** (-1.0 / b)
            
            MAX = []
            w = []
            for _ in range(repeat):
                g = Graph(i, dim = 4)
                g.construct()
                mst = g.prim_mst()
                MAX.append(g.Weight())
            res[i].append(simu - np.mean(MAX)) # should be positive
            print('n = %d:'%i)
            print('weight = %.5f'%res[i][0])
        # print(res)
        bestB[b].append(np.min(pd.DataFrame(res).T[0])) #,np.std(pd.DataFrame(res).T[0]), np.min(pd.DataFrame(res).T[0]), np.max(pd.DataFrame(res).T[0])])
    
    diff = pd.DataFrame(res).T
    print(np.mean(diff))
    
    diff.columns = ['diff']
    index = [i for i in range(4, 201)]
    df = pd.DataFrame({'diff': diff['diff'], 'index': index})
    plt.scatter(x = df['index'], y = df['diff'])
    print(bestB[bList[0]][0] < 0)
