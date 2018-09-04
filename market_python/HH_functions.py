"""
Defines functions for the HH

Uses direct setting of system mode
"""
import gridlabd_functions
import numpy as np
from HH_global import *

#Bid functions
def bid_rule_HVAC(house, mean_p, var_p, interval):
	control_type = gridlabd_functions.get(house,'control_type')['value']
	k = float(gridlabd_functions.get(house,'k')['value'][1:])
	
	T_c_set = float(gridlabd_functions.get(house,'T_c_set_0')['value'][1:])
	T_h_set = float(gridlabd_functions.get(house,'T_h_set_0')['value'][1:])
	T_curr = float(gridlabd_functions.get(house,'air_temperature')['value'][1:-5])
	#calculate energy
	hvac_q = float(gridlabd_functions.get(house,'cooling_demand')['value'][1:-3]) * interval / (60*60)
	heat_q = float(gridlabd_functions.get(house,'heating_demand')['value'][1:-3]) * interval / (60*60)

	#State of appliance in previous period
	status = gridlabd_functions.get(house,'state')['value']
	
	if 'deadband' in control_type:
		# cooling
		if T_curr > T_c_set + k:
			bid_price = 1
			bid_quantity = hvac_q	
			gridlabd_functions.set(house,'bid_mode','COOL')		
			return bid_quantity, bid_price, status
		# heating
		elif T_curr < T_h_set - k:
			bid_price = 1
			bid_quantity = heat_q	
			gridlabd_functions.set(house,'bid_mode','HEAT')			
			return bid_quantity, bid_price, status
		# no activity
		else:
			bid_price = 0
			bid_quantity = 0
			gridlabd_functions.set(house,'bid_mode','NONE')	
			return bid_quantity, bid_price, status
	
	elif 'trans' in control_type:
		# Non-bid region size between cooling and heating [F]
		epsilon = 2
		bid_price = transactive_price(house, T_curr, T_c_set, T_h_set, mean_p, var_p, epsilon)
		if T_curr > T_c_set - (T_c_set - T_h_set)/2 + epsilon/2: #above T_c_zero
			bid_quantity = hvac_q
			gridlabd_functions.set(house,'bid_mode','COOL')
		elif T_curr < T_h_set + (T_c_set - T_h_set)/2 - epsilon/2: #below T_h_zero
			bid_quantity = heat_q
			gridlabd_functions.set(house,'bid_mode','HEAT')
		else:
			bid_quantity = 0
			gridlabd_functions.set(house,'bid_mode','NONE')
		return bid_quantity, bid_price
	else:
		print 'Bid reserve price could not be calculated'
		return 0,0,False

# with non-bid region of size epsilon between T_h and T_c
def transactive_price(house, T_curr, T_c_set, T_h_set, mean_p, var_p, epsilon):
	T_zero_h = T_h_set + (T_c_set - T_h_set)/2 - epsilon/2
	T_zero_c = T_c_set - (T_c_set - T_h_set)/2 + epsilon/2
	T_max = float(gridlabd_functions.get(house,'T_max')['value'][1:])
	T_min = float(gridlabd_functions.get(house,'T_min')['value'][1:])
	k = float(gridlabd_functions.get(house,'k')['value'][1:])
	if T_curr > T_max or T_curr < T_min:
		return 1 #max price
	# cooling
	elif T_curr > T_zero_c:
		#Remains here if comfort settings are changed during operation
		m = (mean_p + k * np.sqrt(var_p))/(T_max - T_zero_c)
		gridlabd_functions.set(house,'m',m)
		n = - m * T_zero_c
		gridlabd_functions.set(house,'n',n)
		#if house == houselist[no_house]:
		#	print 'Cooling'
		#	print mean_p
		#	print k
		#	print np.sqrt(var_p)
		#	print T_max
		#	print T_zero_c
		#	print m
		#	print n
		#	print (m * T_curr + n)
		return (m * T_curr + n)
	# heating
	elif T_curr < T_zero_h:
		m = (mean_p + k * np.sqrt(var_p))/(T_min - T_zero_h)
		gridlabd_functions.set(house,'m',m)
		n = - m * T_zero_h
		gridlabd_functions.set(house,'n',n)
		#if house == houselist[no_house]:
		#	print 'Heating'
		#	print mean_p
		#	print k
		#	print np.sqrt(var_p)
		#	print T_min
		#	print T_zero_h
		#	print m
		#	print n
		#	print (m * T_curr + n)
		return (m * T_curr + n)
	else:
		return 0

