#! coding: utf-8
"""
Script to process and display the time I spend on the computer.

"""
import sys
import pylab
import datetime
from code import interact
# interact(local=locals())


FILE = "/Users/jc5809/Dropbox/Programming/Projects/QS_scripts/comptimelog.txt"

ON  = ["Startup", "Start", "Wake"]
OFF = ["Sleep", "Shutdown", "Restart"]

def word2bool(alist):
	new = list()
	for el in alist:
		if el in ON:
			new.append(True)
		elif el in OFF:
			new.append(False)
	return new

def div(el):
	return map(int, [ el[:2], el[3:5], el[6:] ])

def string2datetime(alist):
	new = list()
	for date, time in alist:
		year, month, day  = div(date)
		hour, minute, sec = div(time)
		dt = datetime.datetime(2000+year, month, day, hour, minute, sec)
		new.append(dt)
	return new

def parseTime(filename):
	"""
	filename:	file with time data in lines

	Returns a tuple of lists of data, in this case, a list of
	datetime instances and a list of booleens representing computer
	state being entered at that time (asleep or awake).
	"""
	lines = list()

	with open(filename) as f:
		for i, row in enumerate(f):
			# if i > 100:
			# 	break
			print i, "\t", row,
			line = row.strip("\n").split("\t\t")
			lines.append(line)

	# the idea would be to seperate time into chunks
	# of customisable length

	activity, date, time = zip(*lines)

	datetimes = zip(date, time)

	return string2datetime(datetimes), word2bool(activity)


def makeGraph(data):
	"""
	Make a graph of Time vs. Activity

		 On
	eg.    ___|‾‾|_|‾|___|‾‾‾‾‾‾|___|‾|_
		Off								 Time ->

	It appears this plot is called a step plot.
	"""
	x, y = data
	# x = range(len(y))
	y1 = y
	y2 = [0]*len(y)
	# steps-post means the step goes up when Wake
	# 					and it goes down when Sleep
	pylab.plot_date(x, y, fmt="", xdate=True, ydate=False,
					linewidth=2, drawstyle="steps-post")
	
	pylab.ylim([-2,3])
	# pylab.xlim([-1,7])
	pylab.fill_between(x, y1, y2, alpha=0.1, edgecolor="w")
	pylab.title('Time I spend on the computer')
	pylab.xlabel('Time')
	pylab.ylabel('Activity')
	pylab.show()

	return


def main():
	# y = [ int(char) for char in "0110100" ]
	data = parseTime(FILE)
	makeGraph(data)
	return

if __name__ == "__main__":

	sys.exit(main())
























