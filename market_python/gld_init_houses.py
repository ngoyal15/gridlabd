import os
import gridlabd_functions
from HH_global import *
import random
import pandas
import pycurl
import json
from StringIO import StringIO
import numpy as np

print('Initialize')

#Get list of house objects in GLM file and assign to global GLD variable "houselist"
houses = gridlabd_functions.find('class=house')
houselist = [];

for house in houses :
	name = house['name']
	houselist.append(name)

gridlabd_functions.set('houselist',';'.join(houselist))

#Implement preferences
#Overwrites preferences in GLM file!!
for house in houselist:
	#Not active in previous period
	gridlabd_functions.set(house,'state',False)

	#Stores original setpoints (differ from HVAC system set points)
	gridlabd_functions.set(house,'T_c_set_0',float(gridlabd_functions.get(house,'cooling_setpoint')['value'][1:-5]))
	gridlabd_functions.set(house,'T_h_set_0',float(gridlabd_functions.get(house,'heating_setpoint')['value'][1:-5]))

	# Preference parameter for bidding
	control_type = np.random.choice(['deadband','transactive'], p=[0,1])
	gridlabd_functions.set(house,'control_type',control_type)
	gridlabd_functions.set(house,'p_bid',0.0)
	gridlabd_functions.set(house,'q_bid',0.0)

	# Switch off house-internal thermostat control
	if control_type == 'deadband':
		gridlabd_functions.set(house,'thermostat_control','NONE') #Lily's model does not include that
	gridlabd_functions.set(house,'system_mode','OFF')
	gridlabd_functions.set(house,'bid_mode','OFF')

	if control_type == 'deadband':
		# Set absolute deadband
		gridlabd_functions.set(house,'k',round(random.uniform(2,5),1))
	elif 'trans' in control_type:	
		# Set sensitivity
		gridlabd_functions.set(house,'k',round(random.uniform(0.2,0.5),1))
		delta = round(random.uniform(2,5),1) #Difference between set points and maximum and minimum temperature
		gridlabd_functions.set(house,'T_max',float(gridlabd_functions.get(house,'T_c_set_0')['value'][1:])+delta)
		gridlabd_functions.set(house,'T_min',float(gridlabd_functions.get(house,'T_h_set_0')['value'][1:])-delta)
		gridlabd_functions.set(house,'m',0)
		gridlabd_functions.set(house,'n',0)
	else:
		sys.exit('No such control type')