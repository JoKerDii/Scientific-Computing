import math
import random
from operator import add, sub
from time import perf_counter
# import pandas as pd
import sys
# import matplotlib.pyplot as plt

def traditional_multiplication(a, b):
    n = len(a)
    res = [[0 for i in range(n)] for j in range(n)]
    for k in range(n):
        for i in range(n):
            temp = a[i][k]
            for j in range(n):
                res[i][j] += temp * b[k][j]
    return res

def plus(a, b):
    res = [list(map(add, a[i], b[i])) for i in range(len(a))]
    return res

def subtract(a, b):
    res = [list(map(sub, a[i], b[i])) for i in range(len(a))]
    return res

def split(m):
    n = len(m)
    half = math.ceil(n/2)
    splits = ([], [], [], [])
    
    for i in range(half):
        splits[0].append(m[i][:half])
        splits[1].append(m[i][half:])
        
    for i in range(half, n):
        splits[2].append(m[i][:half])
        splits[3].append(m[i][half:])
        
    if n % 2: # odd
        # pad rows
        splits[2].append([0] * half)
        splits[3].append([0] * (half - 1))
        
        # pad columns
        for i in range(half):
            splits[1][i].append(0)
            splits[3][i].append(0)
    
    return splits

def hybrid_strassen(a, b, crossover=45):
    n = len(a)
    
    if n == 1:
        return [[a[0][0] * b[0][0]]]
    
    if n < crossover:
        return traditional_multiplication(a, b)
    
    As,Bs = split(a),split(b)
    
    products = [
        hybrid_strassen(As[0], subtract(Bs[1], Bs[3]),crossover), # P1 = A(F-H)
        hybrid_strassen(plus(As[0], As[1]), Bs[3],crossover), # P2 = (A+B)H
        hybrid_strassen(plus(As[2], As[3]), Bs[0],crossover), # P3 = (C+D)E
        hybrid_strassen(As[3], subtract(Bs[2], Bs[0]),crossover), # P4 = D(G-E)
        hybrid_strassen(plus(As[0], As[3]), plus(Bs[0], Bs[3]),crossover), # P5 = (A+D)(E+H)
        hybrid_strassen(subtract(As[1], As[3]), plus(Bs[2], Bs[3]),crossover), # P6 = (B-D)(G+H)
        hybrid_strassen(subtract(As[2], As[0]), plus(Bs[0], Bs[1]),crossover), # P7 = (C-A)(E+F)
    ]
    
    subresults = [
        plus(plus(products[4], products[5]), subtract(products[3], products[1])), # -P2 + P4 + P5 + P6
        plus(products[0], products[1]), # P1 + P2
        plus(products[2], products[3]), # P3 + P4
        plus(plus(products[4], products[6]), subtract(products[0], products[2])) # P1 - P3 + P5 + P7
    ]
    
    res = []
    for i in range(len(subresults[0])):
        res.append(subresults[0][i] + subresults[1][i])
    for i in range(len(subresults[2])):
        res.append(subresults[2][i] + subresults[3][i])
        
    # remove padding
    if n % 2:
        del res[-1]
        for r in res:
            del r[-1]
    return res

def generate_matrix(size):
    res = []
    for i in range(size):
        res.append([random.randint(0, 2) for _ in range(size)])
    return res

def expected(p):
    return 178433024 * (p ** 3)

def main():
    argv = sys.argv
    size = int(argv[2])
    input_file = argv[3]
    crossover = 50
    n = crossover
    a = [[0 for i in range(size)] for j in range(size)]
    b = [[0 for i in range(size)] for j in range(size)]
    
    with open(input_file) as f:
        lines = f.read().splitlines()
        nums = [int(_) for _ in lines]
        
        for i in range(size):
            a[i] = nums[0:size]
            del nums[0:size]
        for i in range(size):
            b[i] = nums[0:size]
            del nums[0:size]
        
        res = hybrid_strassen(a, b, n)
        for i in range(size):
            print(res[i][i])
        
    return


