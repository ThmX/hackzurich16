import sys
import plot
import json
import datetime
import numpy as np
import glob
from matplotlib import pyplot as plt
import bisect
import json
import time

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect.bisect_left(a, x)
    if i:
        return i-1
    raise ValueError


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

	return car_ids, option, json_datasets

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

def get_dataset_by_key(json_datasets, key, time=False):
	datasets = [list(filter(lambda x : key in x["fields"], data)) for data in json_datasets]
	x = [[data["received_at"] for data in dataset] for dataset in datasets]	
	y = [np.array([data["fields"][key] for data in dataset]) for dataset in datasets]

	if(time):
		return x, y
	else:
		return y


############## MAIN ################

if(__name__ == "__main__"):

	car_ids, option, json_datasets = init()

	if(option == "BATTERY"):
		x, y = get_dataset_by_key(json_datasets, "MDI_EXT_BATT_VOLTAGE", time=True)
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
		times = [[] for i in range(6)]
		times[0], avg_rpm = get_dataset_by_key(json_datasets, "MDI_RPM_AVERAGE", time=True)
		times[1], range_1 = get_dataset_by_key(json_datasets, "MDI_RPM_AVERAGE_RANGE_1", time=True)
		times[2], range_2 = get_dataset_by_key(json_datasets, "MDI_RPM_AVERAGE_RANGE_2", time=True)
		times[3], range_3 = get_dataset_by_key(json_datasets, "MDI_RPM_AVERAGE_RANGE_3", time=True)
		times[4], range_4 = get_dataset_by_key(json_datasets, "MDI_RPM_AVERAGE_RANGE_4", time=True)
		times[5], rpm_odb = get_dataset_by_key(json_datasets, "MDI_OBD_RPM", time=True)

		alpha = 0.5
		for i in range(len(times[0])):
			plt.subplot(len(times[0]), 1, i+1)
			data = [avg_rpm[i], range_1[i], range_2[i], range_3[i], range_4[i], rpm_odb[i] ]
			colors = [plot.tableau20[2*i] for i in range(len(data))]
			labels = ["avg", "range1", "range2", "range3", "range4", "odb"]
			plt.hist(data, 20, normed=1, histtype='stepfilled', color=colors, label=labels, alpha=0.5)
			plt.legend(prop={"size": 10})
		plt.show()	

	if(option == "RPM_FUEL"):
		times = [[], [], []]
		times[0], rpm_odb = get_dataset_by_key(json_datasets, "MDI_OBD_RPM", time=True)
		times[1], consumed_measured = get_dataset_by_key(json_datasets, "MDI_OBD_FUEL", time=True)
		times[2], mileage = get_dataset_by_key(json_datasets, "ODO_FULL", time=True) 

		mileage = [mil - np.min(mil) for mil in mileage]
		consumed_measured = [mil - np.min(mil) for mil in consumed_measured]

		# consts = [0.00018621021365193117, 0.00008486945108872097]
		# meas_noise = [15, 12]
		# proc_noise = [0.5, 0.3]

		# consumed_kalman = [np.zeros(len(times[0][k])) for k in range(len(times[0]))]
		# consumed_var = [np.zeros(len(times[0][k])) for k in range(len(times[0]))]

		# # Kalman filter for consumed fuel
		# for k in range(len(times[0])):
		# 	t0 = times[1][k][0]
		# 	consumed_kalman[k][0] = 0
		# 	consumed_var[k][0] = 0

		# 	const = consts[k]
		# 	for i in range(1, len(times[0][k])):
				
		# 		# Prediction step
		# 		dt = (times[0][k][i]-times[0][k][i-1]).total_seconds()
		# 		consumed_kalman[k][i] = consumed_kalman[k][i-1] + rpm_odb[k][i]*dt*const
		# 		consumed_var[k][i] = consumed_var[k][i] + proc_noise[k]*dt

		# 		# Search for the measurement closest to the current prediction
		# 		try:
		# 			j = find_lt(times[1][k], times[0][k][i])
		# 		except:
		# 			continue

		# 		dt_betw_meas_and_rpm = (times[1][k][j] - times[0][k][i]).total_seconds()

		# 		# Correction
		# 		kgain = consumed_var[k][i] / (consumed_var[k][i] + meas_noise[k]*dt_betw_meas_and_rpm)
		# 		consumed_kalman[k][i] += kgain*(consumed_measured[k][j] - consumed_kalman[k][i])
		# 		consumed_var[k][i] = (1 - kgain)*consumed_var[k][i]

		times1_float = [np.array([(time - t[0]).total_seconds() for time in t]) for t in times[1]]
		times2_float = [np.array([(time - t[0]).total_seconds() for time in t]) for t in times[2]]
		mileage_interp = [np.interp(times1_float[k], times2_float[k], mileage[k]) for k in range(len(consumed_measured))]	

		# to be investigated why 10e-2 works, instead of 10e-3
		rate = [10e-2*consumed_measured[k]/(mileage_interp[k] + np.finfo(float).eps)  for k in range(len(consumed_measured))]

		for k, car_id in enumerate(car_ids):
			with open("{}_fuelrate.json".format(car_id), "w") as f:
				data = [(int(time.mktime(x.timetuple())), y) for x, y in zip(times[1][k], rate[k])]
				f.write(json.dumps(data))
			