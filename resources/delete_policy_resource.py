from flask import jsonify, request, make_response
from flask_restful import Resource
from models.user import user_collection

class DeletePolicyResource(Resource):
    def delete(self):
        try:
            data = request.json
            name = data.get('Usename')
            policy_name = data.get('policy_id')

            if not name or not policy_name:
                return make_response(jsonify({"message": "Name and policy name are required"}), 400)

            result = user_collection.update_one(
                {'Username': name},
                {'$pull': {'policies': {'policy_id': policy_name}}}
            )

            if result.modified_count == 0:
                return make_response(jsonify({"message": "Policy or policyholder not found"}), 404)

            return make_response(jsonify({"message": f"Policy '{policy_name}' deleted for policyholder '{name}'"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
