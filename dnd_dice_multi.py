# IMPORTS
from random import seed,randint
from sys import exit
import os
from platform import system as os_name

# OPTIONAL DEPENDENCY
art_flag = False
try:
	from art import tprint
except:
	art_flag = True

# SETTINGS
dice = [4, 6, 8, 10, 12, 20]
class colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# GLOBALS 
os_name = os_name()

# CLASSES
class Die():
	def __init__(self, sides=6):
		self.sides = sides

	def roll(self):
		return randint(1, self.sides)

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
			self.guide = self.guide + f"{x}\t<{colour.BOLD}" + kw + f"{colour.END}{colour.RED}> has args <{colour.BOLD}"
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
		print(f"{colour.RED}>> Malformed Command <{colour.BOLD}keyword{colour.END}{colour.RED} {colour.BOLD}arg{colour.END}{colour.RED}> at Positions <{colour.RED}{colour.BOLD}{plist}{colour.END}{colour.RED}>. Here are all Keywords & Args:\n{self.guide} {colour.END}")

class Sorter():
	def __init__(self):
		self.dice = {}

	def append(self, die, name):
		self.dice[name] = die

	def extract_callbacks(self):
		callbacks = {}
		for name, die in self.dice.items():
			callbacks[name] = die.roll
		return callbacks

# FUNCTIONS 
def clear():
	if os_name == "Darwin" or os_name == "Linux":
		os.system("clear")
	elif os_name == "Windows":
		os.system("cls")

def mainloop(parser):
	while True:
		inp = input(">> ")
		succs, errs = parser.parse(inp)
		if len(succs) > 0:
			try:
				tprint(succs, font="block")
			except:
				print(succs)
		if len(errs):
			parser.err(errs)

def configure():
	if art_flag:
		print(f"{colour.YELLOW}>> Package <{colour.BOLD}art{colour.END}{colour.YELLOW}> has not been installed. Consider running <{colour.BOLD}pip3 install art{colour.END}{colour.YELLOW}> for a cleaner output{colour.END}")
	print(f">> DND Dice written by <{colour.BOLD}Inctus/Haashim{colour.END}>")
	seed()
	sorter = Sorter()
	for die in dice:
		sorter.append(Die(die), str(die))
	parser = Parser(["roll", "clear", "quit"], [[str(die) for die in dice], [], []], {"roll":sorter.extract_callbacks(),"clear":clear, "quit":exit})
	mainloop(parser)

configure()
