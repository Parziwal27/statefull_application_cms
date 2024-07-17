# resources/claim_resource.py
from flask import jsonify, request
from flask_restful import Resource
from models.user import user_collection 
from models.claim import claim_collection 
from models.policy import policies_collection

class ClaimResource(Resource):
    def post(self, name):
        try:
            data = request.json
            policy_name = data.get('policy_name')
            amount = data.get('amount')
            policyholder = user_collection.find_one({'name': name})

            if not policyholder:
                return {"message": "Customer not found"}, 404
            policies = policyholder.get('policies', [])

            policy = None
            for pol in policies:
                if pol['policy_name'] == policy_name:
                    policy = pol
                    break

            if not policy:
                return {"message": f"{name} does not have {policy_name} policy"}, 400

            sum_assured = policy['sum_assured']

            total_claimed = 0
            claims = claim_collection.find({'policyholder_id': policyholder['_id'], 'policy_name': policy_name})
            for claim in claims:
                total_claimed += claim['amount']

            if total_claimed + amount > sum_assured:
                status = "rejected"
                message = "Claim amount exceeds policy limit"
            else:
                status = "approved"
                message = "Claim approved"

            # Create a claim document
            new_claim = {
                "policyholder_id": policyholder['_id'],
                "policy_name": policy_name,
                "amount": float(amount),
                "status": status
            }

            # Insert claim into claim_collection
            result = claim_collection.insert_one(new_claim)

            if result.inserted_id:
                return {"message": message, "claim_id": str(result.inserted_id), "status": status}, 201
            else:
                return {"message": "Failed to submit claim"}, 500

        except Exception as e:
            return {'error': str(e)}, 500
