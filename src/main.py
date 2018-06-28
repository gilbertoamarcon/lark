#!/usr/bin/env python

from collections import OrderedDict
from lark import Lark
from lark import Transformer
from DomainTransformer import DomainTransformer
from ProblemTransformer import ProblemTransformer
import argparse
import oyaml as yaml

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
	parser.add_argument(
			'-y','--yaml_domain_file',
			nargs='?',
			type=str,
			default=None,
			help='YAML domain file.'
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

	# If domain database has not been provided
	if args.yaml_domain_file is None:

		# Parsing domain
		database = DomainTransformer().transform(tree)

	else:

		# Loading domain
		with open(args.yaml_domain_file,'r') as f:
			domain = yaml.load(f.read())

		# Parsing problem
		database = ProblemTransformer(domain).transform(tree)

	# Storing the result in the output file
	with open(args.output_filename,'w') as f:
		f.write(yaml.dump(database))


if __name__ == '__main__':
	main()