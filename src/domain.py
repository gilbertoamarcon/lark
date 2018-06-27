#!/usr/bin/env python

from collections import OrderedDict
from lark import Lark
from lark import Transformer
import argparse
import oyaml as yaml

def main(transformer):

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
	parser = Lark(grammar).parse

	# Reading the input file
	with open(args.input_filename,'rb') as f:
		inp = f.read()

	# Parsing the input file
	tree = parser(inp)

	domain = transformer().transform(tree)

	# Storing the result in the output file
	with open(args.output_filename,'w') as f:
		f.write(yaml.dump(domain))

class transformer(Transformer):

	def __init__(self):
		self.domain_dict = {}

	def number(self, (s,)):
		return float(s)

	def id(self, (s,)):
		return s.encode('ascii','ignore')

	type			= id
	object			= id
	predicate		= id
	numeric			= id
	function		= id
	deadline		= number

	type_list		= list

	def domain(self, domain):
		self.domain_dict = OrderedDict([
			('types',			domain[0]),
			('worlddef',		domain[1]),
			('statedef',		domain[2]),
			# ('actiondef',		domain[3]),
		])
		return self.domain_dict

	def types(self, (items,)):
		return items

	def relation_bundle(self, items):
		ret_val = OrderedDict()
		for i in items:
			if i['type'] not in ret_val:
				ret_val[i['type']] = OrderedDict()
			ret_val[i['type']][i['name']] = i['entry']
		return ret_val

	worlddef = relation_bundle
	statedef = relation_bundle

	def predicatedef(self, items):
		return {
					'type': 'predicates',
					'name': items[0],
					'entry': items[1],
				}

	def numericdef(self, items):
		return {
					'type': 'numerics',
					'name': items[0],
					'entry': items[1],
				}

	def functiondef(self, items):
		return {
					'type': 'functions',
					'name': items[1],
					'entry': {
						'return': items[0],
						'arguments': items[2],
					},
				}



if __name__ == '__main__':
	main(transformer)