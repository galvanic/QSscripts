
"""
Script to process and display the time I spend on the computer.

"""
import sys

FILE = "/Users/jc5809/Dropbox/Programming/Projects/QS_scripts/comptimelog.txt"

def parseTime(filename):
	"""
	filename:	file with time data in lines

	Returns *research how to make graphs again so that I know
	what to return
	"""
	with open(filename) as f:
		for i, line in enumerate(f):
			print i, "\t", line,
	data = []
	return data


def makeGraph(data):
	
	return


def main():
	parseTime(FILE)
	return

if __name__ == "__main__":

	sys.exit(main())