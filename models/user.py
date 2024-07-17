from config.database import db
user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Username", "Password", "First_name", "Last_name", "Email", "Mobile", "isAdmin", "isVerified", "age", "policies"],
        "properties": {
            "Username": {
                "bsonType": "string",
                "description": "Username of the user"
            },
            "Password": {
                "bsonType": "string",
                "description": "Password of the user"
            },
            "First_name": {
                "bsonType": "string",
                "description": "First name of the user"
            },
            "Last_name": {
                "bsonType": "string",
                "description": "Last name of the user"
            },
            "Email": {
                "bsonType": "string",
                "description": "Email address of the user"
            },
            "Mobile": {
                "bsonType": "string",
                "description": "Mobile number of the user"
            },
            "isAdmin": {
                "bsonType": "bool",
                "description": "Admin status of the user",
            },
            "isVerified": {
                "enum": ["pending", "rejected", "accepted"],
                "description": "Verification status of the user",
            },
            "age": {
                "bsonType": "int",
                "minimum": 18,
                "description": "Age of the user"
            },
            "policies": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["policy_id","category", "policy_name", "sum_assured", "duration", "premium", "claimed_amounts", "left_amount"],
                    "properties": {
                        "policy_id": {"bsonType": "string"},
                        "category": {
                            "bsonType": "string",
                            "description": "Category of the policy"
                        },
                        "policy_name": {
                            "bsonType": "string",
                            "description": "Name of the policy"
                        },
                        "sum_assured": {
                            "bsonType": "double",
                            "minimum": 100000,
                            "maximum": 10000000,
                            "description": "Sum assured for the policy"
                        },
                        "duration": {
                            "bsonType": "string",
                            "description": "Duration of the policy"
                        },
                        "premium": {
                            "bsonType": "double",
                            "description": "Premium amount for the policy"
                        },
                        "claimed_amounts": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "double"
                            },
                            "description": "Array storing each claimed amount"
                        },
                        "left_amount": {
                            "bsonType": "double",
                            "description": "Amount left initially equal to the sum assured but overtime minus the claimed amount",
                        }
                    }
                },
                "description": "Policies of the user"
            }
        }
    }
}
try:
    user_collection = db['user']
    if 'user' not in db.list_collection_names():
        policies_collection = db.create_collection('user', validator=user_schema)
except Exception as e:
    print(f"An unexpected error occurred during MongoDB setup: {e}")
    exit()
