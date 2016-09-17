import simplejson
import datetime
import base64
import struct

def sanitize_json(fn):
	STRING_LABELS = ["GPRMC_VALID", "ODO_PARTIAL_KM", "AREA_LIST", "MDI_CRASH_DETECTED", 
			"MDI_OBD_STACK_NAME", "EVENT", "MDI_PANIC_MESSAGE", "MDI_SENSORS_RECORDER_DATA",
			"MDI_SENSORS_RECORDER_CALIBRATION", "MDI_OBD_PID_1", "MDI_OBD_PID_2", "MDI_OBD_PID_3", 
			"MDI_OBD_PID_4", "MDI_OBD_PID_5", "MDI_DIAG_1", "MDI_DIAG_2", "MDI_DIAG_3", "MDI_VEHICLE_STATE", 
			"MDI_OBD_VIN", "MDI_CUSTOM_PID_1", "MDI_CUSTOM_PID_1", "MDI_CUSTOM_PID_2", "MDI_CUSTOM_PID_3", 
			"MDI_CUSTOM_PID_4", "MDI_CUSTOM_PID_5", "MDI_CUSTOM_PID_6", "MDI_CUSTOM_PID_7", "MDI_CUSTOM_PID_8", 
			"MDI_CUSTOM_PID_9", "MDI_CUSTOM_PID_10", "MDI_CUSTOM_PID_11", "MDI_CUSTOM_PID_12", "MDI_CUSTOM_PID_13", 
			"MDI_CUSTOM_PID_14", "MDI_CUSTOM_PID_15", "MDI_CUSTOM_PID_16", "MDI_CUSTOM_PID_17", "MDI_CUSTOM_PID_18", 
			"MDI_CUSTOM_PID_19", "MDI_CUSTOM_PID_20", "MDI_CUSTOM_PID_21", "MDI_CUSTOM_PID_22", "MDI_CUSTOM_PID_23", 
			"MDI_CUSTOM_PID_24", "MDI_CUSTOM_PID_25", "MDI_CUSTOM_PID_26", "MDI_CUSTOM_PID_27", "MDI_CUSTOM_PID_28", 
			"MDI_CUSTOM_PID_29", "MDI_CUSTOM_PID_30", "MDI_CUSTOM_PID_31", "MDI_CUSTOM_PID_32", "MDI_CUSTOM_PID_33", 
			"MDI_CUSTOM_PID_34", "MDI_CUSTOM_PID_35", "MDI_CUSTOM_PID_36", "MDI_CUSTOM_PID_37", "MDI_CUSTOM_PID_38", 
			"MDI_CUSTOM_PID_39", "MDI_CUSTOM_PID_40", "MDI_CUSTOM_PID_41", "MDI_CUSTOM_PID_42", "MDI_CUSTOM_PID_43", 
			"MDI_CUSTOM_PID_44", "MDI_CUSTOM_PID_45", "MDI_CUSTOM_PID_46", "MDI_CUSTOM_PID_47", "MDI_CUSTOM_PID_48", 
			"MDI_CUSTOM_PID_49", "MDI_CUSTOM_PID_50", "MDI_CC_DTC_LIST", "ENH_DASHBOARD_MILEAGE", "ENH_DASHBOARD_FUEL",
			"ENH_DASHBOARD_FUEL_LEVEL", "MDI_CC_OIL_LEVEL", "MDI_CC_OIL_LEVEL_WARNING_THRESHOLD", "MDI_CC_OIL_LEVEL_STATUS",
			"MDI_CC_TIME_FOR_NEXT_INSPECTION", "MDI_CC_DISTANCE_FOR_NEXT_INSPECTION", "MDI_CC_DISTANCE_FOR_CHANGE_OIL", "MDI_CC_TIME_FOR_CHANGE_OIL"]

	BOOL_LABELS = ["DIO_IGNITION", "MDI_EXT_BATT_LOW", "MDI_PANIC_STATE", "MDI_DTC_MIL", "MDI_RPM_OVER", "MDI_IDLE_STATE", "MDI_TOW_AWAY",
			"MDI_JOURNEY_STATE"]

	with open(fn) as f:
		data = f.read()

	json_data = simplejson.loads(data)

	for i, row in enumerate(json_data):
		json_data[i]["received_at"] = datetime.datetime.strptime(row["received_at"], "%Y-%m-%dT%H:%M:%SZ")
		json_data[i]["recorded_at"] = datetime.datetime.strptime(row["recorded_at"], "%Y-%m-%dT%H:%M:%SZ")	
		for field in row["fields"]:
			decoded = base64.b64decode(row["fields"][field]["b64_value"])
			if field in STRING_LABELS:
				row["fields"][field] = decoded.decode()
			elif field in BOOL_LABELS:
				row["fields"][field] = struct.unpack("?", decoded)[0]
			else:
				row["fields"][field] = struct.unpack("I", decoded)[0]

		del json_data[i]["recorded_at_ms"]
		del json_data[i]["id_str"]


	return json_data


if(__name__ == "__main__"):

	if(len(sys.argv) != 2):
		raise Exception("Wrong argument passed. Usage: {:s} data.json".format(__name__))

	print(sanitize_json(sys.argv[1]))
