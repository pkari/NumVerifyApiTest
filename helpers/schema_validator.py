import os
import json
from jsonschema import validate, ValidationError


class JSONHelper:

    @staticmethod
    def open_json_schema(file):
        try:
            current_dir = os.path.dirname(__file__)
            schema_path = os.path.join(current_dir, '..', 'schemas', file)
            schema_path = os.path.abspath(schema_path)

            with open(schema_path) as schema_file:
                schema = json.load(schema_file)

            return schema
        except (OSError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load schema '{file}': {e}")

    @staticmethod
    def schema_validator(data, schema_file):
        try:
            schema = JSONHelper.open_json_schema(schema_file)
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            return e
