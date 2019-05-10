import gridlabd

class myclass:
	shared_integer = 0
	shared_real = 0.0
	shared_string = "zero"
	shared_dict = {"integer": 0, "real": 0.0, "string": "zero"}
	shared_list = ["integer", 0, "real", 0.0, "string", "zero"]
	def __init__(self):
		self.integer = 0
		self.real = 0.0
		self.string = "zero"
		self.dict = {"integer": 0, "real": 0.0, "string": "zero"}
		self.list = ["integer", 0, "real", 0.0, "string", "zero"]
	def on_create(self,t):
		return
	def on_init(self,t):
		return
	def on_precommit(self,t):
		return
	def on_presync(self,t):
		return
	def on_sync(self,t):
		return
	def on_postsync(self,t):
		return
	def on_commit(self,t):
		return
	def on_term(self,t):
		return

if __name__ == '__main__':
	gridlabd.link_class(myclass(),"myclass")