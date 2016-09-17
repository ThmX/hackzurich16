import sys
import plot
import json_sanitize

OPTIONS = ["LOCATION", "BATTERY", "MILEAGE"]

if(len(sys.argv) != 3):
	raise Exception("Wrong argument passed. Usage: {:s} data.json ".format(__name__))


fname, option = sys.argv[1], sys.argv[2]
json = json_sanitize(fname)

if(option == "BATTERY"):
	pass