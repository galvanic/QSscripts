from comptime import FILE, ON, OFF

filename = FILE

with open(filename) as f:
	events = list()
	for i, row in enumerate(f):
		event = row.split()[0]
		events.append(event)
		if len(events) == 1:
			continue
		if (event in ON and events[i-1] in ON) or (event in OFF and events[i-1] in OFF):
			print "There is a problem at lines %d and %d" % (i-1, i)
			print row
		
