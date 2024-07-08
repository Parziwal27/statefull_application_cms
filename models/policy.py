from config.database import db

policy_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["category", "name", "sum_assured", "premium_plans"],
        "properties": {
            "category": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "sum_assured": {
                "bsonType": "double",
                "minimum": 100000,
                "maximum": 10000000 
            }, 
            "premium_plans": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["duration", "premium"],
                    "properties": {
                        "duration": {"bsonType": "string"},
                        "premium": {"bsonType": "double"}
                    }
                }
            }
        }
    }
}

# Categories of policies with realistic data
policy_data = [
    {
        "category": "Life",
        "policies": [
            {
                "name": "Term Life Insurance",
                "sum_assured": 1000000.0,  # Use float to match bsonType 'double'
                "premium_plans": [
                    {"duration": "1 year", "premium": 10000.0},  # Use float for premium
                    {"duration": "5 years", "premium": 45000.0},
                    {"duration": "10 years", "premium": 85000.0}
                ]
            },
            {
                "name": "Term Life Insurance",
                "sum_assured": 5000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 25000.0},
                    {"duration": "5 years", "premium": 100000.0},
                    {"duration": "15 years", "premium": 200000.0}
                ]
            },
            {
                "name": "Term Life Insurance",
                "sum_assured": 2000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 15000.0},
                    {"duration": "10 years", "premium": 70000.0},
                    {"duration": "20 years", "premium": 150000.0}
                ]
            },
            {
                "name": "Term Life Insurance",
                "sum_assured": 3000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 18000.0},
                    {"duration": "7 years", "premium": 60000.0},
                    {"duration": "12 years", "premium": 120000.0}
                ]
            }

        ]
    },
    {
        "category": "Car",
        "policies": [
            {
                "name": "Comprehensive Car Insurance",
                "sum_assured": 500000.0,  # Use float to match bsonType 'double'
                "premium_plans": [
                    {"duration": "1 year", "premium": 8000.0},
                    {"duration": "2 years", "premium": 15000.0},
                    {"duration": "3 years", "premium": 22000.0}
                ]
            },
            {
                "name": "Third Party Car Insurance",
                "sum_assured": 200000.0,  # Use float to match bsonType 'double'
                "premium_plans": [
                    {"duration": "1 year", "premium": 4000.0},
                    {"duration": "2 years", "premium": 7500.0},
                    {"duration": "3 years", "premium": 11000.0}
                ]
            }
        ]
    },
    {
        "category": "Home",
        "policies": [
            {
                "name": "House Insurance - Basic",
                "sum_assured": 1000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 20000.0},
                    {"duration": "5 years", "premium": 90000.0},
                    {"duration": "10 years", "premium": 160000.0}
                ]
            },
            {
                "name": "House Insurance - Comprehensive",
                "sum_assured": 5000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 35000.0},
                    {"duration": "7 years", "premium": 150000.0},
                    {"duration": "15 years", "premium": 280000.0}
                ]
            },
            {
                "name": "House Insurance - Premium",
                "sum_assured": 10000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 60000.0},
                    {"duration": "7 years", "premium": 250000.0},
                    {"duration": "15 years", "premium": 480000.0}
                ]
            }
        ]
    },
    {
        "category": "Health",
        "policies": [
            {
                "name": "Health Insurance - Basic",
                "sum_assured": 1000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 15000.0},
                    {"duration": "5 years", "premium": 70000.0},
                    {"duration": "10 years", "premium": 130000.0}
                ]
            },
            {
                "name": "Health Insurance - Comprehensive",
                "sum_assured": 5000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 30000.0},
                    {"duration": "7 years", "premium": 120000.0},
                    {"duration": "15 years", "premium": 220000.0}
                ]
            },
            {
                "name": "Health Insurance - Premium",
                "sum_assured": 10000000.0,
                "premium_plans": [
                    {"duration": "1 year", "premium": 50000.0},
                    {"duration": "10 years", "premium": 200000.0},
                    {"duration": "20 years", "premium": 380000.0}
                ]
            }
        ]
    }
]

try:
    policies_collection = db['policies']

    # Create policies collection with schema validation
    if 'policies' not in db.list_collection_names():
        policies_collection = db.create_collection('policies', validator=policy_schema)

    # Insert policies data if collection is empty
    if policies_collection.count_documents({}) == 0:
        for category_data in policy_data:
            for policy in category_data['policies']:
                policy['category'] = category_data['category']
            policies_collection.insert_many(category_data['policies'])

    print("MongoDB collections are ready.")

except Exception as e:
    print(f"An unexpected error occurred during MongoDB setup: {e}")
    exit()
