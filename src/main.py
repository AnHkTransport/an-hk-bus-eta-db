import json
import os
import database
from jsonschema import validate

if __name__ == '__main__':
    os.chdir('..')
    try:
        db_json = database.get_remote_hkbusetadb_text()
        an_db = database.generate_db_for_android(db_json)
        pretty_an_db = json.dumps(an_db, indent=4, ensure_ascii=False)

        with open('schema/AndroidRouteFareListSchema.json', 'r', encoding='utf-8') as schema_file:
            an_db_schema = json.load(schema_file)
            validate(an_db, an_db_schema)

        with open('data/AndroidRouteFareList.json', 'w', encoding='utf-8') as f:
            f.writelines(pretty_an_db)

    except (TypeError, ValueError, KeyError) as err:
        print(type(err), err)
