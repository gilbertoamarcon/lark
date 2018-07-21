#!/usr/bin/env python

from collections import OrderedDict
from lark import Lark
from lark import Transformer

class AplProblemTransformer(Transformer):

	def __init__(self,domain):
		self.domain = domain

	def number(self, (s,)):
		return float(s)

	def id(self, (s,)):
		return s.encode('ascii','ignore')

	def object_type(self, items):
		type	= items[0]
		list	= items[1]
		return [(i,type) for i in list]

	def objects(self, items):
		return OrderedDict([i for l in items for i in l])

	type				= id
	object				= id
	predicate			= id
	numeric				= id
	function			= id
	action				= id
	var					= id
	deadline			= number
	object_list			= list

	def problem(self, problem):
		return OrderedDict([
			('objects',					problem[0]),
			('worldstate',				problem[1]),
			('initialstate',			problem[2]),
			('goal',					problem[3]),
		])

	def worldstate(self, items):
		return self.group(items, 'worlddef')

	def initialstate(self, items):
		return self.group(items, 'statedef')

	def goalstate(self, items):
		return self.group(items, 'statedef')

	def group(self, items, keyword):

		# Initializing a dictionary of lists for each relation type
		ret_val = OrderedDict()
		for relat_type,relat in self.domain[keyword].items():
			ret_val[relat_type] = OrderedDict([(k,[]) for k in relat.keys()])

		# Appending entries
		for i in items:
			ret_val[i['type']][i['name']].append(i['entry'])

		return ret_val

	def predicates(self, items):
		return {
			'type':				'predicate',
			'name':				items[0],
			'entry':			items[1],
		}

	def assign(self, items, type):
		return {
			'type':				type,
			'name':				items[0],
			'entry':{
				'arguments':	items[1],
				'value':		items[2],
			},
		}

	def numerics(self, items):
		if len(items) == 2:
			items = [items[0], [], items[1]]
		return self.assign(items, 'numeric')

	def functions(self, items):
		return self.assign(items, 'function')

	func_subgoal = functions


