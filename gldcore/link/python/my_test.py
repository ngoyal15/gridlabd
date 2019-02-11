import gridlabd
import numpy

def on_init(t) :
	global record
	record = {}
	return True

def commit(obj,t) :
	global record
	record[gridlabd.get_global("clock")] = gridlabd.get_object("my_test")["x"]
	return gridlabd.NEVER

def on_term(t):
	global record
	values = list(map(lambda x:numpy.log(float(x)),record.values()))
	print("\nmean=%.3f, std=%.3f, count=%d" % (numpy.mean(values),numpy.std(values), len(values)))

class MyTest(gridlabd.GldObject) :
	def __init__(self,name=None) :
		print('name=%s'%name)
		gridlabd.GldObject.__init__(self,name=name)
		self.name = name
		self.array_value = [5.0,6.0,7.0]
		self.real_value = 2.34;
		self.integer_value = 1
		self.string_value = 'abc'
	def on_sync(self,t0) :
		return int(t0/3600+1)*3600
	def __repr__(self):
		print(self.array_value,self.real_value)
