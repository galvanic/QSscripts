#! coding: utf-8
"""
Script to process and display the time I spend on the computer.

"""
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter as ff
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
	The order of the lists is very important so that we know which
	time corresponds to which event.
	"""
	rows = list()

	with open(filename) as f:
		for i, row in enumerate(f):
			# if i > 100:
			# 	break
			# print i, "\t", row,
			line = row.strip("\n").split("\t\t")
			rows.append(line)

	event, date, time = zip(*rows)

	datetime_strings = [ d+" "+t for d, t in zip(date, time) ]

	return str2datetime(datetime_strings), word2bool(event)


def makeStepPlot(data):
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
	
	fig = plt.figure(figsize=(12,1.5))
	ax = fig.add_subplot(111)

	# steps-post means the step goes up when Wake
	# 					and it goes down when Sleep
	plt.plot_date(x, y, fmt="", xdate=True, ydate=False,
					drawstyle="steps-post")
	
	plt.ylim([-0.5, 1.5])
	plt.fill_between(x, y1, y2, alpha=0.1, edgecolor="w")
	plt.title('Time I spend on the computer')
	plt.xlabel('Time')
	plt.ylabel('Activity')

	ax.xaxis.set_minor_locator(mdates.HourLocator())
	ax.xaxis.set_major_locator(mdates.DayLocator())
	xlabels = ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %m/%d"))
	ax.xaxis.grid(True, which="major")
	plt.subplots_adjust(bottom=0.15)

	for label in ax.get_xticklabels():
		label.set_horizontalalignment('left')
	ax.set_yticks([])
	# plt.show()
	plt.savefig("stepplot.png", bbox_inches=0)

	return


def data4plot(data):
	"""
	Returns data suitably formatted for a bar plot.
	"""
	times, events = data

	eventtimes = zip(times, events)

	# if the first event is sleep, discard it
	if not eventtimes[0][1]:
		eventtimes.pop(0)

	# seperate the starting times from the finishing times
	def getStartEnd(alist):
		start_times, end_times = list(), list()
		for el in alist:
			event_start = el[1]
			if event_start:
				start_times.append(el)
			else:
				end_times.append(el)
		return map(list, [zip(*start_times)[0], zip(*end_times)[0]])

	start_times, end_times = getStartEnd(eventtimes)

	# end_times will always be one short since the computer is ON to process this data
	# so we add the most recent time to endtime so that the latest bar appears
	end_times.append(datetime.datetime.now().replace(microsecond=0))
	assert len(start_times) == len(end_times)

	# calculate the elapsed time
	intervals = [ sleep - wake for wake, sleep in zip(start_times, end_times) ]

	return start_times, end_times, intervals


def makeBarPlot(data):
	"""
	data:	3-tuple of lists
			start_times:	list of datetime instances for event start
			end_times:		list of datetime instances for event end
			intervals:		list of timedelta instances for event duration

	Makes a bar plot, date vs. time of the computer activity.

	It's easy to put in the date data as datetime instances, but
	the time data needs a workaround. We turn the datetime intances
	into integers and then format the time axis accordingly.

	Places were there are a lot of lines as opposed to one block
	shows I was very attentive! [ironic]
	"""
	start_times, end_times, intervals = data

	## x axis date data
	days = [ dt.date() for dt in start_times ]

	## y axis workaround
	def dt2m(dt):
		return (dt.hour*60) + dt.minute
	interval_mins   = [ i.seconds/60 for i in intervals ]	# height of the bars
	starttimes_mins = [ dt2m(dt) for dt in start_times ]	# bottom point of the bars


	## Set up the plot
	fig = plt.figure()						# figsize in inches
	ax = fig.add_subplot(1, 1, 1)

	## bar is (x, height of bar, bottom of bar)
	plt.bar(days, interval_mins, bottom=starttimes_mins, align="edge", edgecolor='none')


	## Customize the plot

	## Customize the x axis
	# set limits for the x axis
	first_day = days[0]
	last_day  = days[-1]
	# ax.set_xlim([first_day, last_day + datetime.timedelta(days=1)])
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %e')) # format x axis tick labels as "mmm dd"
	for label in ax.get_xticklabels():						# align the labels to the left of their column (the right of the tick label)
		label.set_horizontalalignment('left')

	## Customize the y axis
	ax.set_ylim([0, 24*60])
	ax.yaxis.set_minor_locator(plt.MultipleLocator(60))		# a tick mark every hour
	ax.yaxis.set_major_locator(plt.MultipleLocator(4*60))	# a tick label every 4 hours
	# format y axis tick labels as Hour:Minute using a custom formatter
	def m2hm(x, i):
		h = int(x/60)
		m = int(x%60)
		return '%(h)2d:%(m)02d' % {'h':h,'m':m}				# hours don't show a leading 0 zero
	ax.yaxis.set_major_formatter(ff(m2hm))					# the custom formatter


	plt.savefig("barplot2.png")
	return


def main():
	data = parseTime(FILE)
	makeStepPlot(data)
	makeBarPlot(data4plot(data))
	print "Done !"
	return

if __name__ == "__main__":

	sys.exit(main())


# stats
# total_time = sum(intervals, datetime.timedelta())
