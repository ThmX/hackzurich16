import sys
import plot

if(len(sys.argv) != 2):
	raise Exception("Wrong argument passed. Usage: {:s} data.json".format(__name__))
