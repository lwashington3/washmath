from argparse import ArgumentParser
from os import getenv
from sys import argv


def _add_common_options(parser):
	pass


def _create_euler_parser(parser_factory):
	parser = parser_factory("euler", help="Solve a euler function")
	_add_common_options(parser)
	parser.add_argument("-g", "--step_size", help="The step size. (h is used for help)")
	parser.add_argument("-n", "--steps", help="The number of steps to go (inclusive).")
	parser.add_argument("-x", "--initial_x", help="The initial x-value.")
	parser.add_argument("-y", "--initial_y", help="The initial y-value.")
	parser.add_argument("-f", "--function", help="The python equivalent of a lambda function for the differential equation.")
	return parser


def create_argument_parser():
	parser = ArgumentParser(prog="Washington Math Helper")
	subparsers = parser.add_subparsers()
	subparsers.dest = 'command'
	subparsers.required = False
	_create_euler_parser(subparsers.add_parser)
	return parser


def main(args):
	parser = create_argument_parser()
	arguments = parser.parse_args(args)
	if arguments.command == "euler":
		from .calc import euler
		from tabulate import tabulate
		h = float(arguments.step_size)
		n = int(arguments.steps) + 1
		x0 = float(arguments.initial_x)
		y0 = float(arguments.initial_y)
		function = eval(arguments.function)
		answers = euler(h, n, x0, y0,  function, answer_only=False)
		print(tabulate(zip(*answers), headers=("x", "y"), tablefmt="fancy_grid"))


if __name__ == "__main__":
	main(argv[1:])
