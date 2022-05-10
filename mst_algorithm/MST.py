import numpy as np
import random
import pandas as pd
from collections import defaultdict

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
        self.weight = 0
    
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
            for j in range(i):
                if not self.throw(self.adjMat[i][j]):
                    if i not in self.adjList:
                        self.adjList[i] = {j: self.adjMat[i][j]}
                    else:
                        self.adjList[i].update({j: self.adjMat[i][j]})
                        
                    if j not in self.adjList:
                        self.adjList[j] = {i: self.adjMat[j][i]}
                    else:
                        self.adjList[j].update({i: self.adjMat[j][i]})
        
        # to save memory 
        self.adjMat = []
            
    def throw(self, n):

        if self.dim == 1:
            if n < n ** (-1/1.661):
                return False
        if self.dim == 2:
            if n < n ** (-1/2.660):
                return False
        if self.dim == 3:
            if n < n ** (-1/3.869):
                return False
        if self.dim == 4:
            if n < n ** (-1/5.446):
                return False
        return True
    
    def prim_mst(self):
        graph = self.adjList
        
        visited = set()
        
        Q = PriorityQueue()
        Q.insert(self.source, 0)
        
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
    
    n_list = [
        128, 256, 512, 1024, 
        2048, 4096, 8192,
        16384, 32768, 65536, 131072
              ]
    repeat = 5
    res = defaultdict(list)
    
    for i in n_list:
        w = []
        for _ in range(repeat):
            g = Graph(i, dim = 2)
            g.construct()
            g.prim_mst()
            w.append(g.Weight())
            
        res[i].append(np.round(np.mean(w), 5))
        print('n = %d:'%i)
        print('weight = %.5f'%res[i][0])
        pd.DataFrame(res).to_csv('two_dimension_w_clip.csv', index = False)
