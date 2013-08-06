#! coding: utf-8
"""
Script to process and display the time I spend on the computer.

"""
import sys
import pylab
from matplotlib import dates
from datetime import datetime
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

def str2datetime(alist):
	new = [datetime.strptime(string, "%y/%m/%d %H:%M:%S") for string in alist]
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
			# print i, "\t", row,
			line = row.strip("\n").split("\t\t")
			lines.append(line)

	# the idea would be to seperate time into chunks
	# of customisable length

	activity, date, time = zip(*lines)

	datetime_strings = [ d+" "+t for d, t in zip(date, time) ]

	return str2datetime(datetime_strings), word2bool(activity)


def makeGraph(data):
	"""
	Make a graph of Time vs. Activity

		 On
	eg.    ___|‾‾|_|‾|___|‾‾‾‾‾‾|___|‾|_
		Off								 Time ->

	It appears that this plot type is called a step plot.
	"""
	x, y = data
	# for the triangular filling
	y1 = y
	y2 = [0]*len(y)
	
	fig = pylab.figure()
	ax = fig.add_subplot(111)

	# steps-post means the step goes up when Wake
	# 					and it goes down when Sleep
	pylab.plot_date(x, y, fmt="", xdate=True, ydate=False,
					drawstyle="steps-post")
	
	pylab.ylim([-2,3])
	pylab.fill_between(x, y1, y2, alpha=0.1, edgecolor="w")
	pylab.title('Time I spend on the computer')
	pylab.xlabel('Time')
	pylab.ylabel('Activity')

	ax.xaxis.set_minor_locator(dates.HourLocator())
	ax.xaxis.set_major_locator(dates.DayLocator())
	xlabels = ax.xaxis.set_major_formatter(dates.DateFormatter("%a %m/%d"))
	ax.xaxis.grid(True, which="major")
	pylab.subplots_adjust(bottom=0.1)

	for label in ax.get_xticklabels():
		label.set_horizontalalignment('left')
	# pylab.show()
	pylab.savefig("plot1.png", bbox_inches=0)

	return


def main():
	data = parseTime(FILE)
	makeGraph(data)
	return

if __name__ == "__main__":

	sys.exit(main())


