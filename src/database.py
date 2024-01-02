import json
from urllib.request import urlopen


def get_remote_hketadb_md5_text() -> str:
	md5_file_url = r'https://raw.githubusercontent.com/hkbus/hk-bus-crawling/gh-pages/routeFareList.md5'
	return urlopen(md5_file_url).read().decode('utf-8')


def get_remote_hkbusetadb_text() -> str:
	db_file_url = r'https://raw.githubusercontent.com/hkbus/hk-bus-crawling/gh-pages/routeFareList.json'
	return urlopen(db_file_url).read().decode('utf-8')


def generate_db_for_android(db_json: str) -> dict:
	android_db = dict()
	db = json.loads(db_json)
	android_db["holidays"] = db["holidays"]
	android_db["routeList"] = generate_route_list_value(db["routeList"])
	android_db["serviceDayMap"] = generate_service_day_map_value(db["serviceDayMap"])
	android_db["stopList"] = generate_stop_list_value(db["stopList"])
	android_db["stopMap"] = generate_stop_map_value(db["stopMap"])
	return android_db


def generate_route_list_value(d: dict) -> list:
	d = json_key_to_fields_as_list_of_objects(d, "name")
	for route in d:
		for k, v in route.items():
			if k == "bound":
				route[k] = json_single_key_value_as_two_key_values(v, "co", "dir")
			if k == "freq" and v is not None:
				route[k] = generate_freq_value(v)
			if k == "stops":
				route[k] = json_single_key_value_as_two_key_values(v, "co", "stopIds")
	return d


def generate_service_day_map_value(d: dict) -> list:
	return json_key_to_list_as_list_of_objects(d, "serviceDayId", "mapping")


def generate_stop_list_value(d: dict) -> list:
	return json_key_to_fields_as_list_of_objects(d, "stopId")


def generate_freq_value(d: dict) -> list:
	_freq_list = list()
	for k, v in d.items():
		_new_item = dict()
		_new_item["serviceDayId"] = k
		for inner_k, inner_v in v.items():
			_new_item["startTime"] = inner_k
			if inner_v is None:
				_new_item["endTime"] = None
				_new_item["intervalInSeconds"] = None
			else:
				_new_item["endTime"] = inner_v[0]
				_new_item["intervalInSeconds"] = inner_v[1]
		_freq_list.append(_new_item)
	return _freq_list


def generate_stop_map_value(d: dict) -> list:
	_list = list()
	for k, v in d.items():
		_dict = dict()
		_dict["stopId"] = k
		_dict["equivalent"] = json_list_of_lists2_to_list_of_objects(v, "co", "stopId")
		_list.append(_dict)
	return _list


def json_single_key_value_as_two_key_values(d: dict, key_field_name: str, value_field_name: str) -> dict:
	_dict = dict()
	_dict[key_field_name] = list(d.keys())[0]
	_dict[value_field_name] = list(d.values())[0]
	return _dict


def json_key_to_list_as_list_of_objects(d: dict, key_field_name: str, list_field_name: str) -> list:
	_list = list()
	for k, v in d.items():
		_item = dict()
		_item[key_field_name] = k
		_item[list_field_name] = v
		_list.append(_item)
	return _list


def json_key_to_fields_as_list_of_objects(d: dict, key_field_name: str) -> list:
	_list = list()
	for k, v in d.items():
		_item = dict()
		_item[key_field_name] = k
		for inner_k, inner_v in v.items():
			_item[inner_k] = inner_v
		_list.append(_item)
	return _list


def json_list_of_lists2_to_list_of_objects(_list: list, key_name: str, value_name: str) -> list:
	new_list = list()
	for list_item in _list:
		if isinstance(list_item, list) and len(list_item) != 2:
			raise ValueError("The list should contains list of list and each list of list should have size 2 exactly.")
		_dict = dict()
		_dict[key_name] = list_item[0]
		_dict[value_name] = list_item[1]
		new_list.append(_dict)
	return new_list
