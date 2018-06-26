#!/usr/bin/env python

from lark import Lark
from lark import Transformer
import argparse
import yaml

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

	print 'Tree:'
	print tree.pretty()

	problem = transformer().transform(tree)

	print 'Problem:'
	print problem

	# Storing the result in the output file
	with open(args.output_filename,'w') as f:
		f.write(yaml.dump(problem))

class transformer(Transformer):

	def __init__(self):
		self.problem_dict = {}


	def problem(self, problem):
		self.problem_dict = {
			'objects':		problem[0],
			'worldstate':	problem[1],
			'initialstate':	problem[2],
			'goal':			problem[3],
		}
		return self.problem_dict

	def number(self, (s,)):
		return float(s)

	def id(self, (s,)):
		return s.encode('ascii','ignore')

	def type(self, val):
		return ['type',val[0]]

	def object(self, val):
		return ['object',val[0]]

	def predicate(self, val):
		return ['predicate',val[0]]

	def numeric(self, val):
		return ['numeric',val[0]]

	def function(self, val):
		return ['function',val[0]]

	def objects(self, items):
		objs = {}
		current_type = ''
		for i in items:
			if i[0] == 'type':
				current_type = i[1]
			if i[0] == 'object':
				objs[i[1]] = current_type
		return objs

	def worldstate(self, items):
		ret_val = {}
		ret_val['predicates'] = {}
		ret_val['numerics'] = {}
		ret_val['functions'] = {}
		for i in items:

			if i['type'] == 'predicates':
				if not i['name'] in ret_val['predicates']:
					ret_val['predicates'][i['name']] = []
				ret_val['predicates'][i['name']].append(i['arguments'])

			if i['type'] == 'numerics':
				if not i['name'] in ret_val['numerics']:
					ret_val['numerics'][i['name']] = []
				ret_val['numerics'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'],
					})
			if i['type'] == 'functions':
				if not i['name'] in ret_val['functions']:
					ret_val['functions'][i['name']] = []
				ret_val['functions'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'],
					})
		return ret_val

	def initialstate(self, items):
		ret_val = {}
		ret_val['predicates'] = {}
		ret_val['numerics'] = {}
		ret_val['functions'] = {}
		for i in items:

			if i['type'] == 'predicates':
				if not i['name'] in ret_val['predicates']:
					ret_val['predicates'][i['name']] = []
				ret_val['predicates'][i['name']].append(i['arguments'])

			if i['type'] == 'numerics':
				if not i['name'] in ret_val['numerics']:
					ret_val['numerics'][i['name']] = []
				ret_val['numerics'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'],
					})
			if i['type'] == 'functions':
				if not i['name'] in ret_val['functions']:
					ret_val['functions'][i['name']] = []
				ret_val['functions'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'][1],
					})
		return ret_val

	def goal(self, items):
		ret_val = {}
		ret_val['predicates'] = {}
		ret_val['numerics'] = {}
		ret_val['functions'] = {}
		for i in items:

			if i['type'] == 'predicates':
				if not i['name'] in ret_val['predicates']:
					ret_val['predicates'][i['name']] = []
				ret_val['predicates'][i['name']].append(i['arguments'])

			if i['type'] == 'numerics':
				if not i['name'] in ret_val['numerics']:
					ret_val['numerics'][i['name']] = []
				ret_val['numerics'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'],
					})
			if i['type'] == 'functions':
				if not i['name'] in ret_val['functions']:
					ret_val['functions'][i['name']] = []
				ret_val['functions'][i['name']].append({
						'arguments': i['arguments'],
						'value': i['value'][1],
					})
		return ret_val

	def predicates(self, items):
		return {
			'type':			'predicates',
			'name':			items[0][1],
			'arguments':	[i[1] for i in items[1:]],
		}

	def numerics(self, items):
		return {
			'type':			'numerics',
			'name':			items[0][1],
			'arguments':	[i[1] for i in items[1:-1]],
			'value':		items[-1],
		}

	def functions(self, items):
		return {
			'type':			'functions',
			'name':			items[0][1],
			'arguments':	[i[1] for i in items[1:-1]],
			'value':		items[-1],
		}

if __name__ == '__main__':
	main(transformer)