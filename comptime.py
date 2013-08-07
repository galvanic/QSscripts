#! coding: utf-8
"""
Script to process and display the time I spend on the computer.

"""
import sys
import pylab
import matplotlib.dates as mdates
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

def str2datetime(alist):
	new = [ datetime.datetime.strptime(string, "%y/%m/%d %H:%M:%S") for string in alist ]
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


def makePlot(data):
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
	
	fig = pylab.figure(figsize=(12,1.5))
	ax = fig.add_subplot(111)

	# steps-post means the step goes up when Wake
	# 					and it goes down when Sleep
	pylab.plot_date(x, y, fmt="", xdate=True, ydate=False,
					drawstyle="steps-post")
	
	pylab.ylim([-0.5, 1.5])
	pylab.fill_between(x, y1, y2, alpha=0.1, edgecolor="w")
	pylab.title('Time I spend on the computer')
	pylab.xlabel('Time')
	pylab.ylabel('Activity')

	ax.xaxis.set_minor_locator(mdates.HourLocator())
	ax.xaxis.set_major_locator(mdates.DayLocator())
	xlabels = ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %m/%d"))
	ax.xaxis.grid(True, which="major")
	pylab.subplots_adjust(bottom=0.15)

	for label in ax.get_xticklabels():
		label.set_horizontalalignment('left')
	ax.set_yticks([])
	# pylab.show()
	pylab.savefig("stepplot.png", bbox_inches=0)

	return


def makeBarPlot(data):
	import numpy as np
	import matplotlib.pyplot as plt
	import datetime

	times, activity = data

	first_day = times[0].date()
	last_day  = times[-1].date()

	# dates for xaxis
	event_date = mdates.num2date( mdates.drange(first_day, last_day, datetime.timedelta(days=1)) )
	
	# base date for yaxis can be anything, since information is in the time
	anydate = datetime.date(2001,1,1)

	# event times
	event_start = [datetime.time(20, 12), datetime.time(12, 15), datetime.time(8, 1,)]
	event_finish = [datetime.time(23, 56), datetime.time(16, 5), datetime.time(18, 34)]

	# translate times and dates lists into matplotlib date format numpy arrays
	start = np.fromiter((mdates.date2num(datetime.datetime.combine(anydate, event)) for event in event_start), dtype = 'float', count = len(event_start))
	finish = np.fromiter((mdates.date2num(datetime.datetime.combine(anydate, event)) for event in event_finish), dtype = 'float', count = len(event_finish))
	date = mdates.date2num(event_date)

	# calculate events durations
	duration = finish - start

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	# use errorbar to represent event duration
	ax.errorbar(date, start, [np.zeros(len(duration)), duration], linestyle = '')
	# make matplotlib treat both axis as times
	ax.xaxis_date()
	ax.yaxis_date()

	plt.xticks(rotation='vertical')
	plt.subplots_adjust(bottom=0.3)

	plt.savefig("plot2.png", bbox_inches=0)
	return

def makeSleepPlot(data):
	"""
	Taking seconds off since it isn't useful here,
	but could be interesting to look at to see times when I wasn't super attentive.
	"""
	from matplotlib.ticker import FuncFormatter as ff

	times, activity = data

	# take seconds off
	# times = [ dt.replace(second=0) for dt in times ]

	comptimes = zip(times, activity)

	# if the first activity is sleep, discard it
	if not comptimes[0][1]:
		comptimes.pop(0)

	# x axis
	first_day = times[0].date()
	last_day  = times[-1].date()
	days = mdates.num2date( mdates.drange(first_day, last_day, datetime.timedelta(days=1)) )

	# seperate the starting times from the finishing times
	def getStartEnd(alist):
		start_times = list()
		end_times 	= list()
		for el in alist:
			activity = el[1]
			if activity:
				start_times.append(el)
			else:
				end_times.append(el)
		return map(list, [zip(*start_times)[0], zip(*end_times)[0]])

	start_times, end_times = getStartEnd(comptimes)
	# end_times will always be one short since the computer is ON to process this data
	# so we add the most recent time to endtime so that the latest bar appears
	end_times.append(datetime.datetime.now().replace(microsecond=0))
	assert len(start_times) == len(end_times)

	def getElapsedTime(start, end):
		times = zip(start, end)
		intervals  = [ sleep - wake for wake, sleep in times ]
		return intervals

	# for Y-axis, turn from time to numbers
	def dt2m(dt):
		return (dt.hour*60) + dt.minute

	# Then format the Y axis as Hour:Minute using a custom formatter
	def m2hm(x, i):
		h = int(x/60)
		m = int(x%60)
		return '%(h)02d:%(m)02d' % {'h':h,'m':m}

	# bottom point of the bars
	starttimes_mins = [ dt2m(dt) for dt in start_times ]

	# heights of the bars
	intervals = getElapsedTime(start_times, end_times)
	interval_mins = [ i.seconds/60 for i in intervals ]

	# stats
	total_time = sum(intervals, datetime.timedelta())

	fig = pylab.figure(figsize=(6, 9)) #figsize in inches
	ax = fig.add_subplot(1, 1, 1)
	ax.bar(start_times, interval_mins, bottom=starttimes_mins, edgecolor='none')

	# matplotlib date format object
	hfmt = mdates.DateFormatter('%b %d')
	ax.xaxis.set_major_formatter(hfmt)
	ax.xaxis.set_major_locator(pylab.MultipleLocator(1.0)) #a tick mark a day
	for label in ax.get_xticklabels():
		label.set_horizontalalignment('left')
	ax.set_xlim([first_day, last_day + datetime.timedelta(days=1)])
	ax.xaxis.grid(True, which="major")

	ax.yaxis.grid(True, which="major")
	ax.set_ylim([0, 24*60])
	ax.yaxis.set_major_formatter(ff(m2hm))
	ax.yaxis.set_major_locator(pylab.MultipleLocator(60)) #a tick mark an hour

	pylab.savefig("barplot.png")
	return

def main():
	data = parseTime(FILE)
	makePlot(data)
	makeSleepPlot(data)
	return

if __name__ == "__main__":

	sys.exit(main())


