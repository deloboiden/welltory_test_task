import os
import json
import jsonschema

schemasDirectory = os.path.join(os.path.abspath(os.getcwd()), 'task_folder', 'schema')
jsonsDirectory = os.path.join(os.path.abspath(os.getcwd()), 'task_folder', 'event')

schemasList = os.listdir(schemasDirectory)
jsonsList = os.listdir(jsonsDirectory)

with open(os.path.join(os.path.abspath(os.getcwd()), 'README.md'), 'w') as outputFile:
    for schemaFilename in schemasList:
        with open(os.path.join(schemasDirectory, schemaFilename)) as schemaFile:
            schema = json.load(schemaFile)
        try:
            jsonschema.Draft7Validator.check_schema(schema)
        except Exception as ex:
            outputFile.write("Error with schema {}\n: {};\n".format(schemaFilename, ex))
            continue
        for jsonFilename in jsonsList.copy():
            with open(os.path.join(jsonsDirectory, jsonFilename)) as jsonFile:
                json_data = json.load(jsonFile)
            if json_data is None or len(json_data) == 0:
                outputFile.write("json file {} is empty;\n".format(jsonFilename))
                jsonsList.remove(jsonFilename)
                continue
            if json_data.get('event') is None:
                outputFile.write("json file {} has not event;\n".format(jsonFilename))
                jsonsList.remove(jsonFilename)
                continue
            if json_data['event'] == schemaFilename.replace('.schema', ''):
                validator = jsonschema.Draft7Validator(schema)
                errorString = "error in file {} with schema {}:\n".format(jsonFilename, json_data['event'])
                for error in sorted(validator.iter_errors(json_data), key=str):
                    errorString += "{};\n".format(error.message)
                outputFile.write(errorString)
                jsonsList.remove(jsonFilename)

    for jsonFilename in jsonsList:
        with open(os.path.join(jsonsDirectory, jsonFilename)) as jsonFile:
            json_data = json.load(jsonFile)
        outputFile.write("file {} with event {} does not fit any valid scheme;\n".format(jsonFilename,
                                                                                         json_data['event']))
