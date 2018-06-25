#!/usr/bin/env python

from lark import Lark
from lark import InlineTransformer
import argparse


class parserulateTree(InlineTransformer):
	from operator import add, sub, mul, truediv as div, neg
	number = float

	def __init__(self):
		self.vars = {}

		def assign_var(self, name, value):
			self.vars[name] = value
			return value

			def var(self, name):
				return self.vars[name]

def main():

	# Parsing user input
	parser = argparse.ArgumentParser()
	parser.add_argument(
			'-g','--grammar_filename',
			nargs='?',
			type=str,
			required=True,
			help='Grammar specification file.'
		)
	parser.add_argument(
			'-i','--input_filename',
			nargs='?',
			type=str,
			required=True,
			help='Input file to parse.'
		)
	parser.add_argument(
			'-o','--output_filename',
			nargs='?',
			type=str,
			required=True,
			help='Output file.'
		)
	args = parser.parse_args()

	# Reading the grammar
	with open(args.grammar_filename,'r') as f:
		grammar = f.read()

	# Setting up the parser
	parser = Lark(grammar, parser='lalr', transformer=parserulateTree()).parse

	# Reading the input file
	with open(args.input_filename,'rb') as f:
		inp = f.read()

	# Parsing the input file
	out = parser(inp)

	# Storing the result in the output file
	with open(args.output_filename,'w') as f:
		f.write(str(out))

if __name__ == '__main__':
	main()