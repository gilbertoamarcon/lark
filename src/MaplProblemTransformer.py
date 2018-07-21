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

	type			= id
	agent			= id
	object			= id
	capability_name	= id
	action			= id
	var				= id
	deadline		= number

	def problem(self, problem):
		return OrderedDict([
			('agents',			problem[0]),
			('objects',			problem[1]),
			('agentcaps',		problem[2]),
			('worldstate',		problem[3]),
			('initialstate',	problem[4]),
			('goal',			problem[5]),
		])

	def agents(self, items):
		return OrderedDict([i for l in items for i in l])

	def agent_type(self, items):
		return [(i,items[0]) for i in items[1:]]

	def objects(self, items):
		return OrderedDict([i for l in items for i in l])

	def object_type(self, items):
		return [(i,items[0]) for i in items[1:]]

	# ===================================
	# Capabilities
	# ===================================

	def capability_dict(self, items):
		return OrderedDict(items)

	def capability(self, items):
		return tuple(items)

	# ===================================
	# Agent Capabilities
	# ===================================

	def agent_capabilities(self, items):
		return OrderedDict([i for l in items for i in l])

	def agentcap(self, items):
		agent_list		= items[0]
		capability_dict	= items[1]
		return [(agent,deepcopy(capability_dict)) for agent in agent_list]

	agent_list = list



	def group(self, items, keyword):

		# Initializing a dictionary of lists for each relation type
		ret_val = OrderedDict()
		for relat_type,relat in self.domain[keyword].items():
			ret_val[relat_type] = OrderedDict([(k,[]) for k in relat.keys()])

		# Appending entries
		for i in items:
			ret_val[i['type']][i['name']].append(i['entry'])

		return ret_val

	def worldstate(self, items):
		return self.group(items, 'worlddef')

	def initialstate(self, items):
		return self.group(items, 'statedef')

	def goalstate(self, items):
		return self.group(items, 'statedef')


	def declare(self, items):
		return {
			'type':				items[0].data.encode('ascii','ignore'),
			'name':				items[0].children[0],
			'entry':			items[1:],
		}

	def assign(self, items):
		return {
			'type':				items[0].data.encode('ascii','ignore'),
			'name':				items[0].children[0],
			'entry':{
				'arguments':	items[1:-1],
				'value':		items[-1],
			},
		}

	predicates		= declare
	numerics		= assign
	functions		= assign
	func_subgoal	= assign


