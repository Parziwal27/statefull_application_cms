# models/claim.py
from config.database import db

claim_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["policyholder_id", "policy_name", "amount", "status"],
        "properties": {
            "policyholder_id": {"bsonType": "objectId"},
            "policy_name": {"bsonType": "string"},
            "amount": {"bsonType": "double"},
            "status": {
                "bsonType": "string",
                "enum": ["pending", "approved", "rejected"]
            }
        }
    }
}

if 'claim' in db.list_collection_names():
    claim_collection = db['claim']
else:
    claim_collection = db.create_collection('claim', validator=claim_schema)
