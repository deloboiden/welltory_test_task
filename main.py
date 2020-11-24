import os
import json
import jsonschema


schemasDirectory = os.path.join(os.path.abspath(os.getcwd()), 'task_folder', 'schema')
jsonsDirectory = os.path.join(os.path.abspath(os.getcwd()), 'task_folder', 'event')

schemasList = os.listdir(schemasDirectory)
jsonsList = os.listdir(jsonsDirectory)

for schema_filename in schemasList:
    with open(os.path.join(schemasDirectory, schema_filename)) as schema_file:
        schema = json.load(schema_file)
    try:
       jsonschema.Draft7Validator.check_schema(schema)
    except Exception as ex:
        print("Error with schema {}\n: {}".format(schema_filename, ex))
        continue
    for json_filename in jsonsList.copy():
        with open(os.path.join(jsonsDirectory, json_filename)) as json_file:
            json_data = json.load(json_file)
        if json_data is None or len(json_data) == 0:
            print("json file {} is empty".format(json_filename))
            jsonsList.remove(json_filename)
            continue
        if json_data.get('event') is None:
            print("json file {} has not event".format(json_filename))
            jsonsList.remove(json_filename)
            continue
        if json_data['event'] == schema_filename.replace('.schema', ''):
            validator = jsonschema.Draft7Validator(schema)
            for error in sorted(validator.iter_errors(json_data), key=str):
                print("error in file {} with schema {}\n: {}".format(json_filename, json_data['event'], error.message))
            jsonsList.remove(json_filename)

for json_filename in jsonsList:
    with open(os.path.join(jsonsDirectory, json_filename)) as json_file:
        json_data = json.load(json_file)
    print("file {} with event {} does not fit any valid scheme".format(json_filename, json_data['event']))
