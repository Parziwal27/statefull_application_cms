from config.database import db

policyholder_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "age", "policies"],
        "properties": {
            "name": {"bsonType": "string"},
            "age": {"bsonType": "int", "minimum": 18},
            "policies": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["category", "policy_name", "sum_assured", "duration", "premium"],
                    "properties": {
                        "category": {"bsonType": "string"},
                        "policy_name": {"bsonType": "string"},
                        "sum_assured": {"bsonType": "double", "minimum": 100000, "maximum": 10000000},
                        "duration": {"bsonType": "string"},
                        "premium": {"bsonType": "double"}
                    }
                }
            }
        }
    }
}

if 'policy_holder' in db.list_collection_names():
    policy_holder_collection = db['policy_holder']
else:
    policy_holder_collection = db.create_collection('policy_holder', validator=policyholder_schema)
