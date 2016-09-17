import sys
import plot
import json_sanitize

OPTIONS = ["LOCATION", "BATTERY", "MILEAGE"]

if(len(sys.argv) != 3):
	raise Exception("Wrong argument passed. Usage: {:s} data.json ".format(__name__))


fname = sys.argv[1]
json = json_sanitize(fname)


if(sys.argv[2] == 1)