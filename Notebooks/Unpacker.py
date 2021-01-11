# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 16:28:09 2021

@author: tombr
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
           
def importer():
    filename = input("Filename: ")
    data = pd.read_csv(filename, sep = "\t")
    
    #print(data.keys())
    
    time = data["time"]
    Susceptable = data['susceptible (total) median']
    Exposed = data['exposed (total) median']
    Infected = data['infectious (total) median']
    Recovered = np.array(data['cumulative recovered (total) median'])
    
    samples = len(time)
    recovered = [0]
    for i in range(0,samples-1):
        recovered.append(Recovered[i+1]-Recovered[i])
    
    return time, Susceptable, Exposed, Infected, recovered

    
def main():
    time, susceptable, exposed, infected, recovered = importer()
    
    fig, ax = plt.subplots()
    ax.plot(time, recovered)
    
main()