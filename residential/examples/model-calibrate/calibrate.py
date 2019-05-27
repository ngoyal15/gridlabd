"""
The program calibrates a house model in multiple steps

Step 1 - determine the baseload, total UA, and balance temperatures

"""
import numpy
import matplotlib.pyplot as plt 
import pandas

config = {
	"heat_fraction": 0.8, 		# fraction of energy use that ends up as heat in the house air [pu]
	"heating_cop": 2.5, 		# efficiency of the home heating system (~0.01 for none, ~2.5 for heat pumps, ~100 for gas units) [pu]
	"cooling_cop": 3.5, 		# efficiency of the home cooling system (~0.01 for none, ~3.5 for A/C units) Btu/Wh
	"system_efficiency" : 0.6, # overall performance factor the heating/cooling systems (~0.7-0.8 for forced air systems) [pu]
	"Bh": 60.0, 				# initial heating balance temperature (~60) [degF
	"Bc": 70.0, 				# initial cooling balance temperature (~70) [degF]
	"gas_enduses" : False, 		# True if dryer and range use gas instead of electricity
}

eta_i = config["heat_fraction"] * 3421. # Btu/kWh
eta_h = config["heating_cop"] / config["system_efficiency"] * 3421. # Btu/kWh
eta_c = config["cooling_cop"] / config["system_efficiency"] * 1000. # Btu/kWh

print("eta_i: %.0f Btu/kWh, eta_h: %.0f Btu/kWh, eta_c: %.0f Btu/kWh" % (eta_i,eta_h,eta_c))

data = pandas.read_csv("house.csv",header=None,skiprows=8,names=["t","To","Ta","E","Th","Tc"],converters={"E":lambda s:abs(complex(s))})

global evaluate_cache
evaluate_cache = {}
def evaluate(data,config,Bh,Bc,quick=False):
	key = Bh*100+Bc
	global evaluate_cache
	if quick and key in evaluate_cache.keys():
		return evaluate_cache[key]

	t = data.index
	To = data["To"]
	E = data["E"]

	T = []
	Q = []
	T1 = []
	T2 = []
	T3 = []
	Q1 = []
	Q2 = []
	Q3 = []
	for h in range(1,len(t)) :
		if To[h] < Bh :
			T.append([1/eta_i,(Bh-To[h])/eta_h,0])
			if not quick :
				T1.append(To[h])
				Q1.append(E[h]-E[h-1])
		elif To[h] > Bc :
			T.append([1/eta_i,0,(To[h]-Bc)/eta_c])
			if not quick :
				T2.append(To[h])
				Q2.append(E[h]-E[h-1])
		else :
			T.append([1/eta_i,0,0])
			if not quick :
				T3.append(To[h])
				Q3.append(E[h]-E[h-1])
		Q.append(E[h]-E[h-1])

	A = numpy.array(T)
	At = A.transpose()
	y = numpy.array(Q)
	x = numpy.matmul(numpy.matmul(numpy.linalg.inv(numpy.matmul(At,A)),At),y)
	dx = abs(x[1] - x[2])
	print("%5d %4d %4d %6.1f %6.0f %4.0f %4.0f %4.0f" % ( key, Bh, Bc, dx, x[0], x[1], x[2], (x[1]+x[2])/2), flush=True)
	result = {"dx":dx,"A":A,"y":y,"x":x,"T1":T1,"Q1":Q1,"T2":T2,"Q2":Q2,"T3":T3,"Q3":Q3}
	evaluate_cache[key] = result 
	return result

dx = None
save = {}
print("key    Bh   Bc    dd     Qb    Uh   Uc   UA ")
print("----- ---- ---- ------ ------ ---- ---- ----",flush=True)
done = False
Bh = config["Bh"]
Bc = config["Bc"]
while not done :
	xy = evaluate(data,config,Bh,Bc)
	x0 = evaluate(data,config,Bh-1,Bc,quick=True)
	x1 = evaluate(data,config,Bh+1,Bc,quick=True)
	y0 = evaluate(data,config,Bh,Bc-1,quick=True)
	y1 = evaluate(data,config,Bh,Bc+1,quick=True)
	dx = xy["dx"]
	done = True
	if x0["dx"] < dx :
		Bh -= 1
		done = False
	elif x1["dx"] < dx :
		Bh += 1
		done = False
	if y0["dx"] < dx :
		Bc -= 1
		done = False
	elif y1["dx"] < dx :
		Bc += 1
		done = False	

inferred_UA = (xy["x"][1]+xy["x"][2])/2
baseload_kW = xy["x"][0]/eta_i

print("Inferred UA.... %6.1f Btu/degF.h" % inferred_UA)
print("Baseload....... %6.1f kW" % baseload_kW)

plt.figure(1)
plt.scatter(xy["T1"],xy["Q1"],color='r')
plt.scatter(xy["T2"],xy["Q2"],color='b')
plt.scatter(xy["T3"],xy["Q3"],color='k')
plt.title("House UA ~ %.0f Btu/degF.h, Baseload ~ %.0f kW" % (inferred_UA,baseload_kW))
plt.grid()
plt.savefig("house.png")


