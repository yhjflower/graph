# coding=utf-8
import pandas as pd
import time
import numpy as np
import math
import random

Profits=pd.Series([135,139,149,150,156,163,173,184,\
         192,201,210,214,221,229,240])

Weights=pd.Series([70,73,77,80,82,87,90,94,98,106,\
         110,113,115,118,120])

Capacity=750


# 定义损失函数
def schedulecost(sol):
    get_profits=Profits[sol==1].sum()
    #get_weights=Weights[sol==1].sum()

    return get_profits



# 随机搜索算法
def randomoptimize(costf):
    best = 0
    bestr = None
    for i in range(0, 1000):
        # Create a random solution
        while 1:
            r = np.random.randint(2,size=len(Profits))
            if Weights[r==1].sum()<=Capacity: break

        # Get the cost
        cost = costf(r)

        # Compare it to the best one so far
        if cost > best:
            best = cost
            bestr = r
    return bestr,best


# 爬山法
def hillclimb(costf):
    # Create a random solution
    while 1:
        sol = np.random.randint(2, size=len(Profits))
        if Weights[sol == 1].sum() <= Capacity: break
    # Main loop
    while 1:
        # Create list of neighboring solutions
        neighbors = []

        for j in range(len(Profits)):
            # One away in each direction

                if sol[j] ==0:
                    neighbors.append(np.concatenate((sol[0:j],[sol[j] + 1],sol[j + 1:])))
                if sol[j] ==1:
                    neighbors.append(np.concatenate((sol[0:j],[sol[j] - 1],sol[j + 1:])))

        # See what the best solution amongst the neighbors is
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            if Weights[neighbors[j] == 1].sum() > Capacity:
                pass
            else:
                cost = costf(neighbors[j])
            if cost > best:
                best = cost
                sol = neighbors[j]

        # If there's no improvement, then we've reached the top
        if best == current:
            break
    return sol,best


def get(x):      #随机将背包中已经存在的物品取出
    while 1:
        ob = random.randint(0,14);
        if(x[ob]==1): x[ob]=0;break;

def put(x):      #随机放入背包中不存在的物品
    while 1:
        ob = random.randint(0,14);
        if(x[ob]==0): x[ob]=1;break;

# 模拟退火算法
def annealingoptimize(costf, T=100.0, cool=0.95, balance=100):
    global  vec,best,best_3
    for k in range(balance):
        vecb = vec[:]
        i = np.random.randint(0, len(Profits))
        # Create a new list with one of the values changed
        if vecb[i] ==0:
            get(vecb)
            vecb[i] +=1
        else:
            put(vecb)
            vecb[i]-=1
        if Weights[vecb == 1].sum() > Capacity: continue
        # Calculate the current cost and the new cost
        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e, -(ea-eb) / T)
        # Is it better, or does it make the probability
        # cutoff?
        if (eb > ea or random.random() < p):
            vec = vecb
        if eb>best:
            best=eb
            best_3=vecb[:]




s_1,best_1 = randomoptimize(schedulecost)
print('随机森林')
print(s_1 ,best_1)

s_2 ,best_2= hillclimb(schedulecost)
print('爬山法')
print(s_2 ,best_2)

T,cool=200.0 ,0.95
best=0
best_3=[0]*15
while 1:
    vec = np.random.randint(2, size=len(Profits))
    if Weights[vec == 1].sum() <= Capacity: break
while T>0.1:
    annealingoptimize(schedulecost,T,cool)
    # Decrease the temperature
    T = T * cool
print('模拟退火')
print(vec,schedulecost(vec))
