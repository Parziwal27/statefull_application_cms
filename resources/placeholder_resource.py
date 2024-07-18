from flask import jsonify, request, make_response
from flask_restful import Resource
from models.user import user_collection
import uuid

class PlaceholderResource(Resource):
    def get(self, name=None):
        try:
            if name:
                cursor = user_collection.find({'Username': name}, {'_id': 0})
                policy_holder = list(cursor)
                if not policy_holder:
                    return make_response(jsonify({"message": "Policyholder not found"}), 404)
                return make_response(jsonify(policy_holder[0]), 200)
            else:
                policy_holders = list(user_collection.find({}, {'_id': 0}))
                return make_response(jsonify(policy_holders), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def post(self):
        try:
            data = request.json
            age = data.get('age')
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            mobile = data.get('mobile')
            is_admin = data.get('is_admin', False)
            is_verified = data.get('is_verified', 'pending')

            if not age or not username or not password or not first_name or not last_name or not email or not mobile:
                return make_response(jsonify({"message": "Name, age, username, password, first name, last name, email, and mobile are required"}), 400)
            if age < 18:
                return make_response(jsonify({"message": "Age must be 18 or older"}), 400)

            if user_collection.find_one({'Username': username}):
                return make_response(jsonify({"message": "Policyholder already exists"}), 400)

            new_policy_holder = {
                "Username": username,
                "Password": password,
                "First_name": first_name,
                "Last_name": last_name,
                "Email": email,
                "Mobile": mobile,
                "isAdmin": is_admin,
                "isVerified": is_verified,
                "age": age,
                "policies": []
            }

            user_collection.insert_one(new_policy_holder)
            return make_response(jsonify({"message": "Policyholder added successfully"}), 201)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def put(self, name):
        try:
            data = request.json
            policy_id = data.get('policy_id')
            category = data.get('category')
            policy_name = data.get('policy_name')
            sum_assured = float(data.get('sum_assured'))
            duration = data.get('duration')
            premium = float(data.get('premium'))
            left_amount=float(data.get('left_amount'))

            if not policy_id or not category or not policy_name or not sum_assured or not duration or not premium or not left_amount:
                return make_response(jsonify({"message": "All fields are required"}), 400)

            updated_policy = {
                "policy_id": policy_id,
                "category": category,
                "policy_name": policy_name,
                "sum_assured": sum_assured,
                "duration": duration,
                "premium": premium,
                "claimed_amounts":[],
                "left_amount":left_amount
            }

            existing_policy_holder = user_collection.find_one({'Username': name})

            if not existing_policy_holder:
                return make_response(jsonify({"message": "Policyholder not found"}), 404)

            policy_exists = False
            for policy in existing_policy_holder['policies']:
                if policy['policy_id'] == policy_id:
                    policy_exists = True
                    policy.update(updated_policy)
                    break

            if not policy_exists:
                existing_policy_holder['policies'].append(updated_policy)


            user_collection.update_one(
                {'Username': name},
                {'$set': {'policies': existing_policy_holder['policies']}}
            )

            return make_response(jsonify({"message": f"Policy '{policy_name}' updated for '{name}'"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def delete(self, name):
        try:
            result = user_collection.delete_one({'Username': name})

            if result.deleted_count == 0:
                return make_response(jsonify({"message": "Policyholder not found"}), 404)

            return make_response(jsonify({"message": f"Policyholder '{name}' deleted successfully"}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
