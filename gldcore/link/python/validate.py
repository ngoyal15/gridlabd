import sys
assert(sys.version_info.major>2)

import gridlabd

class MyTest(gridlabd.GldObject) :
	def __init__(self) :
		self.array_value = [5.0,6.0,7.0]
		self.real_value = 2.34;
		self.integer_value = 1
		self.string_value = 'abc'
	def on_sync(self,t0) :
		return int(t0/3600+1)*3600
	def __repr__(self):
		print(self.array_value,self.real_value)

a = MyTest
print(a)

gridlabd.command('validate.glm')
gridlabd.command('-D')
gridlabd.command('suppress_repeat_messages=FALSE')
gridlabd.command('--warn')
gridlabd.start('wait')
gridlabd.save('done.json');
gridlabd.save('done.glm');


