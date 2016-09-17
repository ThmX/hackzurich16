import sys
import plot
import json
import datetime
import numpy as np
import glob
from matplotlib import pyplot as plt

def init():
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

	return option, json_datasets

def get_battery_dataset(json_datasets):
	datasets = [list(filter(lambda x : "MDI_EXT_BATT_VOLTAGE" in x["fields"], data)) for data in json_datasets]
	x = [[data["received_at"] for data in dataset] for dataset in datasets]
	y = [np.array([data["fields"]["MDI_EXT_BATT_VOLTAGE"] for data in dataset])/1000. for dataset in datasets]
	return x, y

def get_acc_datasets(json_datasets):
	datasets = [list(
		filter(lambda x : all((key in x["fields"] 
			for key in ("BEHAVE_ACC_X_PEAK", "BEHAVE_ACC_Y_PEAK", "BEHAVE_ACC_Z_PEAK"))), data))
	for data in json_datasets]

	x = [[data["received_at"] for data in dataset] for dataset in datasets]
	acc_x = [np.array([row["fields"]["BEHAVE_ACC_X_PEAK"] for row in dataset]) for dataset in datasets]
	acc_y = [np.array([row["fields"]["BEHAVE_ACC_Y_PEAK"] for row in dataset]) for dataset in datasets]
	acc_z = [np.array([row["fields"]["BEHAVE_ACC_Z_PEAK"] for row in dataset]) for dataset in datasets]
	
	return x, acc_x, acc_y, acc_z	

def get_location_datasets(json_datasets):
	x = [[row["loc"][0] for row in dataset if row["loc"]] for dataset in json_datasets]
	y = [[row["loc"][1] for row in dataset if row["loc"]] for dataset in json_datasets]
	return x, y

def get_rpm_averages(json_datasets):
	keys = ["MDI_RPM_AVERAGE", "MDI_RPM_AVERAGE_RANGE_1", "MDI_RPM_AVERAGE_RANGE_2", "MDI_RPM_AVERAGE_RANGE_3", "MDI_RPM_AVERAGE_RANGE_4"]
	datasets = [list(filter(lambda x : any((key in x["fields"] for key in keys)), data)) for data in json_datasets]

	x = [[data["received_at"] for data in dataset] for dataset in datasets]	
	avg = [np.array([row["fields"]["MDI_RPM_AVERAGE"] for row in dataset if "MDI_RPM_AVERAGE" in row["fields"]]) for dataset in datasets]
	range_1 = [np.array([row["fields"]["MDI_RPM_AVERAGE_RANGE_1"] for row in dataset if "MDI_RPM_AVERAGE_RANGE_1" in row["fields"]]) for dataset in datasets]
	range_2 = [np.array([row["fields"]["MDI_RPM_AVERAGE_RANGE_2"] for row in dataset if "MDI_RPM_AVERAGE_RANGE_2" in row["fields"]]) for dataset in datasets]
	range_3 = [np.array([row["fields"]["MDI_RPM_AVERAGE_RANGE_3"] for row in dataset if "MDI_RPM_AVERAGE_RANGE_3" in row["fields"]]) for dataset in datasets]
	range_4 = [np.array([row["fields"]["MDI_RPM_AVERAGE_RANGE_4"] for row in dataset if "MDI_RPM_AVERAGE_RANGE_4" in row["fields"]]) for dataset in datasets]
	return x, avg, range_1, range_2, range_3, range_4
	
def get_dataset_by_key(json_datasets, key, time=False):
	datasets = [list(filter(lambda x : key in x["fields"], data)) for data in json_datasets]
	x = [[data["received_at"] for data in dataset] for dataset in datasets]	
	y = [np.array([data["fields"][key] for data in dataset])/1000. for dataset in datasets]

	if(time):
		return x, y
	else:
		return y


############## MAIN ################

if(__name__ == "__main__"):

	option, json_datasets = init()

	if(option == "BATTERY"):
		x, y = get_battery_dataset(json_datasets)
		print(len(x[0]), len(y[0]))
		plot.plot(x, y, "Battery", "Time", "Voltage[V]")

	if(option == "LOCATION"):
		x, y = get_location_datasets(json_datasets)
		plot.plot(x, y, "LOCATION", "Lattitude", "Longitude")

	if(option == "ACC_PEAK"):
		x, acc_x, acc_y, acc_z = get_acc_datasets(json_datasets)
		acc = np.array([np.sqrt(x_single_car**2 + y_single_car**2 + z_single_car**2) 
			for x_single_car, y_single_car, z_single_car in zip(acc_x, acc_y, acc_z)])
		plot.plot(x, acc, "Acceleration peaks", "Time", "Acceleration[mG]")

	if(option == "RPM_AVG"):
		x, avg_rpm, range_1, range_2, range_3, range_4 = get_rpm_averages(json_datasets)
		alpha = 0.5
		plt.subplot(211)		
		plt.hist(avg_rpm[0], bins=15, color=plot.tableau20[0], alpha=alpha, normed=True)
		plt.hist(range_1[0], bins=15, color=plot.tableau20[2], alpha=alpha, normed=True)
		plt.hist(range_2[0], bins=15, color=plot.tableau20[4], alpha=alpha, normed=True)
		plt.hist(range_3[0], bins=15, color=plot.tableau20[6], alpha=alpha, normed=True)
		plt.hist(range_4[0], bins=15, color=plot.tableau20[8], alpha=alpha, normed=True)

		plt.subplot(212)
		plt.hist(avg_rpm[1], bins=15, color=plot.tableau20[0], alpha=alpha, normed=True)
		plt.hist(range_1[1], bins=15, color=plot.tableau20[2], alpha=alpha, normed=True)
		plt.hist(range_2[1], bins=15, color=plot.tableau20[4], alpha=alpha, normed=True)
		plt.hist(range_3[1], bins=15, color=plot.tableau20[6], alpha=alpha, normed=True)
		plt.hist(range_4[1], bins=15, color=plot.tableau20[8], alpha=alpha, normed=True)
		plt.show()	

	if(option == "CRASH"):
		times = [[] for i in range(4)]

		times[0], crash = get_dataset_by_key(json_datasets, "MDI_CRASH_DETECTED", time=True)
		times[1], acc_x = get_dataset_by_key(json_datasets, "BEHAVE_ACC_X_PEAK", time=True)
		times[2], acc_y = get_dataset_by_key(json_datasets, "BEHAVE_ACC_Y_PEAK", time=True)
		times[3], acc_z = get_dataset_by_key(json_datasets, "BEHAVE_ACC_Z_PEAK", time=True)

		acc = [np.sqrt(np.array(acc_x_i)**2 + np.array(acc_y_i)**2 + np.array(acc_z_i)**2) for 
			acc_x_i, acc_y_i, acc_z_i in zip(acc_x, acc_y, acc_z)]

		plt.subplot(211)
		plot.plot(times[0], crash, xlab = "Time", ylab="Crash event", title="CRASH")
		plt.subplot(212)
		plot.plot(times[1], acc, xlab = "Time", ylab="Acceleration", title="ACC")



			