if __name__ == "__main__":
    main()
    
    # option = "Q2"
    # if option == "Q2":
        
    #     ####### Question 2 #######
    #     strassen_means = []
    #     traditional_means = []
    #     repeats = 50
    #     crossovers = 100
    #     startp = 20
    #     for n in range(startp, crossovers):
    #         strassen_mean = 0
    #         traditional_mean = 0
    #         for i in range(repeats):
    #             a = generate_matrix(n+1)
    #             b = generate_matrix(n+1)
    #             # traditional
    #             start = perf_counter()
    #             res = traditional_multiplication(a, b)
    #             traditional_mean += perf_counter() - start
    #             # strassen
    #             start = perf_counter()
    #             res = hybrid_strassen(a, b, n)
    #             strassen_mean += perf_counter() - start
    #         strassen_mean /= repeats
    #         traditional_mean /= repeats
    #         strassen_means.append(strassen_mean)
    #         traditional_means.append(traditional_mean)
            
    # elif option == 'Q3':
    #     ####### Question 3 #######
    #     crossover = 80
    #     size = 1024
    #     means = []
    #     repeats = 50
    #     ps = [0.01, 0.02, 0.03, 0.04, 0.05]
    #     for p in ps:
    #         print(p)
    #         mean = 0
    #         for rep in range(repeats):
    #             adjM = [[0 for i in range(size)] for j in range(size)]
    #             for i in range(size):
    #                 for j in range(i):
    #                     if random.random() < p:
    #                         adjM[i][j] = 1
    #                         adjM[j][i] = 1
    #             result = hybrid_strassen(hybrid_strassen(adjM, adjM, crossover), adjM, crossover)
    #             mean += sum([result[i][i] for i in range(size)]) / 6
    #         mean /= repeats
    #         means.append(mean)
            
    #         mydf = pd.DataFrame({'value': mean, 'p': p}, index = [0])
    #         mydf.to_csv(f"p_{p}_{repeats}.csv")
    #         # print(means)
            
    #     expects = [expected(i) for i in ps]
    #     print(expects)
    #     print(means)
    
    
    ####### Question 2 Plots #######
    ####### 1: odd runtime #######
    # ranges = [k for k in range(startp,crossovers) if k % 2] # odd
    # strassen_odd = [strassen_means[i-startp] for i in ranges]
    # traditional_odd = [traditional_means[i-startp] for i in ranges] 
    # fig, ax = plt.subplots(figsize = (12,12))
    # plt.plot(ranges, strassen_odd, label = "strassen")
    # plt.plot(ranges, traditional_odd, label = "traditional")
    # plt.title(f"Runtime of Strassen's and Traditional algorithm over {repeats} repeats (odd n)", fontsize = 12)
    # plt.xlabel("Crossover", fontsize = 12)
    # plt.ylabel("Average runtime", fontsize = 12)
    # plt.legend(loc = 'best', fontsize = 12)
    
    ####### 2: even runtime #######
    # ranges = [k for k in range(startp,crossovers) if not k % 2] # even
    # strassen_even = [strassen_means[i-startp] for i in ranges]
    # traditional_even = [traditional_means[i-startp] for i in ranges] 
    # fig, ax = plt.subplots(figsize = (12,12))
    # plt.plot(ranges, strassen_even, label = "strassen")
    # plt.plot(ranges, traditional_even, label = "traditional")
    # plt.title(f"Runtime of Strassen's and Traditional algorithm over {repeats} repeats (even n)", fontsize = 12)
    # plt.xlabel("Crossover", fontsize = 12)
    # plt.ylabel("Average runtime", fontsize = 12)
    # plt.legend(loc = 'best', fontsize = 12)
    
    ####### 3: odd diff #######
    # ranges = [k for k in range(startp,crossovers) if k % 2] # odd
    # print(ranges)
    # strassen_odd = [strassen_means[i-startp] for i in ranges]
    # traditional_odd = [traditional_means[i-startp] for i in ranges] 
    # differences = [traditional_odd[i] - strassen_odd[i] for i in range(len(ranges))]
    # fig, ax = plt.subplots(figsize = (12,12))
    # plt.plot(ranges, differences, label = 'difference')
    # plt.plot(ranges, [0]*(len(ranges)), label = 'zero line')
    # plt.title(f"Difference of Runtime of Traditional and Strassen's over {repeats} repeats (odd n)", fontsize = 12)
    # plt.xlabel("Crossover", fontsize = 12)
    # plt.ylabel("Difference of Average Runtime", fontsize = 12)
    # plt.ylim([-0.05, 0.05])
    # # plt.ylim([-0.5, 0.5])
    # plt.legend(fontsize = 12)

    ####### 4: evem diff #######
    # ranges = [k for k in range(startp,crossovers) if not k % 2] # even
    # print(ranges)
    # strassen_even = [strassen_means[i-startp] for i in ranges]
    # traditional_even = [traditional_means[i-startp] for i in ranges] 
    # differences = [traditional_even[i] - strassen_even[i] for i in range(len(ranges))]
    # fig, ax = plt.subplots(figsize = (12,12))
    # plt.plot(ranges, differences,label = 'difference')
    # plt.plot(ranges, [0]*(len(ranges)), label = 'zero line')
    # plt.title(f"Difference of Runtime of Traditional and Strassen's over {repeats} repeats (even n)", fontsize = 12)
    # plt.xlabel("Crossover", fontsize = 12)
    # plt.ylabel("Difference of Average Runtime", fontsize = 12)
    # plt.ylim([-0.05, 0.05])
    # plt.legend(fontsize = 12)

    
