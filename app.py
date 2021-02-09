# IMPORTS
from sys import exit
import os
from platform import system as os_name
from random import seed

from classes.die import Die
from classes.parser import Parser
from classes.sorter import Sorter
from shared.settings import colour,dice

# OPTIONAL DEPENDENCY
art_flag = False
try:
	from art import tprint
except:
	art_flag = True

# GLOBALS 
os_name = os_name()

# FUNCTIONS 
def clear():
	if os_name == "Darwin" or os_name == "Linux":
		os.system("clear")
	elif os_name == "Windows":
		os.system("cls")

def mainloop(parser):
	while True:
		inp = input(">> ").lower()
		succs, errs = parser.parse(inp)
		if len(succs) > 0:
			try:
				tprint(succs, font="block")
			except:
				print(succs)
		if len(errs):
			parser.err(errs)

def run():
	if art_flag:
		print(f"{colour.YELLOW}>> Package <{colour.BOLD}art{colour.END}{colour.YELLOW}> has not been installed. Consider running <{colour.BOLD}pip3 install art{colour.END}{colour.YELLOW}> for a cleaner output{colour.END}")
	print(f">> DND Dice written by <{colour.BOLD}Inctus/Haashim{colour.END}>")
	seed()
	sorter = Sorter()
	for die in dice:
		sorter.append(Die(die), str(die))
	parser = Parser(["roll", "clear", "quit"], [[str(die) for die in dice], [], []], {"roll":sorter.extract_callbacks(),"clear":clear, "quit":exit})
	mainloop(parser)

run()