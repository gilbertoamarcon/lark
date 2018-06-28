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
		pass

	def number(self, (s,)):
		return float(s)

	def id(self, (s,)):
		return s.encode('ascii','ignore')

	# Token ids and numbers
	type			= id
	object			= id
	action			= id
	var				= id
	when			= id
	deadline		= number

	# Lists
	type_list_curl	= list
	type_list_squa	= list
	var_list		= list
	type_var_list	= list

	actiondefs		= list
	effectsdef		= list
	conditionsdef	= list

	# Get first and only list element
	def list_strip(self, (items,)):
		return items
	types			= list_strip
	actiondur		= list_strip
	cost			= list_strip

	# Type and variable name for each entry
	def type_var_list(self, items):
		return OrderedDict([(name,type) for name,type in zip(items[1::2],items[0::2])])

	def domain(self, domain):
		return OrderedDict([
			('types',			domain[0]),
			('worlddef',		domain[1]),
			('statedef',		domain[2]),
			('actiondef',		domain[3]),
		])

	def relation_bundle(self, items):
		ret_val = OrderedDict()
		for i in items:
			if i['type'] not in ret_val:
				ret_val[i['type']] = OrderedDict()
			ret_val[i['type']][i['name']] = i['entry']
		return ret_val

	worlddef = relation_bundle
	statedef = relation_bundle

	def actiondef(self, items):
		return {
					'name':				items[0],
					'entry':			items[1],
					'actiondur':		items[2],
					'cost':				items[3],
					'conditionsdef':	items[4],
					'effectsdef':		items[5],
				}

	def declare(self, items):
		return {
			'type':				items[0].data.encode('ascii','ignore'),
			'name':				items[0].children[0],
			'entry':			items[1],
		}

	def assign(self, items):
		return {
			'type':				items[1].data.encode('ascii','ignore'),
			'name':				items[1].children[0],
			'entry':{
				'arguments':	items[2:][0],
				'return':		items[0],
			},
		}

	predicatedef	= declare
	numericdef		= declare
	functiondef		= assign

	# Temporal conditions
	def conditions(self, items):
		return {
			'when':		items[0],
			'entry':	items[1],
			'type':		items[1]['type'],
		}

	def effect(self, items):
		return {
			'when':		items[0],
			'entry':	items[1],
		}




	# ========================================================
	# Action Conditions
	# ========================================================

	def pred_cond(self, items):
		return {
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
		}

	def func_cond(self, items):
		value = items[2] if (len(items)==3) else None
		return {
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		value,
		}

	def num_cond(self, items):
		return {
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		items[2],
		}

	def varsdiff(self, items):
		return {
			'type':			'varsdiff',
			'arguments':	items,
		}





	# ========================================================
	# Action Effects
	# ========================================================

	def func_assign(self, items):
		value = items[2] if (len(items)==3) else None
		return {
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		value,
		}

	def pred_eff(self, items):
		return {
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
		}

	def numeric_eff_assign(self, items):
		value = items[2] if (len(items)==3) else None
		return {
			'effect':		'assign',
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		value,
		}

	def numeric_eff_increase(self, items):
		value = items[2] if (len(items)==3) else None
		return {
			'effect':		'increase',
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		value,
		}

	def numeric_eff_decrease(self, items):
		value = items[2] if (len(items)==3) else None
		return {
			'effect':		'decrease',
			'type':			items[0].data.encode('ascii','ignore'),
			'name':			items[0].children[0],
			'arguments':	items[1],
			'value':		value,
		}








	# ========================================================
	# Probability Distributions
	# ========================================================

	def distribution_constant(self, (items,)):
		return {
			'type':		'constant',
			'value':	items,
		}

	def distribution_uniform(self, items):
		return {
			'type':		'uniform',
			'min':		items[0],
			'max':		items[1],
		}

	def distribution_normal(self, items):
		return {
			'type':		'normal',
			'mu':		items[0],
			'sigma':	items[1],
		}

	def distribution_exponential(self, (items,)):
		return {
			'type':		'exponential',
			'value':	items,
		}




	# ========================================================
	# Math
	# ========================================================

	def exp_numeric(self, items):
		return {
			'numeric':	items[0].children[0],
			'vars':		items[1:][0],
		}

	def mul(self, items):
		return ['*',items]

	def div(self, items):
		return ['/',items]

	def add(self, items):
		return ['+',items]

	def sub(self, items):
		return ['-',items]






if __name__ == '__main__':
	main(transformer)