import os
import rwText
import json
from cvxpy import *
import random

import datetime
import gridlabd_functions
from HH_global import *
import HH_functions as HHfct
import market_functions as Mfct
from HHoptimizer_funcDefs import *

sim_time = os.getenv("clock")
interval = int(gridlabd_functions.get('retail','interval')['value'])/60

#Run market only every five minutes
#Remark: The file is currently called at every event (i.e. 1min) but the main part not executed.
#Potentially, it would be faster to do the check in markets? 
if (sim_time[17:19] == "00") and (int(sim_time[15:16]) % interval == 0):

	print 'Precommit'
	print sim_time
	
	#Initialize market
	retail = Mfct.Market()
	retail.reset()
	retail.Pmin = 0.1
	retail.Pmax = 1.0

	#Get historical parameters from msql database!!!
	mean_p = float(gridlabd_functions.get('FIR2_filter','value2')['value'][1:])
	print 'mean_p'
	if mean_p == 0.0:
		mean_p = 0.5
	print mean_p
	var_p = 0.1

	###
	#Demand side
	###

	bid_prices = []
	bid_quantities = []
	for house in houselist:
		bid_quantity, bid_price, status = HHfct.bid_rule_HVAC(house, mean_p, var_p, interval)
		gridlabd_functions.set(house,'p_bid',bid_price)
		gridlabd_functions.set(house,'q_bid',bid_quantity)
		bid_prices += [bid_price] #Can we use the market object to store bids for dispatch?
		bid_quantities += [bid_quantity]
		retail.buy(bid_quantity,bid_price,active=status)

	#Include unresponsive load
	load_SLACK = float(gridlabd_functions.get('node_149','measured_real_power')['value'][:-1])
	print 'Last measured volume'
	print load_SLACK
	unresp_load = load_SLACK - retail.get_active()
	retail.buy(unresp_load)

	###
	#Supply side
	###

	supply_costs = random.random()
	print'supply costs: '+str(supply_costs)
	#Max capacity (later from CC)
	C = 10
	retail.sell(C,supply_costs)

	###
	#Market clearing
	###

	retail.clear()
	Pd = retail.Pd # cleared demand price
	gridlabd_functions.set('retail','price',Pd)
	print 'retail price '+str(Pd)

	###
	#Redistribute prices and quantities to market participants
	###

	#Send price information to market
	
	#Distribute prices to houses
	for house in houselist: #Deadband only currently implemented!!!!
		#HHfct.set_HVAC_direct(house,'deadband',bid_prices[houselist.index(house)],Pd) #bidding mode should be stored locally
		control_type = gridlabd_functions.get(house,'control_type')['value']
		HHfct.set_HVAC_setpoint(house,control_type,bid_price,Pd)
		#if house == houselist[no_house]: 
		#	print gridlabd_functions.get(house,'system_mode')['value']

