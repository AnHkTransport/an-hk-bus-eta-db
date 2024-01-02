import json
import os
import database

if __name__ == '__main__':
	os.chdir("..")
	# etadb_path = Path('test/EtaDbSample.json')
	# etadb_path = Path('data/routeFareList.json')
	try:
		db_json = database.get_remote_hkbusetadb_text()
		an_db = database.generate_db_for_android(db_json)
		pretty_an_db = json.dumps(an_db, indent=4, ensure_ascii=False)
		with open('data/AndroidRouteFareList.json', 'w', encoding='utf-8') as f:
			f.writelines(pretty_an_db)
	except (TypeError, ValueError, KeyError) as err:
		print(err, "in generating json for Android.")
