from flask import jsonify, request, make_response
from models.claim import claim_collection
from models.user import user_collection
from bson.objectid  import ObjectId, InvalidId
from flask_restful import Resource
class ClaimResource(Resource):
    def get(self,name=None):
        try:
            if name:
                cursor = claim_collection.find({'policyholder_id': name}, {'_id': 0})
                policy_holder = list(cursor)
                if not policy_holder:
                    return make_response(jsonify({"msg": "Policyholder not found"}), 404)
                return make_response(jsonify(policy_holder), 200)
            else:
                policy_holders = list(claim_collection.find({}, {'_id': 0}))
                return make_response(jsonify(policy_holders), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
    def post(self,name):
        data = request.json

        user = user_collection.find_one({'Username': name})
        if not user:
            return {'msg': 'User not found'}, 404
        policy=None
        for p in user["policies"]:
            if p['policy_id']==data['policy_id']:
                policy = p
                break
        if not policy:
            return {'msg': 'Policy not found'}, 404

        if data['amount'] > policy['left_amount']:
            return {'msg': 'Claim amount exceeds the remaining policy amount'}, 400

        # Create the claim
        new_claim = {
            'policyholder_id': user["Username"],
            'policy_id': data['policy_id'],
            'amount': float(data['amount']),
            'status': 'pending'
        }

        result = claim_collection.insert_one(new_claim)
        
        return {'msg': 'Claim submitted successfully', 'claim_id': str(result.inserted_id)}, 201


class ConfirmClaimResource(Resource):
    def put(self, claim_id):
        try:
            claim = claim_collection.find_one({'_id': ObjectId(claim_id)})
            if not claim:
                return {'msg': 'Claim not found'}, 404

            if claim['status'] != 'pending':
                return {'msg': 'Claim is not in pending status'}, 400

            user = user_collection.find_one({"Username": claim['policyholder_id']})
            if not user:
                return {'msg': 'User not found'}, 404
            policy=None
            for p in user["policies"]:
                if p['policy_id']==claim['policy_id']:
                    policy = p
                    break
            if not policy:
                return {'msg': 'Policy not found'}, 404

            if claim['amount'] > policy['left_amount']:
                return {'msg': 'Claim amount exceeds the remaining policy amount'}, 400

            claim_collection.update_one(
                {'_id': ObjectId(claim_id)},
                {'$set': {'status': 'approved'}}
            )
            user_collection.update_one(
                {'_id': ObjectId(user['_id']), 'policies.policy_id': claim['policy_id']},
                {
                    '$push': {'policies.$.claimed_amounts': claim['amount']},
                    '$inc': {'policies.$.left_amount': -claim['amount']}
                }
            )

            return {'msg': 'Claim confirmed successfully'}, 200
        except:
            return {'msg': 'Failed to confirm claim'}, 500
class RejectClaimResource(Resource):
    def put(self, claim_id):
        try:
            claim = claim_collection.find_one({'_id': ObjectId(claim_id)})
            if not claim:
                return {'msg': 'Claim not found'}, 404

            if claim['status'] != 'pending':
                return {'msg': 'Claim is not in pending status'}, 400

            claim_collection.update_one(
                {'_id': ObjectId(claim_id)},
                {'$set': {'status': 'rejected'}}
            )
            return {'msg': 'Claim rejected successfully'}, 200
        except InvalidId:
            return {'msg': 'Invalid claim ID'}, 400
        except Exception as e:
            print(f"Error occurred: {e}")
            return {'msg': 'Failed to reject claim'}, 500
