import numpy
import matplotlib.pyplot as plt 
import pandas

config = {
	"internal_cop": 0.8, # pu
	"heating_cop": 2.5, # pu
	"cooling_cop": 3.5, # Btu/Wh
	"system_efficiency" : 0.61, # pu
	"house_ua":	575.0, # Btu/degF.h
	"Tb": -7, # balance temperature offset
	"range" : [-2,+2], # balance temperature search range
	"gas_enduses" : False, # True if dryer and range use gas instead of electricity
}

eta_i = config["internal_cop"] * 3421. # Btu/kWh
eta_h = config["heating_cop"] / config["system_efficiency"] * 3421. # Btu/kWh
eta_c = config["cooling_cop"] / config["system_efficiency"] * 1000. # Btu/kWh

print("eta_i: %.0f Btu/kWh, eta_h: %.0f Btu/kWh, eta_c: %.0f Btu/kWh" % (eta_i,eta_h,eta_c))

data = pandas.read_csv("house.csv",header=None,skiprows=8,names=["t","To","Ta","E","Th","Tc"],converters={"E":lambda s:abs(complex(s))})

t = data.index
To = data["To"]
Ta = data["Ta"]
E = data["E"]
Th = data["Th"]
Tc = data["Tc"]

dx = None
save = {}
print(" Bh   Bc    dd     Qb    Uh   Uc   UA ")
print("---- ---- ------ ------ ---- ---- ----")

for Bh in range(config["Tb"]+config["range"][0],config["Tb"]+config["range"][1]+1):
	for Bc in range(Bh+config["range"][0],Bh+config["range"][1]+1):
		T = []
		Q = []
		T1 = []
		T2 = []
		T3 = []
		Q1 = []
		Q2 = []
		Q3 = []
		for h in range(1,len(t)) :
			if To[h] < Th[h]+Bh :
				T.append([1/eta_i,((Th[h]+Bh)-To[h])/eta_h,0])
				T1.append(To[h])
				Q1.append(E[h]-E[h-1])
			elif To[h] > Tc[h]+Bc :
				T.append([1/eta_i,0,(To[h]-(Tc[h]+Bc))/eta_c])
				T2.append(To[h])
				Q2.append(E[h]-E[h-1])
			else :
				T.append([1/eta_i,0,0])
				T3.append(To[h])
				Q3.append(E[h]-E[h-1])
			Q.append(E[h]-E[h-1])

		A = numpy.array(T)
		At = A.transpose()
		y = numpy.array(Q)
		x = numpy.matmul(numpy.matmul(numpy.linalg.inv(numpy.matmul(At,A)),At),y)
		dd = abs(x[1] - x[2])
		if dx == None or dd < dx :
			save = {
				"Bh":Bh, 		"Bc":Bc,	
				"A":A.copy(),	"y":y.copy(),	"x":x.copy(),
				"T1":T1.copy(),	"Q1":Q1.copy(),
				"T2":T2.copy(),	"Q2":Q2.copy(),
				"T3":T3.copy(),	"Q3":Q3.copy(),
				}
			dx = dd

		print("%4d %4d %6.1f %6.0f %4.0f %4.0f %4.0f" %(Bh,Bc,dd,x[0],x[1],x[2],(x[1]+x[2])/2),flush=True)

inferred_UA = (save["x"][1]+save["x"][2])/2
baseload_kW = save["x"][0]/eta_i

print("Inferred UA.... %6.1f Btu/degF.h" % inferred_UA)
print("Baseload....... %6.1f kW" % baseload_kW)

plt.figure(1)
plt.scatter(save["T1"],save["Q1"],color='r')
plt.scatter(save["T2"],save["Q2"],color='b')
plt.scatter(save["T3"],save["Q3"],color='k')
plt.title("House UA ~ %.0f Btu/degF.h, Baseload ~ %.0f kW" % (inferred_UA,baseload_kW))
plt.grid()
plt.savefig("house.png")


