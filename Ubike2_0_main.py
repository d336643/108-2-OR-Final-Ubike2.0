from Ubike2_0_config import *
from Ubilke2_0_func import *
import numpy as np
import pandas as pd




# get the optimize DP result of each stop
for s in range(stopNum):
    D = StopD[s]
    PillarNum = StopPillarNum[s]
    V = [0] * (T + 1)
    for i in range(len(V)):
        V[i] = [0] * (int(PillarNum * (2/3))- int(PillarNum * (1/3)) + 1)
    
    minimum_cost(T, D, V, PillarNum, CostPerBike, CosrPerStop)
    head = list(range(int(PillarNum * (1/3)),int(PillarNum * (2/3))+1))
    print_min_cost(V, head)
    
    TotalV[s]= V
    
# Output recommandation
result = getResult(TotalV, T, stopNum)

print(result)


