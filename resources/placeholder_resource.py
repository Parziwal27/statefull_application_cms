from flask import jsonify, request, make_response
from flask_restful import Resource
from models.placeholder import policy_holder_collection  # Adjust import as per your directory structure

class PlaceholderResource(Resource):
    def get(self, name=None):
        try:
            if name:
                cursor = policy_holder_collection.find({'name': name}, {'_id': 0})
                policy_holder = list(cursor)
                if not policy_holder:
                    return make_response(jsonify({"message": "Policyholder not found"}), 404)
                return make_response(jsonify(policy_holder[0]), 200)
            else:
                policy_holders = list(policy_holder_collection.find({}, {'_id': 0}))
                return make_response(jsonify(policy_holders), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def post(self):
        try:
            data = request.json
            name = data.get('name')
            age = data.get('age')

            if not name or not age:
                return make_response(jsonify({"message": "Name and age are required"}), 400)

            if age < 18:
                return make_response(jsonify({"message": "Age must be 18 or older"}), 400)

            if policy_holder_collection.find_one({'name': name}):
                return make_response(jsonify({"message": "Policyholder already exists"}), 400)

            new_policy_holder = {
                "name": name,
                "age": age,
                "policies": []
            }

            policy_holder_collection.insert_one(new_policy_holder)
            return make_response(jsonify({"message": "Policyholder added successfully"}), 201)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def put(self, name):
        try:
            data = request.json
            category = data.get('category')
            policy_name = data.get('policy_name')
            sum_assured = float(data.get('sum_assured'))
            duration = data.get('duration')
            premium = float(data.get('premium'))

            if not category or not policy_name or not sum_assured or not duration or not premium:
                return make_response(jsonify({"message": "All fields are required"}), 400)

            new_policy = {
                "category": category,
                "policy_name": policy_name,
                "sum_assured": sum_assured,
                "duration": duration,
                "premium": premium
            }

            existing_policy_holder = policy_holder_collection.find_one({'name': name})

            if not existing_policy_holder:
                return make_response(jsonify({"message": "Policyholder not found"}), 404)

            # Add the new policy to the policies array
            policy_holder_collection.update_one(
                {'name': name},
                {'$addToSet': {'policies': new_policy}}
            )

            return make_response(jsonify({"message": f"Policy '{policy_name}' added for '{name}'"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def delete(self, name):
        try:
            result = policy_holder_collection.delete_one({'name': name})

            if result.deleted_count == 0:
                return make_response(jsonify({"message": "Policyholder not found"}), 404)

            return make_response(jsonify({"message": f"Policyholder '{name}' deleted successfully"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
