import os
import rwText
import json
from cvxpy import *
import random

import gridlabd_functions
from HH_global import *
import HH_functions as HHfct
import market_functions as Mfct
from HHoptimizer_funcDefs import *

"""
Purpose of this code:
- read house temperatures
- (check state of HVAC)
- write bids 
- write price to market
- write T_set to house
"""
#
sim_time = os.getenv("clock")
print 'Precommit'
print sim_time

#Initialize market
retail = Mfct.Market()
retail.reset()
retail.Pmin = 0.1
retail.Pmax = 1.0

###
#Demand side
###

for house in houselist:
	bid_quantity, bid_price = HHfct.bid_rule_HVAC('node1_House1','deadband',k,T_c_set)
	retail.buy(bid_quantity,bid_price)

#Include zip load

###
#Supply side
###

supply_costs = random.random()
print'supply costs: '+str(supply_costs)
retail.sell(10,supply_costs)

###
#Market clearing
###

retail.clear()
Pd = retail.Pd # cleared demand price
print 'retail price '+str(Pd)
#retail.plot()

###
#Redistribute prices and quantities to market participants
###

#Send price information to market
gridlabd_functions.set('retail','price',Pd)
#Distribute prices to houses
for house in houselist:
	HHfct.set_HVAC(house,'deadband',bid_price,Pd) #bidding mode should be stored locally

