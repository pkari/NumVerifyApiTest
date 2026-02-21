import os
import json
from jsonschema import validate, ValidationError


class JSONHelper:

    @staticmethod
    def open_json_schema(file):
        # Get the directory of the current file (helpers/test_file.py)
        current_dir = os.path.dirname(__file__)

        # Go up one level to project_root, then into schemas/
        schema_path = os.path.join(current_dir, '..', 'schemas', file)

        # Normalize the path (handles .. correctly)
        schema_path = os.path.abspath(schema_path)

        with open(schema_path) as schema_file:
            schema = json.load(schema_file)

        return schema

    @staticmethod
    def schema_validator(data):
        try:
            schema = JSONHelper.open_json_schema("GET_numverify.json")
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            return e
