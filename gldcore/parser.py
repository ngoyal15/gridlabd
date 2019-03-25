import sys
import re

debug_level = 9
def debug(level, msg) :
	if level < debug_level :
		print("DEBUG[%d]: %s" % (level,msg))

class GlmParser :
	def __init__(self,yfile="parser.y") :
		self.directives = {"BASE":None, "CLASS":None, "START":None, "END":[]};
		self.targets = {}
		self.yfile = yfile
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
					elif line[0:2] == "::" : # terminal
						terminal = line[2:].strip()
						if terminal :
							self.terminal(target,pattern,terminal)
					elif line[0] == ":" : # pattern
						pattern = line[1:].strip()
						self.target(target,pattern)
					else : # target
						target = line
						if target in self.targets.keys() :
							raise Exception("target '%s' is already defined" % (target))
						self.targets[target] = {}
				except Exception as e:
					print("%s(%d): %s" % (yfile,linenum,e))
					raise
		for item,value in self.directives.items() :
			if value == None :
				raise Exception("{0}: missing required '%{1}' directive".format(yfile,item))
		self.cppfile = self.directives["CLASS"] + ".cpp"
		self.hfile = self.directives["CLASS"] + ".h"
		if self.directives["START"] not in self.targets :
			raise Exception("{0}: START target {1} not defined".format(yfile,self.directives["START"]))
		for target,patterns in self.targets.items() :
			debug(2,"target = '%s', patterns = %s" % (target,patterns))
			for pattern in patterns :
				debug(3,"pattern = '%s'" % (pattern))
				if pattern[0] == "\"" :
					debug(3,"pattern = '%s' is a literal string" % (pattern))
					continue
				elif pattern[0] == "[" :
					debug(3,"pattern = '%s' is a pattern" % (pattern))
					continue
				elif re.fullmatch("[A-Z]+",pattern) and not pattern in self.targets.keys() :
					raise Exception("{0}: target {1} not defined".format(yfile,pattern))
				else :
					debug(3,"pattern = '%s' is a target" % (pattern))

	def directive(self,text) :
		debug(1,"directive(text='%s')"%(text))
		items = re.sub("[ \t]+"," ",text).split(" ")
		if not items :
			raise Exception("directive(text='%s'): missing directive" % (text))
		if items[0] not in self.directives :
			raise Exception("directive(text='%s'): directive '%s' is invalid" % (text,items[0]))
		if not self.directives[items[0]] :
			self.directives[items[0]] = (" ").join(items[1:])
		else :
			raise Exception("directive(text='%s'): directive '%s' occurred a second time" % (text,items[0]))

	def target(self,target,pattern) :
		debug(1,"terminal(target='%s',pattern='%s')" % (target,pattern))
		patterns = re.sub("[ \t]+"," ",pattern).split(" ")
		self.targets[target][pattern] = patterns

	def terminal(self,target,pattern,terminal) :
		debug(1,"handler(target='%s',pattern='%s',terminal='%s'"%(target,pattern,terminal))
		target = self.targets[target][pattern].append(terminal)

	def __str__(self) :
		return ("%s : {\n\tdirectives : %s,\n\ttargets : %s\n\t}\n" % (repr(self),self.directives,self.targets))

	def write_h(self) :
		with open(self.hfile,"w") as f :
			f.write("// automatically generated from {0}\n".format(self.yfile))
			f.write("class {0} : public {1} \n".format(self.directives["CLASS"],self.directives["BASE"]))
			f.write("{\n")
			f.write("\ttypedef int PARSERSTATUS;\n")
			f.write("private:\n")
			f.write("public:\n")
			f.write("\t{0}(const char *file);\n".format(self.directives["CLASS"]))
			f.write("\t~{0}(void);\n".format(self.directives["CLASS"]))
			for target in self.targets :
				f.write("\tPARSERSTATUS {0}(PARSER);\n".format(target))
			f.write("};\n")

	def write_cpp(self) :
		with open(self.cppfile,"w") as f :
			f.write("// automatically generated from %{0}\n".format(self.yfile))
			f.write("#include \"{0}.h\"\n".format(self.directives["CLASS"]))
			f.write("{0}::{0}(const char *file)\n".format(self.directives["CLASS"]))
			f.write("\t: {0}(file)\n".format(self.directives["BASE"]))
			f.write("{\n")
			f.write("}\n")
			f.write("{0}::~{0}(void)\n".format(self.directives["CLASS"]))
			f.write("{\n")
			f.write("}\n")
			for target in self.targets :
				self.write_target(f,target)

	def write_target(self,f,target) :
		debug(1,"write_target(f,target='%s')" % target)
		f.write("{0}::PARSERSTATUS {0}::{1}(PARSER)\n".format(self.directives["CLASS"],target))
		f.write("{\n")
		debug(2,"terminals = %s" % self.targets[target].values())
		for terminal in self.targets[target].values():
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
	if ( len(sys.argv) > 1 ) :
		name = sys.argv[1]
	else :
		name = "parser.y"
	parser = GlmParser(name)
	parser.write_h()
	parser.write_cpp()

