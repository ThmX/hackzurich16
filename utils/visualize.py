import sys
import plot
import json
import datetime
import numpy as np
import glob

OPTIONS = ["LOCATION", "BATTERY", "MILEAGE"]

if(len(sys.argv) < 4):
	raise Exception("Wrong argument passed. Usage: visualize data_folder option car_id#1 car_id#2 ...")

path = sys.argv[1]
option = sys.argv[2]
car_ids = sys.argv[3:] 
filelist_set = [[x for x in glob.glob("{}/{}*.json".format(path, car_id)) 
	if "raw" not in x] for car_id in car_ids]

json_datasets = []
for filelist in filelist_set:
	json_data = []
	for fname in filelist:
		with open(fname) as f:
			try:
				json_data += json.loads(f.read())
			except:
				print(fname)
	json_datasets.append(json_data)

for j, json_data in enumerate(json_datasets):
	for i, row in enumerate(json_data):
		json_data[i]["received_at"] = datetime.datetime.fromtimestamp(row["received_at"])
		json_data[i]["recorded_at"] = datetime.datetime.fromtimestamp(row["recorded_at"])	
	json_datasets[j] = json_data

if(option == "BATTERY"):
	datasets = [list(filter(lambda x : "MDI_EXT_BATT_VOLTAGE" in x["fields"], data)) for data in json_datasets]

	x = [[data["received_at"] for data in dataset] for dataset in datasets]
	y = [np.array([data["fields"]["MDI_EXT_BATT_VOLTAGE"] for data in dataset])/1000. for dataset in datasets]
	plot.plot(x, y, "Battery", "Time", "Voltage[V]")


if(option == "LOCATION"):
	x = [[row["loc"][0] for row in dataset if row["loc"]] for dataset in json_datasets]
	y = [[row["loc"][1] for row in dataset if row["loc"]] for dataset in json_datasets]

	plot.plot(x, y, "LOCATION", "Lattitude", "Longitude")

if(option == "ACC_PEAK"):
	datasets = [list(
		filter(lambda x : all((key in x["fields"] 
			for key in ("BEHAVE_ACC_X_PEAK", "BEHAVE_ACC_Y_PEAK", "BEHAVE_ACC_Z_PEAK"))), data))
	for data in json_datasets]

	x = [[data["received_at"] for data in dataset] for dataset in datasets]

	acc_x = [np.array([row["fields"]["BEHAVE_ACC_X_PEAK"] for row in dataset]) for dataset in datasets]
	acc_y = [np.array([row["fields"]["BEHAVE_ACC_Y_PEAK"] for row in dataset]) for dataset in datasets]
	acc_z = [np.array([row["fields"]["BEHAVE_ACC_Z_PEAK"] for row in dataset]) for dataset in datasets]

	acc = [np.sqrt(x_single_car**2 + y_single_car**2 + z_single_car**2) 
		for x_single_car, y_single_car, z_single_car in zip(acc_x, acc_y, acc_z)]

	plot.plot(x, acc, "Acceleration peaks", "Time", "Acceleration[mG]")


