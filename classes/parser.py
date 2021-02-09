# MODULES
from shared.settings import colour

# CLASS
class Parser():
	def __init__(self, kws, args, callbacks):
		self.forms = {}
		for i, kw in enumerate(kws):
			self.forms[kw] = args[i]
		self.kws = kws
		self.callbacks = callbacks
		self.guide = ""
		for j, kw in enumerate(kws):
			x = "\n" if i else ""
			self.guide = self.guide + f"{x}\t<{colour.BOLD}" + kw + f"{colour.END}{colour.RED}>\thas args <{colour.BOLD}"
			if self.forms[kw]:
				for i, arg in enumerate(self.forms[kw]):
					if i < len(self.forms[kw])-1:
						self.guide = self.guide + f"{arg}, "
					else:
						self.guide = self.guide + f"and {arg}{colour.END}{colour.RED}>"
			else:
				self.guide = self.guide + f"None{colour.END}{colour.RED}>"

	def parse(self, inp):
		commands = [text.strip() for text in inp.split("and")]
		results = []
		for text in commands:
			results.extend(self.parse_sub(text))
		errs = []
		succs = ""
		for i,result in enumerate(results):
			if result == False:
				errs.append(i+1)
			else:
				succs = succs + str(result) + "\n"
		return succs, errs

	def parse_sub(self, text):
		split = text.split(" ", 2)
		try:
			kw = split[0]
			if kw in self.kws:
				if self.forms[kw]:
					args = split[1]
					subargs = args.split(",")
					returnee = []
					for arg in subargs:
						returnee.append(self.check_arg(kw, arg))
					return returnee
				else:
					self.callbacks[kw]()
					return []
			return [False]
		except Exception:
			return [False]
	
	def check_arg(self, kw, arg):
		if arg in self.forms[kw]:
			return self.callbacks[kw][arg]()
		return False

	def err(self, positions):
		plist = ""
		if positions:
			plist = str(positions[0])
			for i, position in enumerate(positions):
				if i:
					plist = plist + ", " + str(position)
		else:
			plist = "Unknown"
		print(f"{colour.RED}>> Malformed Command <{colour.BOLD}keyword{colour.END}{colour.RED} {colour.BOLD}arg{colour.END}{colour.RED}> at position(s) <{colour.RED}{colour.BOLD}{plist}{colour.END}{colour.RED}>. Here are all Keywords & Args:{self.guide} {colour.END}")