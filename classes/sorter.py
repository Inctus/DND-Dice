# CLASS
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