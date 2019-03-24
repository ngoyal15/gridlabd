import re

debug_enable = True
def debug(msg) :
	if debug_enable :
		print("DEBUG: %s" % msg)

class GlmParser :
	def __init__(self,yfile="glmparser.y") :
		self.directives = {"START":[], "END":[]};
		self.targets = {}
		self.classname = yfile.replace(".y","")
		with open(yfile,"r") as f :
			terminal = None
			target = None
			linenum = 0
			for line in [x.strip() for x in f.readlines()] :
				try :
					linenum += 1
					if len(line) == 0 : # empty line
						continue;
					elif line[0] == "#" : # comment line
						continue;
					elif line[0] == "%" : # directive
							self.directive(line[1:].strip())
					elif line[0:1] == "::" : # terminal handler
						handler = line[2:].strip()
						if not terminal :
							raise Exception("handler '%s' without terminal" % (handler))
						self.handler(target,terminal,handler)
					elif line[0] == ":" : # terminal
						terminal = line[1:].strip()
						if not target :
							raise Exception("terminal '%s' without target" % (terminal))
						self.terminal(target,terminal)
					else : # target
						target = line
						self.targets[target] = {}
				except Exception as e:
					print("%s(%d): %s" % (yfile,linenum,e))
					raise

	def directive(self,text) :
		debug("directive(text='%s')"%(text))
		items = re.sub("[ \t]+"," ",text).split(" ")
		if not items :
			raise Exception("directive(text='%s'): missing directive" % (text))
		if items[0] not in self.directives :
			raise Exception("directive(text='%s'): directive '%s' is invalid" % (text,items[0]))
		if not self.directives[items[0]] :
			if len(items) > 1 :	
				self.directives[items[0]] = "".join(items[1:])
		else :
			raise Exception("directive(text='%s'): directive '%s' occurred a second time" % (text,items[0]))

	def terminal(self,target,text) :
		debug("terminal(target='%s',text='%s')" % (target,text))
		if not target in self.targets or not type(self.targets) is list :
			self.targets[target] = []
		items = re.sub("[ \t]+"," ",text).split(" ")
		self.targets[target].append(items)

	def handler(self,target,terminal,text) :
		debug("handler(target='%s',terminal='%s',text='%s'"%(target,terminal,text))
		target = self.targets[target]
		if not terminal in target or not type(target) is list:
			target[terminal] = []
		target[terminal].append(text)

	def __str__(self) :
		return ("%s : {\n\tdirectives : %s,\n\ttargets : %s\n\t}\n" % (repr(self),self.directives,self.targets))

	def write_h(self) :
		with open(self.classname+".h","w") as f :
			f.write("// automatically generated from {0}.y\n".format(self.classname))
			f.write("class {0}\n".format(self.classname))
			f.write("{\n")
			f.write("\ttypedef int PARSERSTATUS;\n")
			f.write("private:\n")
			f.write("public:\n")
			f.write("\t{0}(const char *file);\n".format(self.classname))
			f.write("\t~{0}(void);\n".format(self.classname))
			for target in self.targets :
				f.write("\tPARSERSTATUS {0}(PARSER);\n".format(target))
			f.write("};\n")

	def write_cpp(self) :
		with open(self.classname+".cpp","w") as f :
			f.write("// automatically generated from %{0}.y\n".format(self.classname))
			f.write("#include \"{0}.h\"\n".format(self.classname))
			f.write("{0}::{0}(const char *file)\n".format(self.classname))
			f.write("{\n")
			f.write("}\n")
			f.write("{0}::~{0}(void)\n".format(self.classname))
			f.write("{\n")
			f.write("}\n")
			for target in self.targets :
				self.write_target(f,target)

	def write_target(self,f,target) :
		f.write("{0}::PARSERSTATUS {0}::{1}(PARSER)\n".format(self.classname,target))
		f.write("{\n")
		for terminal in self.targets[target]:
			f.write("\tif ( {0} )\n".format(self.make_calls(terminal)))
			f.write("\t{\n")
			f.write("\t}\n")
		f.write("\treturn 0;\n")
		f.write("}\n")

	def make_calls(self,terminal) :
		calls = []
		for item in terminal :
			if item[0] == '[' :
				calls.append("match(PARSER,\"{0}\")".format(item))
			else :
				calls.append("{0}(PARSER)".format(item))
		return " && ".join(calls)

if __name__ == '__main__' :
	parser = GlmParser()
	parser.write_h()
	parser.write_cpp()

