import numpy as np
import math
import pandas as pd
from Ubike2_0_config import *

def minimum_cost(T, D, V, pillarNum, CostPerBike, CosrPerStop):
    for t in range(1, T + 1):
        
        lbound = int(pillarNum * (1/3))
        hbound = int(pillarNum * (2/3))

        for y in range(lbound, hbound+1):
            choices = {}
            if(D[T-t] > 0 and y-D[T-t] < lbound):#需要補車
                # 少 y-D[T-t][s] 台車
                min_x = lbound-(y-D[T-t])#至少滿足需求
                max_x = hbound - (y-D[T-t])#至多不超過上限
                choices["situation"] = "補車"
            elif(D[T-t] < 0 and y-D[T-t] > hbound):#需要移車
                #有 -D[s][t]-(hbound-y) 車沒位置停
                min_x = -D[T-t]-(hbound-y)           #至少滿足需求
                max_x = (y-D[T-t])-lbound           #至多不小魚下限
                choices["situation"] = "移車"
            else: #不用移or補
#                     print("stop",s, ": ", "no need, lbound={}, hbound={}, D={}, y={}".format(lbound, hbound, D[T-t][s], y))
                choices["situation"] = "不用去"
                min_x = max_x = 0

            choices["pillar"] = pillarNum
            choices["lbound"] = lbound
            choices["hbound"] = hbound
            choices["D"] = D[T-t]
            choices["min_x"] = min_x
            choices["max_x"] = max_x
#             print("y={}".format(y), ": ", choices)

            
            opt_x = -1
            if t == 1:
                min_cost = 9999999
                for x in range(min_x, max_x+1):
                    z = 1 if x > 0 else 0
                    cost = CostPerBike * x + CosrPerStop * z
                    if cost < min_cost: 
                        min_cost = cost
                        opt_x = x
            elif choices["situation"] == "補車": 
                min_cost = 9999999 
                for x in range(min_x, max_x+1):
                    z = 1 if x > 0 else 0
                    cost = V[t - 1][y + x - D[T - t]-lbound][0] + CostPerBike * x + CosrPerStop * z 
                    if cost < min_cost: 
                        min_cost = cost
                        opt_x = x
            elif choices["situation"] == "移車": 
                min_cost = 9999999
                for x in range(min_x, max_x+1):
                    z = 1 if x > 0 else 0
                    cost = V[t - 1][y - x - D[T - t]-lbound][0] + CostPerBike * x + CosrPerStop * z 
                    if cost < min_cost: 
                        min_cost = cost
                        opt_x = x
            elif choices["situation"] == "不用去": 
                min_cost = 0
                opt_x = 0
            
#             print("t={}, y={}, opt_x={}".format(t,y,opt_x))
            V[t][y-lbound] = [min_cost, opt_x]
        
        
def print_min_cost(V, head):
    print("  ",end="")
    for i in head:
        print("{:>3}".format(i), end="")
    print()
    for t in range(len(V)):
        print(t, end=" ")
        for y in range(len(V[0])):
            if(t == 0):
                print("{:>3}".format(0), end="")
            else:
                print("{:>3}".format(V[t][y][0]), end="")
            #print(V[t][y], end = " ")
        print()
    print()



def getResult(TotalV, T, stopNum):
    nuTV = np.array(TotalV)
    nuTV = nuTV.transpose()

    result = pd.DataFrame(columns = (['TimePeriod','stopSet','minCost','x']))

    for t in range(T,0,-1):
        SetInT = pd.Series({'TimePeriod':T-t,
                                    'stopSet'  :list(),
                                    'minCost'  :0,
                                    'x' : 0,
                                    # 'Action':list()
                                    })
        minCost = 0
        for s in range(stopNum):
            nuStop = np.array(nuTV[t][s])
            nuStop = nuStop.transpose()
            minI = nuTV[t][s][0].index(min(nuTV[t][s][0]))
            minCost += nuTV[t][s][minI][0]
            x = nuTV[t][s][minI][1]
            if(nuTV[t][s][minI][0]!=0):
                SetInT['stopSet'].append(s)
                # SetInT['Action'].append(nuTV[t][s][minI][2])
        SetInT['minCost'] = minCost
        SetInT['x'] = x
        result = result.append(SetInT, ignore_index=True)
    return result

