import pickle



CostPerBike = 1
CosrPerStop = 5
setupCost = 10



with open("demand/3stop_1hour.pkl", 'rb') as f:
        data = pickle.load(f)
# print(data)
StopPillarNum = list()
StopD = list()

T = 0
for s in data:
	StopPillarNum.append(data[s]['pillarNum'])
	StopD.append(data[s]['Demand'])
	T = len(data[s]['Demand'])

stopNum = len(data)
TotalV = [list() for i in range(stopNum)]     #[Stop[t[y[]]]]


