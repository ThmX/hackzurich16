import sanitize_json

if(len(sys.argv) != 2):
	raise Exception("Wrong argument passed. Usage: {:s} data.json".format(__name__))

print(sanitize_json(sys.argv[1]))