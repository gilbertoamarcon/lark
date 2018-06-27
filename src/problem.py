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
			'-y','--yaml_domain_file',
			nargs='?',
			type=str,
			required=True,
			help='YAML domain file.'
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

	# Domain YAML
	with open(args.yaml_domain_file,'r') as f:
		domain = yaml.load(f.read())

	problem = transformer(domain).transform(tree)

	# Storing the result in the output file
	with open(args.output_filename,'w') as f:
		f.write(yaml.dump(problem))

class transformer(Transformer):

	def __init__(self,domain):
		self.domain = domain
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

	type		= id
	object		= id
	predicate	= id
	numeric		= id
	function	= id
	deadline	= number

	def objects(self, items):
		return dict([i for l in items for i in l])

	def object_type(self, items):
		return [(i,items[0]) for i in items[1:]]


	def group(self, items, keyword):
		ret_val = {relat:{} for relat in self.domain[keyword]}
		for type,relat in self.domain[keyword].items():
			ret_val[type] = {k:[] for k in relat.keys()}
		for i in items:
			ret_val[i['type']][i['name']].append({e:i[e] for e in ['arguments','value'] if e in i})


		return ret_val

	def worldstate(self, items):
		return self.group(items, 'worlddef')

	def initialstate(self, items):
		return self.group(items, 'statedef')

	def goal(self, items):
		return self.group(items, 'statedef')


	def predicates(self, items):
		return {
			'type':			'predicates',
			'name':			items[0],
			'arguments':	items[1:],
		}

	def numerics(self, items):
		return {
			'type':			'numerics',
			'name':			items[0],
			'arguments':	items[1:-1],
			'value':		items[-1],
		}

	def functions(self, items):
		return {
			'type':			'functions',
			'name':			items[0],
			'arguments':	items[1:-1],
			'value':		items[-1],
		}



if __name__ == '__main__':
	main(transformer)