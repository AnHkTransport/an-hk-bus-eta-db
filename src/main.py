import json
import os
import database
from jsonschema import validate
import py7zr

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

        os.chdir('data')
        with py7zr.SevenZipFile('AndroidRouteFareList.7z', 'w') as archive:
            archive.write('AndroidRouteFareList.json')

    except (TypeError, ValueError, KeyError) as err:
        print(type(err), err)
