import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def relationship(data, d = 1):
    data = data.T.reset_index().rename(columns = {'index' : 'n', 0: 'size'})
    data['n'] = data['n'].astype('int')
    
    fig = plt.figure(figsize = (10,8))
    if d == 1:
        plt.ylim(1.0,1.5)
        plt.plot(data['n'], data['size'])
        plt.xlabel("n", fontsize = 20)
        # plt.xscale('log')
        plt.ylabel("Average Tree Size", fontsize = 20)
        plt.title(f"Average Tree Size vs. N (Dimension {d})", fontsize = 20)
        plt.xticks(data['n'][[0,4,5,6,7,8,9]], fontsize = 20, rotation = 40)
        # plt.xticks(data['n'], fontsize = 20, rotation = 40)
    else:
        plt.plot(np.log2(data['n']), np.log2(data['size']))
        plt.xlabel("Log n", fontsize = 20)
        plt.ylabel("Log Average Tree Size", fontsize = 20)
        plt.title(f"Log Average Tree Size vs. Log n (Dimension {d})", fontsize = 20)
        plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.savefig(f'plot_{d}.pdf')
    plt.show()
    
if __name__ == '__init__':
    
    one = pd.read_csv("one_dimension_w_clip.csv")
    relationship(one, d = 1)
    
    two = pd.read_csv("two_dimension_w_clip.csv")
    relationship(two, d = 2)

    three = pd.read_csv("three_dimension_w_clip.csv")
    relationship(three, d = 3)

    four = pd.read_csv("four_dimension_w_clip.csv")
    relationship(four, d= 4)
    