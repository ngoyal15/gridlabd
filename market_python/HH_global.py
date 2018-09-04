import gridlabd_functions

#Get list of house objects in GLM file and assign to global GLD variable "houselist"
houses = gridlabd_functions.find('class=house')
houselist = [];

for house in houses :
	name = house['name']
	houselist.append(name)

gridlabd_functions.set('houselist',';'.join(houselist))
#House to be tracked in print out / verbose
no_house = 0

#Preferences to be set in the HH
#k = 0.5		#Tolerable temperature deadband
# T_h_set = 68
# T_c_set = 71

# i = 0
# #Implement preferences
# for house in houselist:
# 	gridlabd_functions.set(house,'k',k)
# 	gridlabd_functions.set(house,'heating_setpoint',T_h_set)
# 	gridlabd_functions.set(house,'cooling_setpoint',T_c_set)
# 	i += 1