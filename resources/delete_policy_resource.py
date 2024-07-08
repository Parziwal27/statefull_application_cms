from flask import jsonify, request, make_response
from flask_restful import Resource
from models.placeholder import policy_holder_collection  # Adjust import as per your directory structure

class DeletePolicyResource(Resource):
    def delete(self):
        try:
            data = request.json
            name = data.get('name')
            policy_name = data.get('policy_name')

            if not name or not policy_name:
                return make_response(jsonify({"message": "Name and policy name are required"}), 400)

            result = policy_holder_collection.update_one(
                {'name': name},
                {'$pull': {'policies': {'policy_name': policy_name}}}
            )

            if result.modified_count == 0:
                return make_response(jsonify({"message": "Policy or policyholder not found"}), 404)

            return make_response(jsonify({"message": f"Policy '{policy_name}' deleted for policyholder '{name}'"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
