import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def coefficients(data, d = 2):
    data = data.T.reset_index().rename(columns = {'index' : 'n', 0: 'size'})
    data['n'] = data['n'].astype(int)
    reg = LinearRegression().fit(np.log2(data[['n']]), np.log2(data['size']))
    print(f"Dimension: {d}")
    print(f"Coefficients: {reg.coef_[0]:.5f}.")
    print(f"Intercept: {reg.intercept_:.5f}.")
    
data = pd.read_csv("two_dimension_w_clip.csv")
coefficients(data, d = 2)
data = pd.read_csv("three_dimension_w_clip.csv")
coefficients(data, d = 3)
data = pd.read_csv("four_dimension_w_clip.csv")
coefficients(data, d = 4)