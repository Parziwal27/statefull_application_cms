# resources/policy_resource.py
from flask import jsonify
from flask_restful import Resource
from models.policy import policies_collection  # Adjust import as per your directory structure

class PolicyResource(Resource):
    def get(self):
        try:
            policies = list(policies_collection.find({}, {'_id': 0}))
            return jsonify(policies)
        except Exception as e:
            return {'error': str(e)}, 500