#Set rule: control HVAC by control of system mode
def set_HVAC_direct(house,control_type,bid_price,Pd):
	if bid_price >= Pd and bid_price > 0: #to exclude consumption when price is zero
		#Appliance is active
		gridlabd_functions.set(house,'state',True)
		#switch on HVAC
		if 'COOL' in gridlabd_functions.get(house,'bid_mode')['value']:
			gridlabd_functions.set(house,'system_mode','COOL')
		elif 'HEAT' in gridlabd_functions.get(house,'bid_mode')['value']:
			gridlabd_functions.set(house,'system_mode','HEAT')
		else:
			print 'Check bid mode - there might be an inconsistency in bidding and actual behavior'
		return
	else:
		#Appliance is not active
		gridlabd_functions.set(house,'state',False)
		#turn off HVAC
		gridlabd_functions.set(house,'system_mode','OFF')
		return

#Set rule: control HVAC by control of set point
def set_HVAC_setpoint(house,control_type,bid_price,Pd):

	#Set state: Load is active in that period
	if bid_price >= Pd:
		gridlabd_functions.set(house,'state',True)
	else:
		gridlabd_functions.set(house,'state',False)

	if 'deadband' in control_type:
		if bid_price >= Pd and bid_price > 0: #to exclude consumption when price is zero
			#switch on HVAC
			if 'COOL' in gridlabd_functions.get(house,'bid_mode')['value']:
				gridlabd_functions.set(house,'system_mode','COOL')
			elif 'HEAT' in gridlabd_functions.get(house,'bid_mode')['value']:
				gridlabd_functions.set(house,'system_mode','HEAT')
			else:
				print 'Check bid mode - there might be an inconsistency in bidding and actual behavior'
			return
		else:
			#turn off HVAC
			gridlabd_functions.set(house,'system_mode','OFF')
			#gridlabd_functions.set('control_1','control','OFF')
			return

	elif ('trans' in control_type): 

		m = float(gridlabd_functions.get(house,'m')['value'])
		n = float(gridlabd_functions.get(house,'n')['value'])
		T_max = float(gridlabd_functions.get(house,'T_max')['value'][1:])
		T_min = float(gridlabd_functions.get(house,'T_min')['value'][1:])

		# if house == houselist[no_house]:
		# 		print 'Set HVAC'
		# 		print gridlabd_functions.get(house,'bid_mode')['value']
		# 		print Pd
		# 		print n
		# 		print m
		# 		if m>0.0:
		# 			print ((Pd - n)/m)

		#change setpoint on HVAC
		if 'COOL' in gridlabd_functions.get(house,'bid_mode')['value']:
			gridlabd_functions.set(house,'system_mode','COOL')
			# calculate new setpoint
			T_c_set_new = (Pd - n)/m
			if T_c_set_new > T_max:
				gridlabd_functions.set(house,'cooling_setpoint',T_max)
			else:
				gridlabd_functions.set(house,'cooling_setpoint',T_c_set_new)
		
		elif 'HEAT' in gridlabd_functions.get(house,'bid_mode')['value']:
			gridlabd_functions.set(house,'system_mode','HEAT')
			#calculate new setpoint
			T_h_set_new = (Pd - n)/m
			if T_h_set_new < T_min:
				gridlabd_functions.set(house,'heating_setpoint',T_min)
			else:
				gridlabd_functions.set(house,'heating_setpoint',T_h_set_new)
		else:
			gridlabd_functions.set(house,'system_mode','OFF')
		return
	else:
		print 'HVAC could not be set'
		return