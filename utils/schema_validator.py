import json

from jsonschema import validate, ValidationError

# Load json schema from file
def load_schema(schema_path):
    with open(schema_path, "r") as file:
        return json.load(file)
    
# Validate response using json schema
def validate_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as e:
        raise ValidationError(f"Schema validation error: {e.message}")
    
