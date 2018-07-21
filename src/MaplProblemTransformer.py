#!/usr/bin/env python

from collections import OrderedDict
from lark import Lark
from lark import Transformer
from copy import deepcopy

class MaplProblemTransformer(Transformer):

	def __init__(self,domain):
		self.domain = domain

	def number(self, (s,)):
		return float(s)

	def id(self, (s,)):
		return s.encode('ascii','ignore')

	def type_list(self, items):
		type	= items[0]
		list	= items[1]
		return [(i,type) for i in list]

	def type_dict(self, items):
		return OrderedDict([i for l in items for i in l])

	type				= id
	agent				= id
	object				= id
	capability_name		= id
	predicate_name		= id
	task_name			= id
	numeric				= id
	function			= id
	action				= id
	var					= id
	deadline			= number

	agent_list			= list
	object_list			= list
	task_list			= list

	agent_capabilities	= type_dict
	task_capabilities	= type_dict

	agents				= type_dict
	objects				= type_dict
	agent_type			= type_list
	object_type			= type_list

	def problem(self, problem):
		return OrderedDict([
			('agents',					problem[0]),
			('objects',					problem[1]),
			('agentcapabilities',		problem[2]),
			('worldstate',				problem[3]),
			('initialstate',			problem[4]),
			('goal',					problem[5]),
			('taskcapabilities',		problem[6]),
		])

	# ===================================
	# Capabilities
	# ===================================

	def capability_dict(self, items):
		return OrderedDict(items)

	def capability(self, items):
		return tuple(items)

	def capabilities(self, items):
		list			= items[0]
		capability_dict	= items[1]
		return [(l,deepcopy(capability_dict)) for l in list]

	agentcap			= capabilities
	taskcap				= capabilities




	def worldstate(self, items):
		return self.group(items, 'worlddef')

	def initialstate(self, items):
		return self.group(items, 'statedef')

	def task_dict(self, items):
		return OrderedDict(items)

	def task(self, items):
		return (items[0],self.group(items[1:], 'statedef'))

	def group(self, items, keyword):

		# Initializing a dictionary of lists for each relation type
		ret_val = OrderedDict()
		for relat_type,relat in self.domain[keyword].items():
			ret_val[relat_type] = OrderedDict([(k,[]) for k in relat.keys()])

		# Appending entries
		for i in items:
			ret_val[i['type']][i['name']].append(i['entry'])

		return ret_val

	def relations(self, (items,)):
		return items

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


